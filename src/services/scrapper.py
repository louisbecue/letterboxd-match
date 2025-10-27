import json
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re


class LetterboxdScraper:
    def __init__(self):
        self.base_url = "https://letterboxd.com"
        self.session = None
    
    async def __aenter__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch web page content"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"HTTP {response.status} for {url}")
                    return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def get_user_page_count(self, username: str) -> int:
        """Get the number of pages of rated movies for the user"""
        url = f"{self.base_url}/{username}/films/"
        content = await self.fetch_page(url)
        if not content:
            return 0
        
        soup = BeautifulSoup(content, 'html.parser')
        try:
            pagination = soup.select_one("div.pagination")
            if not pagination:
                return 1
            
            page_links = pagination.find_all("a", href=True)
            page_numbers = [
                int(re.search(r'/page/(\d+)/', link['href']).group(1))
                for link in page_links if re.search(r'/page/(\d+)/', link['href'])
            ]
            return max(page_numbers) if page_numbers else 1
        except Exception as e:
            print(f"Error getting page count: {e}")
            return 1

    def extract_rating_from_classes(self, classes: List[str]) -> Optional[float]:
        """Extract rating from CSS classes like 'rated-8' (8 = 4 stars)"""
        for class_name in classes:
            if class_name.startswith('rated-'):
                try:
                    rating_num = int(class_name.replace('rated-', ''))
                    return rating_num / 2.0
                except ValueError:
                    continue
        return None

    async def scrape_user_ratings_page(self, username: str, page: int) -> List[Dict]:
        """Scrape a single page of user ratings"""
        url = f"{self.base_url}/{username}/films/page/{page}/"
        content = await self.fetch_page(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        movies = soup.select("li.griditem")
        ratings = []
        
        for movie in movies:
            try:
                react_component = movie.find("div", class_="react-component")
                if not react_component:
                    continue

                movie_title = react_component.get("data-item-name")
                if not movie_title:
                    continue
                
                movie_title = re.sub(r'\s*\(\d{4}(?:[^)]*)\)\s*$', '', movie_title).strip()
                    
                movie_slug = react_component.get("data-item-slug")
                movie_url = f"{self.base_url}/film/{movie_slug}/" if movie_slug else None

                rating_value = None
                viewingdata = movie.find("p", class_="poster-viewingdata")
                
                if viewingdata:
                    rating_span = viewingdata.find("span", class_="rating")
                    if rating_span:
                        classes = rating_span.get("class", [])
                        rating_value = self.extract_rating_from_classes(classes)
                
                if rating_value is not None:
                    ratings.append({
                        "movie_id": movie_slug or "unknown",
                        "title": movie_title,
                        "rating": rating_value,
                        "letterboxd_url": movie_url
                    })
            except Exception as e:
                print(f"Error parsing movie: {e}")
                continue
        
        return ratings

    async def scrape_user_ratings(self, username: str, max_pages: Optional[int] = None) -> List[Dict]:
        """Scrape all ratings for a user"""
        total_pages = await self.get_user_page_count(username)
        if total_pages == 0:
            print(f"No pages found for user: {username}")
            return []
        
        if max_pages:
            total_pages = min(total_pages, max_pages)

        tasks = [
            self.scrape_user_ratings_page(username, page)
            for page in range(1, total_pages + 1)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_ratings = []
        for result in results:
            if isinstance(result, list):
                all_ratings.extend(result)
            else:
                print(f"Error in scraping task: {result}")
        
        return all_ratings

    async def get_user_ratings_dict(self, username: str, max_pages: Optional[int] = None) -> Dict[str, dict]:
        """
        Get user ratings as a dictionary:
        {movie_title: {'rating': ..., 'movie_id': ..., 'letterboxd_url': ...}}
        """
        ratings_list = await self.scrape_user_ratings(username, max_pages)
        ratings_dict = {
            movie['title']: {
                'rating': movie['rating'],
                'movie_id': movie.get('movie_id'),
                'letterboxd_url': movie.get('letterboxd_url'),
            }
            for movie in ratings_list if movie.get('rating') is not None
        }
        return ratings_dict

    def save_to_json(self, data: List[Dict], filename: str):
        """Save data to JSON format"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

