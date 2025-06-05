# codextest

This repository contains a minimal FastAPI "Hello World" example. Follow the steps below to set up a virtual environment, install dependencies and run the server locally.

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

4. **Open your browser** and navigate to `http://localhost:8000/`. You should see a mostly blank page with the text "hello world".

## Files

- `app/main.py` – FastAPI application entry point.
- `requirements.txt` – Python dependencies.

