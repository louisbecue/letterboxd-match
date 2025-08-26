import os
import json
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import argparse
from datetime import datetime
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
            pagination = soup.find("div", class_="pagination")
            if not pagination:
                return 1
            
            page_links = pagination.find_all("a")
            if not page_links:
                return 1

            page_numbers = []
            for link in page_links:
                href = link.get('href', '')
                page_match = re.search(r'/page/(\d+)/', href)
                if page_match:
                    page_numbers.append(int(page_match.group(1)))
            
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
                except (ValueError, IndexError):
                    continue
        return None

    async def scrape_user_ratings_page(self, username: str, page: int) -> List[Dict]:
        """Scrape a single page of user ratings"""
        url = f"{self.base_url}/{username}/films/page/{page}/"
        content = await self.fetch_page(url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')

        movies = soup.find_all("li", class_="griditem")
        ratings = []
        
        print(f"Found {len(movies)} movie items on page {page}")
        
        for movie in movies:
            try:
                react_component = movie.find("div", class_="react-component")
                if not react_component:
                    continue

                movie_title = react_component.get("data-item-name")
                if not movie_title:
                    continue
                
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
                    movie_data = {
                        "movie_id": movie_slug or "unknown",
                        "title": movie_title,
                        "rating": rating_value,
                        "letterboxd_url": movie_url
                    }
                    ratings.append(movie_data)
                    print(f"Found rated movie: {movie_title} ({rating_value}★)")
                
            except Exception as e:
                print(f"Error parsing movie: {e}")
                continue
        
        print(f"Successfully extracted {len(ratings)} ratings from page {page}")
        return ratings

    async def scrape_user_ratings(self, username: str, max_pages: Optional[int] = None) -> List[Dict]:
        """Scrape all ratings for a user"""
        print(f"Getting page count for user: {username}")
        total_pages = await self.get_user_page_count(username)
        
        if total_pages == 0:
            print(f"No pages found for user: {username}")
            return []
        
        if max_pages:
            total_pages = min(total_pages, max_pages)
        
        print(f"Scraping {total_pages} pages for user: {username}")

        semaphore = asyncio.Semaphore(3)
        
        async def scrape_with_semaphore(page):
            async with semaphore:
                await asyncio.sleep(1.0)
                return await self.scrape_user_ratings_page(username, page)
        
        all_ratings = []

        for page in range(1, total_pages + 1):
            try:
                print(f"Processing page {page}/{total_pages}")
                page_ratings = await self.scrape_user_ratings_page(username, page)
                all_ratings.extend(page_ratings)

                if page < total_pages:
                    await asyncio.sleep(1.5)
                    
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                continue
        
        return all_ratings

    async def get_user_ratings_dict(self, username: str, max_pages: Optional[int] = None) -> Dict[str, dict]:
        """
        Get user ratings as a dictionary:
        {movie_title: {'rating': ..., 'movie_id': ..., 'letterboxd_url': ...}}
        """
        ratings_list = await self.scrape_user_ratings(username, max_pages)
        ratings_dict = {}
        
        for movie in ratings_list:
            if movie.get('rating') is not None:
                ratings_dict[movie['title']] = {
                    'rating': movie['rating'],
                    'movie_id': movie.get('movie_id'),
                    'letterboxd_url': movie.get('letterboxd_url'),
                }
        
        print(f"Found {len(ratings_dict)} rated movies for {username}")
        return ratings_dict

    def save_to_json(self, data: List[Dict], filename: str):
        """Save data to JSON format"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Scraper to retrieve Letterboxd ratings")
    parser.add_argument("username", help="Letterboxd username")
    parser.add_argument("-o", "--output", default=None, help="JSON output file")
    parser.add_argument("-p", "--pages", type=int, default=None, help="Maximum number of pages to scrape")
    args = parser.parse_args()
    
    output_file = args.output or f"{args.username}_letterboxd_ratings.json"
    
    async with LetterboxdScraper() as scraper:
        print(f"Starting scrape for user: {args.username}")
        ratings = await scraper.scrape_user_ratings(args.username, args.pages)
        
        if ratings:
            output_data = {
                "username": args.username,
                "total_ratings": len(ratings),
                "scrape_date": datetime.now().isoformat(),
                "ratings": ratings
            }
            scraper.save_to_json(output_data, output_file)

            ratings_dict = await scraper.get_user_ratings_dict(args.username, args.pages)
            print(f"Successfully scraped {len(ratings)} movies with {len(ratings_dict)} rated movies")
        else:
            print("No ratings found")


if __name__ == "__main__":
    asyncio.run(main())
