def calculate_score(user1_ratings, user2_ratings):
    """
    Calculate compatibility score between two users based on their ratings.
    The score is based on the average rating difference for common movies.
    """
    common_movies = set(user1_ratings.keys()) & set(user2_ratings.keys())
    if len(common_movies) == 0:
        return 0.0

    total_difference = 0
    for movie in common_movies:
        rating1 = user1_ratings[movie]['rating']
        rating2 = user2_ratings[movie]['rating']
        total_difference += abs(rating1 - rating2)

    average_difference = total_difference / len(common_movies)
    compatibility_score = max(0, 100 - (average_difference * 20))
    return round(compatibility_score, 2)