# Letterboxd Match
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2%2B-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Live on Render](https://img.shields.io/badge/Render-Live-46E3B4?logo=render&logoColor=white)](https://letterboxd-match.onrender.com)
[![License](https://img.shields.io/badge/License-See%20LICENCE-lightgrey)](LICENCE)

Letterboxd Match is a web app to compare two Letterboxd users, calculate a compatibility score, and suggest movies.

**Online demo:** [https://letterboxd-match.up.railway.app](https://letterboxd-match.up.railway.app)
  
**Alternate demo:** [https://letterboxd-match.onrender.com](https://letterboxd-match.onrender.com)


## Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML (Jinja2), CSS
- **Deployment:** Gunicorn
- **Configuration:** [`config.py`](config.py)
- **Depenencies:** [`requirements.txt`](requirements.txt)

## Project Structure

```
src/
  app.py                # Flask entry point
  routes/               # API routes
  services/             # Business logic (compatibility, recommendations)
static/                 # CSS files
templates/              # HTML templates
Procfile                # Render/Gunicorn config
requirements.txt        # Python dependencies
config.py               # App settings
```

## Local Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:

   ```bash
   python -m src.app
   ```

   Access the app: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

> **Disclaimer:**  
> This project is not affiliated with Letterboxd. For personal use only.
