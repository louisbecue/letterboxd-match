from flask import Blueprint, request, render_template, current_app
import asyncio
from ..services.scrapper import LetterboxdScraper
from ..services.tmdb_service import TMDBService
from ..services.recommendation_engine import load_letterboxd_data, calculate_user_preferences, find_similar_movies
import pandas as pd
import numpy as np

analyze_bp = Blueprint('analyze', __name__)

async def fetch_user_ratings(username: str) -> dict:
    """Fetch user ratings as a simple dictionary {movie_title: rating}"""
    try:
        async with LetterboxdScraper() as scraper:
            ratings_dict = await scraper.get_user_ratings_dict(username, max_pages=10)
            return ratings_dict
    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
        return {}

def calculate_user_stats(user_ratings: dict) -> dict:
    """Calculate user statistics"""
    if not user_ratings:
        return {}
    
    ratings = [info.get('rating', 0) for info in user_ratings.values() if info.get('rating')]
    
    if not ratings:
        return {}
    
    return {
        'total_movies': len(user_ratings),
        'average_rating': round(np.mean(ratings), 1),
        'highest_rated': max(ratings),
        'lowest_rated': min(ratings),
        'most_common_rating': float(pd.Series(ratings).mode().iloc[0]) if len(pd.Series(ratings).mode()) > 0 else 0,
        'rating_distribution': {
            '5_stars': len([r for r in ratings if r == 5.0]),
            '4.5_stars': len([r for r in ratings if r == 4.5]),
            '4_stars': len([r for r in ratings if r == 4.0]),
            '3.5_stars': len([r for r in ratings if r == 3.5]),
            '3_stars': len([r for r in ratings if r == 3.0]),
            'below_3': len([r for r in ratings if r < 3.0]),
        }
    }

def generate_solo_recommendations(user_ratings: dict) -> list:
    """Generate recommendations for solo user based on their preferences"""
    try:
        movies_df = load_letterboxd_data()
        user_profile = calculate_user_preferences(user_ratings, movies_df)
        
        # Create a dummy second user profile for using existing recommendation logic
        dummy_profile = {}
        recommendations = find_similar_movies(user_profile, dummy_profile, movies_df, user_ratings, {})
        
        # Also add highly rated movies from similar genres
        seen_movies = set(user_ratings.keys())
        movies_with_ratings = movies_df[movies_df['count'] >= 1000].copy()
        
        additional_recs = []
        for genre in user_profile.keys():
            if not genre or genre.strip() == '':
                continue
            
            genre_movies = movies_with_ratings[
                movies_with_ratings['genres'].str.contains(genre, case=False, na=False)
            ].copy()
            
            genre_movies = genre_movies[
                ~genre_movies['title'].apply(
                    lambda x: any(x.lower() in seen_title.lower() for seen_title in seen_movies)
                )
            ]
            
            if len(genre_movies) > 0:
                # Sort by rating and popularity
                genre_movies = genre_movies.sort_values(['mean', 'count'], ascending=[False, False])
                
                for _, movie in genre_movies.head(2).iterrows():
                    additional_recs.append({
                        "title": movie['title'],
                        "letterboxd_url": movie.get('Film_URL', ''),
                        "reason": f"Highly rated {genre} film (★{round(movie['mean'], 1)})"
                    })
        
        # Combine and limit recommendations
        all_recs = recommendations + additional_recs
        return all_recs[:20]
        
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return []

@analyze_bp.route('/analyze', methods=['POST'])
def analyze_user():
    """Analyze a single Letterboxd user"""
    try:
        username = request.form.get('username')
        
        if not username:
            return render_template('solo_results.html', error='Username is required')
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            user_ratings = loop.run_until_complete(fetch_user_ratings(username))
        finally:
            loop.close()

        if not user_ratings:
            return render_template('solo_results.html', 
                                 error=f'Could not fetch data for user {username}. Please check the username.')
        
        # Calculate statistics
        stats = calculate_user_stats(user_ratings)
        top_movies = get_top_movies(user_ratings)
        recommendations = generate_solo_recommendations(user_ratings)
        
        # Enrich with posters
        tmdb_service = TMDBService(current_app.config.get('TMDB_API_KEY'))
        if tmdb_service.api_key:
            top_movies = tmdb_service.enrich_movies_with_poster(top_movies)
            recommendations = tmdb_service.enrich_movies_with_poster(recommendations)
        
        return render_template(
            'solo_results.html',
            username=username,
            stats=stats,
            top_movies=top_movies,
            recommendations=recommendations
        )
        
    except Exception as e:
        print(f"Error in analyze_user: {e}")
        return render_template(
            'solo_results.html',
            error=f'Internal server error: {str(e)}',
            username='',
            stats={},
            top_movies=[],
            recommendations=[]
        )