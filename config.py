import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    LETTERBOXD_API_KEY = os.environ.get('LETTERBOXD_API_KEY') or 'your_letterboxd_api_key'
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///site.db'
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'