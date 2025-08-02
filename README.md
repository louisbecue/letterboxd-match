# 🎬 Letterboxd Match

A web app to compare two Letterboxd users, calculate a compatibility score, and suggest movies.

**Live demo:** [https://letterboxd-match.onrender.com](https://letterboxd-match.onrender.com)

---

## Technical Overview

- **Backend:** Python 3, Flask
- **Frontend:** HTML (Jinja2 templates), CSS
- **Deployment:** Render (Gunicorn)
- **Configuration:** See [`config.py`](config.py)

## Project Structure

```
src/
  app.py                # Flask app entry point
  routes/               # API routes
  services/             # Logic for compatibility & recommendations
static/                 # CSS
templates/              # HTML templates
Procfile                # For Render deployment
requirements.txt        # Python dependencies
config.py               # App configuration
```

## Run Locally

1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start the development server

```bash
python -m src.app
```

The site will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Deployment

- All dependencies are listed in [`requirements.txt`](requirements.txt)
- Ready for Render: connect your repository and deploy.

---

> **Disclaimer:**  
> This project is not affiliated with Letterboxd.
pip install -r requirements.txt