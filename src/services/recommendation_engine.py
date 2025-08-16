import pandas as pd
import numpy as np
import os
import random
import ast

def parse_genres(genre_str):
        try:
            if genre_str == '[]' or not genre_str:
                return ''
            genres = ast.literal_eval(genre_str)
            return '|'.join(genres) if isinstance(genres, list) else ''
        except:
            return ''

def load_letterboxd_data():
    """Load Letterboxd data from CSV"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "..", "data", "Movie_Data_File_Light.csv")
    
    movies = pd.read_csv(data_path)
    
    movies = movies.fillna({'Film_title': '', 'Genres': '[]', 'Average_rating': 0, 'Total_ratings': 0})
    movies['Average_rating'] = pd.to_numeric(movies['Average_rating'], errors='coerce').fillna(0)
    movies['Total_ratings'] = pd.to_numeric(movies['Total_ratings'], errors='coerce').fillna(0)

    movies = movies.assign(
        genres=movies['Genres'].apply(parse_genres),
        title=movies['Film_title'],
        mean=movies['Average_rating'],
        count=movies['Total_ratings']
    )
    
    return movies

def calculate_user_preferences(user_ratings: dict, movies_df: pd.DataFrame):
    """Calculate user preferences based on genres and ratings"""
    user_profile = {}
    for title, info in user_ratings.items():
        rating = info.get('rating', 0)
        if isinstance(rating, (int, float)) and rating >= 3.5:
            movie_match = movies_df[movies_df['title'].str.contains(title, case=False, na=False, regex=False)]
            if not movie_match.empty:
                genres_str = movie_match.iloc[0]['genres']
                if genres_str:
                    for genre in genres_str.split('|'):
                        genre = genre.strip()
                        if genre:
                            user_profile[genre] = user_profile.get(genre, 0) + rating
    return user_profile

def find_similar_movies(user1_profile: dict, user2_profile: dict, movies_df: pd.DataFrame, user1_ratings: dict, user2_ratings: dict):
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
    movies_with_ratings = movies_df[movies_df['count'] >= 1000].copy()
    preferred_genres_shuffled = preferred_genres.copy()
    random.shuffle(preferred_genres_shuffled)
    
    for genre, preference_score in preferred_genres_shuffled[:7]:
        if not genre or genre.strip() == '':
            continue
            
        genre_movies = movies_with_ratings[movies_with_ratings['genres'].str.contains(genre, case=False, na=False)].copy()
        genre_movies = genre_movies[~genre_movies['title'].apply(lambda x: any(x.lower() in seen_title.lower() for seen_title in seen_movies))]
        genre_movies = genre_movies[~genre_movies['title'].apply(lambda x: x in recommended_titles)]
        
        if len(genre_movies) == 0:
            continue

        genre_movies['composite_score'] = (genre_movies['mean'] * 0.6 + np.random.random(len(genre_movies)) * 1.5 +
            np.log(genre_movies['count'] + 1) * 0.1)
        
        genre_movies = genre_movies.sort_values('composite_score', ascending=False)
        num_movies = random.randint(1, min(4, len(genre_movies)))
        for _, movie in genre_movies.head(num_movies).iterrows():
            if len(recommendations) < 20:
                title = movie['title']
                if title not in recommended_titles:
                    recommended_titles.add(title)
                    letterboxd_url = movie.get('Film_URL', '')
                    recommendations.append({
                        "title": title,
                        "letterboxd_url": letterboxd_url,
                        "reason": f"Perfect match for your shared love of {genre} movies (★{round(movie['mean'], 1)})"
                    })
    return recommendations[:15]

def generate_recommendations(user1_ratings: dict, user2_ratings: dict, user1_name: str, user2_name: str) -> dict:
    """Generate movie recommendations"""
    recommendations_for_user2 = sorted(
        [{
            "title": title,
            "rating": info.get('rating', 0),
            "letterboxd_url": info.get('letterboxd_url'),
            "reason": f"Loved by {user1_name} (★{info.get('rating')})"
        }
        for title, info in user1_ratings.items() 
        if (isinstance(info.get('rating'), (int, float)) and info.get('rating', 0) >= 4.0 and title not in user2_ratings)],
        key=lambda x: x.get("rating", 0), reverse=True
    )[:5]
    
    recommendations_for_user1 = sorted(
        [{
            "title": title,
            "rating": info.get('rating', 0),
            "letterboxd_url": info.get('letterboxd_url'),
            "reason": f"Loved by {user2_name} (★{info.get('rating')})"
        }
        for title, info in user2_ratings.items()
        if (isinstance(info.get('rating'), (int, float)) and info.get('rating', 0) >= 4.0 and title not in user1_ratings)],
        key=lambda x: x.get("rating", 0), reverse=True
    )[:5]

    try:
        movies_df = load_letterboxd_data()
        user1_profile = calculate_user_preferences(user1_ratings, movies_df)
        user2_profile = calculate_user_preferences(user2_ratings, movies_df)
        mutual_recommendations = find_similar_movies(user1_profile, user2_profile, movies_df, user1_ratings, user2_ratings)
        
    except Exception as e:
        print(f"Error loading Letterboxd data: {e}")
        mutual_recommendations = []
        user1_profile = {}
        user2_profile = {}

    return {
        f"for_{user1_name}": recommendations_for_user1,
        f"for_{user2_name}": recommendations_for_user2,
        "mutual_recommendations": mutual_recommendations,
    }
