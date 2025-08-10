import os
import json
import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import argparse


class LetterboxdScraper:
    def __init__(self):
        self.base_url = "https://letterboxd.com"
        self.session = None
    
    async def __aenter__(self):
        self.session = ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> Optional[bytes]:
        """Fetch web page content"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
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
        soup = BeautifulSoup(content, 'lxml')
        try:
            page_links = soup.find_all("li", class_="paginate-page")
            if page_links:
                last_page = page_links[-1].find("a").text.replace(",", "")
                return int(last_page)
            else:
                return 1
        except (IndexError, AttributeError, ValueError):
            return 1

    async def scrape_user_ratings_page(self, username: str, page: int) -> List[Dict]:
        """Scrape a single page of user ratings"""
        url = f"{self.base_url}/{username}/films/page/{page}/"
        content = await self.fetch_page(url)
        if not content:
            return []
        soup = BeautifulSoup(content, 'lxml')
        movies = soup.find_all("li", class_="poster-container")
        ratings = []
        for movie in movies:
            try:
                film_poster = movie.find("div", class_="film-poster")
                if not film_poster:
                    continue   
                movie_url = film_poster.get("data-target-link")
                if not movie_url:
                    continue 
                movie_id = movie_url.split("/")[-2]
                img = film_poster.find("img")
                movie_title = img.get("alt") if img else "Unknown title"
                rating_element = movie.find("span", class_="rating")
                rating_value = None
                if rating_element:
                    rating_classes = rating_element.get("class", [])
                    for class_name in rating_classes:
                        if class_name.startswith("rated-"):
                            try:
                                rating_value = int(class_name.split("-")[-1]) / 2.0
                                break
                            except ValueError:
                                pass
                movie_data = {"movie_id": movie_id,
                              "title": movie_title,
                              "rating": rating_value,
                              "letterboxd_url": f"{self.base_url}{movie_url}"}
                ratings.append(movie_data)
            except Exception as e:
                continue
        return ratings

    async def scrape_user_ratings(self, username: str, max_pages: Optional[int] = None) -> List[Dict]:
        """Scrape all ratings for a user"""
        total_pages = await self.get_user_page_count(username)
        if total_pages == 0:
            return []
        if max_pages:
            total_pages = min(total_pages, max_pages)
        tasks = []
        for page in range(1, total_pages + 1):
            task = self.scrape_user_ratings_page(username, page)
            tasks.append(task)
        all_ratings = []
        for coro in asyncio.as_completed(tasks):
            page_ratings = await coro
            all_ratings.extend(page_ratings)
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
        return ratings_dict

    def save_to_json(self, data: List[Dict], filename: str):
        """Save data to JSON format"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
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
        ratings = await scraper.scrape_user_ratings(args.username, args.pages)
        if ratings:
            output_data = {
                "username": args.username,
                "total_ratings": len(ratings),
                "scrape_date": "2025-08-02",
                "ratings": ratings
            }
            scraper.save_to_json(output_data, output_file)
            ratings_dict = await scraper.get_user_ratings_dict(args.username, args.pages)
        else:
            print("No ratings found")

if __name__ == "__main__":
    asyncio.run(main())
