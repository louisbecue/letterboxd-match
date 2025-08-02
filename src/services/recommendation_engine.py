def generate_recommendations(user1_ratings: dict, user2_ratings: dict, user1_name: str, user2_name: str) -> dict:
    """Generate movie recommendations"""
    # Movies user1 loved (4+ stars) but user2 hasn't seen
    recommendations_for_user2 = [
        {
            "title": title,
            "rating": info.get('rating'),
            "movie_id": info.get('movie_id'),
            "letterboxd_url": info.get('letterboxd_url')
        }
        for title, info in user1_ratings.items()
        if isinstance(info.get('rating'), (int, float)) and info.get('rating', 0) >= 4.0 and title not in user2_ratings
    ][:10]
    
    # Movies user2 loved (4+ stars) but user1 hasn't seen  
    recommendations_for_user1 = [
        {
            "title": title,
            "rating": info.get('rating'),
            "movie_id": info.get('movie_id'),
            "letterboxd_url": info.get('letterboxd_url')
        }
        for title, info in user2_ratings.items()
        if isinstance(info.get('rating'), (int, float)) and info.get('rating', 0) >= 4.0 and title not in user1_ratings
    ][:10]
    
    return {
        f"for_{user1_name}": recommendations_for_user1,
        f"for_{user2_name}": recommendations_for_user2
    }