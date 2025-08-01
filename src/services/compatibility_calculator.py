class CompatibilityCalculator:
    def calculate_score(self, user1_movies, user2_movies):
        """
        Calculate the compatibility score between two users based on their watched movies.
        The score is determined by the number of common movies watched by both users.
        """
        common_movies = set(user1_movies) & set(user2_movies)
        total_movies = set(user1_movies) | set(user2_movies)
        
        if not total_movies:
            return 0  # Avoid division by zero if both users have no watched movies
        
        score = len(common_movies) / len(total_movies)
        return score