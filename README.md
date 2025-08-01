# 🎬 Letterboxd Match

A web app to compare two Letterboxd users, calculate a compatibility score, and suggest movies.

**Live demo:** [https://letterboxd-match.onrender.com](https://letterboxd-match.onrender.com)

---

## 🛠️ Technical Overview

- **Backend:** Python 3, Flask
- **Frontend:** HTML (Jinja2 templates), CSS, JS
- **Deployment:** Render (Gunicorn)
- **Configuration:** See [`config.py`](config.py)

### Project Structure

```
src/
  app.py                # Flask app entry point
  routes/               # API routes (compare, recommendations)
  models/               # Data models
  services/             # Logic for compatibility & recommendations
  utils/                # Helpers
static/                 # CSS & JS
templates/              # HTML templates
Procfile                # For Render deployment
requirements.txt        # Python dependencies
config.py               # App configuration
```

### Deployment

- All dependencies are listed in [`requirements.txt`](requirements.txt)
- [`Procfile`](Procfile) for Gunicorn:
  ```
  web: gunicorn -m src.app
  ```
- Ready for Render: connect your repository and deploy.

---

> **Disclaimer:**  
> This project is not affiliated with or endorsed by Letterboxd.  
> It is an independent project built for educational and personal purposes.
