# codextest

This repository contains a minimal FastAPI + Vue.js TODO application. Follow the steps below to set up a virtual environment, install dependencies and run the server locally.

## Setup

1. **Create a virtual environment** (Python 3.8+ recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:

   ```bash
   python -m app.main
   ```

4. **Open your browser** and navigate to `http://localhost:8000/`. You should see a simple TODO application where you can add, edit and delete notes.

The Vue.js code now lives in `app/static/main.js` and the HTML template is in `app/templates/index.html`. FastAPI serves these files via the `/static` route.

## Files

- `app/main.py` – FastAPI application entry point.
- `requirements.txt` – Python dependencies.

