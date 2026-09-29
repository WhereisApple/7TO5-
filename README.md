# 7TO5

A FastAPI-based web app for the 7TO5 language learning site and sandbox.

## Features
- Learn page with 7TO5 syntax examples
- Try page with live code execution
- About Developer page for your portfolio link
- Secure FastAPI headers and deployment-friendly setup

## Local development

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open:
- http://localhost:8000/learn
- http://localhost:8000/try
- http://localhost:8000/about

## Deployment

This app is set up for deployment on Render with:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Notes
The About Developer page contains a placeholder portfolio link that you can replace with your own profile URL.
