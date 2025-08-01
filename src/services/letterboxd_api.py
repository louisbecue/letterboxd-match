import requests

BASE_URL = "https://api.letterboxd.com/api/v0/"

def fetch_user_data(username, api_key):
    response = requests.get(f"{BASE_URL}user/{username}", headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_movie_data(movie_id, api_key):
    response = requests.get(f"{BASE_URL}film/{movie_id}", headers={"Authorization": f"Bearer {api_key}"})
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()