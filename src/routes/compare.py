from flask import Blueprint, request, jsonify, render_template
import asyncio
import time
import os
from dotenv import load_dotenv
from ..services.scrapper import LetterboxdScraper
from ..services.compatibility_calculator import calculate_score
from ..services.recommendation_engine import generate_recommendations
from ..services.tmdb_service import TMDBService

# Charge les variables d'environnement
load_dotenv()

compare_bp = Blueprint('compare', __name__)
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# tmp
import json

def load_ratings(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    ratings_dict = {}
    for movie in data.get('ratings', []):
        title = movie.get('title', 'Unknown Title')
        ratings_dict[title] = {
            'rating': movie.get('rating'),
            'movie_id': movie.get('movie_id'),
            'letterboxd_url': movie.get('letterboxd_url')
        }
    return ratings_dict
#end tmp

async def fetch_user_ratings(username: str) -> dict:
    """Fetch user ratings as a simple dictionary {movie_title: rating}"""
    try:
        async with LetterboxdScraper() as scraper:
            ratings_dict = await scraper.get_user_ratings_dict(username, max_pages=10)
            return ratings_dict
    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
        return {}

@compare_bp.route('/compare', methods=['POST'])
def compare_users():
    """Compare two Letterboxd users"""
    try:
        username1 = request.form.get('user1')
        username2 = request.form.get('user2')
        
        if not username1 or not username2:
            return render_template('results.html', error='Both username1 and username2 are required')
        
        # # Run async function in Flask context
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        
        # try:
        #     # Fetch user ratings as simple dictionaries
        #     user1_ratings = loop.run_until_complete(fetch_user_ratings(username1))
        #     user2_ratings = loop.run_until_complete(fetch_user_ratings(username2))
        # finally:
        #     loop.close()

        user1_ratings = load_ratings(f'tmp/louis_bce_letterboxd_ratings.json')
        user2_ratings = load_ratings(f'tmp/emma_cinema_letterboxd_ratings.json')

        if not user1_ratings:
            return jsonify({'error': f'Could not fetch data for user {username1}'}), 404
        
        if not user2_ratings:
            return jsonify({'error': f'Could not fetch data for user {username2}'}), 404
        
        compatibility_score = calculate_score(user1_ratings, user2_ratings)
        recommendations = generate_recommendations(user1_ratings, user2_ratings, username1, username2)

        recs = recommendations.get(f"for_{username1}", []) + recommendations.get(f"for_{username2}", [])

        tmdb_service = TMDBService(TMDB_API_KEY)
        recs = tmdb_service.enrich_recommendations(recs)

        user1 = {'username': username1, 'total_ratings': len(user1_ratings)}
        user2 = {'username': username2, 'total_ratings': len(user2_ratings)}

        return render_template(
            'results.html',
            user1=user1,
            user2=user2,
            compatibility_score=compatibility_score,
            recommendations=recs
        )
    except Exception as e:
        return render_template(
            'results.html',
            error=f'Internal server error: {str(e)}', 
            user1={'username': '', 'total_ratings': 0},
            user2={'username': '', 'total_ratings': 0},
            compatibility_score=0,
            recommendations=[]
        )

@compare_bp.route('/compare', methods=['POST'])
def compare():
    """POST endpoint for compare route using form data"""
    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    return jsonify({
        'message': 'Compare route - POST received',
        'username1': username1,
        'username2': username2
    })