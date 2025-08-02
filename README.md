# Letterboxd Match

Letterboxd Match is a web app to compare two Letterboxd users, calculate a compatibility score, and suggest movies.

**Online demo:** [https://letterboxd-match.onrender.com](https://letterboxd-match.onrender.com)

## Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML (Jinja2), CSS
- **Deployment:** Render (Gunicorn)
- **Configuration:** [`config.py`](config.py)

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

## Deployment & CI/CD

- All dependencies are listed in [`requirements.txt`](requirements.txt).
- Automatic deployment with Render: connect your Git repo, Render finds the `Procfile` and installs dependencies.

---

> **Disclaimer:**  
> This project is not affiliated with Letterboxd. For personal use only.