class User:
    def __init__(self, user_id, username, watched_movies=None):
        self.user_id = user_id
        self.username = username
        self.watched_movies = watched_movies if watched_movies is not None else []

    def add_movie(self, movie):
        if movie not in self.watched_movies:
            self.watched_movies.append(movie)

    def remove_movie(self, movie):
        if movie in self.watched_movies:
            self.watched_movies.remove(movie)

    def get_watched_movies(self):
        return self.watched_movies

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', watched_movies={self.watched_movies})"