import requests

class TMDBService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
    
    def search_movie(self, title: str, year: str = None):
        """Search for a movie by title"""
        url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'query': title,
            'language': 'en-US'
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                movie = data['results'][0]
                poster_path = movie.get('poster_path')
                if poster_path:
                    return f"{self.image_base_url}{poster_path}"
            return None
        except Exception as e:
            print(f"TMDB error for '{title}': {e}")
            return None
    
    def enrich_recommendations(self, recommendations: list):
        """Add poster URLs to recommendations"""
        for rec in recommendations:
            poster_url = self.search_movie(rec['title'])
            rec['poster_url'] = poster_url
        return recommendations