import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import random

def load_movielens_data():
    """Load MovieLens data"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "..", "data", "ml-latest-small")
    
    movies = pd.read_csv(os.path.join(data_path, "movies.csv"))
    ratings = pd.read_csv(os.path.join(data_path, "ratings.csv"))
    tags = pd.read_csv(os.path.join(data_path, "tags.csv"))
    
    return movies, ratings, tags

def calculate_user_preferences(user_ratings: dict, movies_df: pd.DataFrame, ratings_df: pd.DataFrame):
    """Calculate user preferences based on genres and ratings"""
    user_profile = {}
    
    for title, info in user_ratings.items():
        rating = info.get('rating', 0)
        if isinstance(rating, (int, float)) and rating >= 3.5:
            movie_match = movies_df[movies_df['title'].str.contains(title.split('(')[0].strip(), case=False, na=False)]
            if not movie_match.empty:
                genres = movie_match.iloc[0]['genres'].split('|')
                for genre in genres:
                    if genre != '(no genres listed)':
                        user_profile[genre] = user_profile.get(genre, 0) + rating
    
    return user_profile

def find_similar_movies(user1_profile: dict, user2_profile: dict, movies_df: pd.DataFrame, user1_ratings: dict, user2_ratings: dict, ratings_df: pd.DataFrame):
    """Find movies similar to both users' preferences"""
    
    combined_preferences = {}
    all_genres = set(list(user1_profile.keys()) + list(user2_profile.keys()))
    
    for genre in all_genres:
        pref1 = user1_profile.get(genre, 0)
        pref2 = user2_profile.get(genre, 0)
        if pref1 > 0 and pref2 > 0:
            combined_preferences[genre] = (pref1 + pref2) / 2
        elif pref1 > 0 or pref2 > 0:
            combined_preferences[genre] = max(pref1, pref2) * 0.7
    
    preferred_genres = sorted(combined_preferences.items(), key=lambda x: x[1], reverse=True)
    
    recommendations = []
    seen_movies = set(user1_ratings.keys()) | set(user2_ratings.keys())
    recommended_titles = set()
    
    movie_avg_ratings = ratings_df.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()
    movie_avg_ratings = movie_avg_ratings[movie_avg_ratings['count'] >= 10]
    
    movies_with_ratings = movies_df.merge(movie_avg_ratings, on='movieId', how='inner')
    
    preferred_genres_shuffled = preferred_genres.copy()
    random.shuffle(preferred_genres_shuffled)
    
    for genre, preference_score in preferred_genres_shuffled[:7]:
        genre_movies = movies_with_ratings[movies_with_ratings['genres'].str.contains(genre, case=False, na=False)].copy()
        
        genre_movies = genre_movies[~genre_movies['title'].apply(lambda x: any(x.split('(')[0].strip().lower() in seen_title.lower() 
                                    for seen_title in seen_movies))]
        
        genre_movies = genre_movies[~genre_movies['title'].apply(lambda x: x.split('(')[0].strip() in recommended_titles)]
        
        if len(genre_movies) == 0:
            continue
        
        genre_movies['composite_score'] = (genre_movies['mean'] * 0.6 +np.random.random(len(genre_movies)) * 2 +
                                           genre_movies['title'].apply(lambda x: get_year_bonus(x)) * 0.2)
        
        genre_movies = genre_movies.sort_values('composite_score', ascending=False)
        
        num_movies = random.randint(1, min(4, len(genre_movies)))
        
        for _, movie in genre_movies.head(num_movies).iterrows():
            if len(recommendations) < 20:
                title_no_year = movie['title'].split('(')[0].strip()
                
                if title_no_year not in recommended_titles:
                    recommended_titles.add(title_no_year)
                    recommendations.append({
                        "title": title_no_year,
                        "genres": movie['genres'],
                        "avg_rating": round(movie['mean'], 2),
                        "rating_count": movie['count'],
                        "movie_id": movie['movieId'],
                        "preference_match": round(preference_score, 2),
                        "reason": f"Perfect match for your shared love of {genre} movies (★{round(movie['mean'], 1)})"
                    })

    return recommendations[:15]

def get_year_bonus(title):
    """Gives a bonus to more recent movies"""
    try:
        if '(' in title and ')' in title:
            year_str = title.split('(')[-1].split(')')[0]
            if year_str.isdigit():
                year = int(year_str)
                current_year = 2025
                if year >= 2020:
                    return 1.0
                elif year >= 2010:
                    return 0.7
                elif year >= 2000:
                    return 0.4
                else:
                    return 0.1
    except:
        pass
    return 0.3

def generate_recommendations(user1_ratings: dict, user2_ratings: dict, user1_name: str, user2_name: str) -> dict:
    """Generate movie recommendations"""
    
    recommendations_for_user2 = sorted(
        [
            {
                "title": title,
                "rating": info.get('rating'),
                "movie_id": info.get('movie_id'),
                "letterboxd_url": info.get('letterboxd_url'),
                "reason": f"Loved by {user1_name} (★{info.get('rating')})"
            }
            for title, info in user1_ratings.items()
            if (isinstance(info.get('rating'), (int, float)) and info.get('rating', 0) >= 4.0 and title not in user2_ratings)
        ],
        key=lambda x: x["rating"],
        reverse=True
    )[:5]
    
    recommendations_for_user1 = sorted(
        [
            {
                "title": title,
                "rating": info.get('rating'),
                "movie_id": info.get('movie_id'),
                "letterboxd_url": info.get('letterboxd_url'),
                "reason": f"Loved by {user2_name} (★{info.get('rating')})"
            }
            for title, info in user2_ratings.items()
            if (isinstance(info.get('rating'), (int, float)) and info.get('rating', 0) >= 4.0 and title not in user1_ratings)
        ],
        key=lambda x: x["rating"],
        reverse=True
    )[:5]
    
    try:
        movies_df, ratings_df, tags_df = load_movielens_data()
        
        user1_profile = calculate_user_preferences(user1_ratings, movies_df, ratings_df)
        user2_profile = calculate_user_preferences(user2_ratings, movies_df, ratings_df)
        
        mutual_recommendations = find_similar_movies(
            user1_profile, user2_profile, movies_df, user1_ratings, user2_ratings, ratings_df
        )
        
    except Exception as e:
        print(f"Error loading MovieLens data: {e}")
        mutual_recommendations = []

    return {
        f"for_{user1_name}": recommendations_for_user1,
        f"for_{user2_name}": recommendations_for_user2,
        "mutual_recommendations": mutual_recommendations,
        "user_profiles": {
            user1_name: user1_profile if 'user1_profile' in locals() else {},
            user2_name: user2_profile if 'user2_profile' in locals() else {}
        }
    }
