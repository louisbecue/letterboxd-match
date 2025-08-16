import statistics

def calculate_score(user1_ratings, user2_ratings):
    """
    Calculate compatibility score between two users based on their ratings.
    The score is based on the average rating difference for common movies.
    Returns a tuple: (compatibility_score, number_of_common_movies)
    """
    common_movies = set(user1_ratings.keys()) & set(user2_ratings.keys())
    num_common_movies = len(common_movies)
    if num_common_movies == 0:
        return 0.0, 0

    total_difference = 0
    for movie in common_movies:
        rating1 = user1_ratings[movie]['rating']
        rating2 = user2_ratings[movie]['rating']
        total_difference += abs(rating1 - rating2)

    average_difference = total_difference / num_common_movies
    compatibility_score = max(0, 100 - (average_difference * 20))
    return round(compatibility_score, 2), num_common_movies


def four_favorite_movies(user1_ratings, user2_ratings):
    """
    Returns the four favorite movies in common between two users.
    """
    common_movies = set(user1_ratings.keys()) & set(user2_ratings.keys())
    if not common_movies:
        return []

    movies_with_avg = []
    for movie in common_movies:
        rating1 = user1_ratings[movie]['rating']
        rating2 = user2_ratings[movie]['rating']
        avg_rating = (rating1 + rating2) / 2
        movies_with_avg.append((movie, avg_rating))

    movies_with_avg.sort(key=lambda x: x[1], reverse=True)
    return [{'title': movie} for movie, _ in movies_with_avg[:4]]

def rating_patterns(user1_ratings, user2_ratings):
    """
    - Utilisateur plus généreux/sévère dans les notes
    - Distribution des notes (combien de 5★, 4★...)
    - Écart-type des notes (goûts éclectiques vs cohérents)
    """
    user1_scores = [rating['rating'] for rating in user1_ratings.values()]
    user2_scores = [rating['rating'] for rating in user2_ratings.values()]
    
    if not user1_scores or not user2_scores:
        return {}

    user1_avg = statistics.mean(user1_scores)
    user2_avg = statistics.mean(user2_scores)

    return {
        'user1_average': round(user1_avg, 2),
        'user2_average': round(user2_avg, 2),
    }