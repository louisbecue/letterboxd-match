def clean_movie_data(movie_data):
    cleaned_data = []
    for movie in movie_data:
        cleaned_movie = {
            'id': movie.get('id'),
            'title': movie.get('title'),
            'year': movie.get('year'),
            'rating': movie.get('rating'),
            'watched_date': movie.get('watched_date')
        }
        cleaned_data.append(cleaned_movie)
    return cleaned_data

def extract_user_movies(user_data):
    return clean_movie_data(user_data.get('movies', []))