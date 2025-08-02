# Letterboxd Scraper

An asynchronous web scraper to retrieve user ratings and reviews from Letterboxd and export them to JSON format.

## Installation

### Prerequisites

- Python 3.8+
- pip

### Dependencies

```bash
pip install aiohttp beautifulsoup4 lxml tqdm
```

## Usage

### Basic usage

- Scrape all ratings from a user

```bash
python src/services/scrapper.py username
```

### Advanced options

- With custom output file

```bash
python src/services/scrapper.py username -o my_ratings.json
```

- Limit number of pages (useful for testing)

```bash
python src/services/scrapper.py username -p 5
```

- Combine options

```bash
python src/services/scrapper.py username -o backup.json -p 10
```

## JSON output structure

The generated JSON file contains:

```json
{
  "username": "username",
  "total_ratings": 150,
  "scrape_date": "2025-08-02",
  "ratings": [
    {
      "movie_id": "the-matrix",
      "title": "The Matrix",
      "year": 1999,
      "rating": 4.5,
      "watch_date": "2025-01-15T00:00:00",
      "letterboxd_url": "https://letterboxd.com/film/the-matrix/"
    },
    {
      "movie_id": "inception",
      "title": "Inception",
      "year": 2010,
      "rating": 5.0,
      "watch_date": "2025-01-20T00:00:00",
      "letterboxd_url": "https://letterboxd.com/film/inception/"
    }
  ]
}
```

### Field descriptions

| Field | Type | Description |
|-------|------|-------------|
| `username` | string | Letterboxd username |
| `total_ratings` | integer | Total number of rated movies |
| `scrape_date` | string | Scraping date |
| `movie_id` | string | Unique movie identifier on Letterboxd |
| `title` | string | Movie title |
| `year` | integer/null | Movie release year |
| `rating` | float/null | Rating out of 5 (0.5 to 5.0 in 0.5 increments) |
| `watch_date` | string/null | Watch date in ISO format |
| `letterboxd_url` | string | Full URL to the movie page |

## Programmatic usage

You can also use the `LetterboxdScraper` class directly in your code:

```python
import asyncio
from src.services.scrapper import LetterboxdScraper

async def main():
    async with LetterboxdScraper() as scraper:
        # Get user ratings
        ratings = await scraper.scrape_user_ratings("username", max_pages=5)
        
        # Save to JSON
        output_data = {
            "username": "username",
            "total_ratings": len(ratings),
            "ratings": ratings
        }
        scraper.save_to_json(output_data, "output.json")

if __name__ == "__main__":
    asyncio.run(main())
```

### Estimated times

| Number of movies | Pages | Approximate time |
|-----------------|-------|------------------|
| 100 movies | 3-4 pages | 10-15 seconds |
| 500 movies | 15-20 pages | 30-45 seconds |
| 1000+ movies | 30+ pages | 1-2 minutes |

## Error handling

The scraper automatically handles:

- **Network errors**: Automatic retry and informative messages
- **Missing pages**: Ignores inaccessible pages
- **Parsing failures**: Continues even if some movies cannot be parsed
- **Non-existent users**: Clear error message

## Limitations

- **Letterboxd limit**: Maximum 128 scrapable pages per user
- **Rate limiting**: Respects site limitations
- **Private profiles**: Cannot access private profiles
- **Unrated movies**: Only rated movies are retrieved

## ⚠️ Warning

This scraper is intended for personal and educational use. Please respect Letterboxd's terms of service and do not abuse requests