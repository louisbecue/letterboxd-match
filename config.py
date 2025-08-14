import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-insecure-key')
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')