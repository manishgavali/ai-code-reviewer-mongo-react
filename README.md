# AI Code Reviewer (React + FastAPI + MongoDB) — Compact Demo

**Student-written plain-language explainer:**
This project is a compact, runnable demo of an **AI Code Reviewer** using:
- Frontend: React (Vite)
- Backend: Python FastAPI
- Database: MongoDB (stores reviews)

The app lets you paste code (one file), sends it to the backend which runs simple static checks
(security, best practices, refactor hints), optionally calls an LLM if you set `OPENAI_API_KEY`,
saves the review to MongoDB, and returns a human-readable response shown in the React UI.

--- 
## What is included
- `api/` — FastAPI backend with MongoDB (pymongo) integration and endpoints `/api/review` and `/api/review/{id}`.
- `frontend/` — Vite + React app (single page) that allows pasting code and viewing results.
- `db/` — folder with a README describing MongoDB collections (no SQL file for Mongo).
- `architecture.md`, `deployment.md`, `CITATIONS.md`, `LICENSE`.

## Quick local run
Prereqs: Python 3.10+, Node 18+, MongoDB (local or Atlas).

1. Start MongoDB (or create Atlas cluster). Note connection string (MONGO_URI).
2. Backend:
   - `cd api`
   - Create venv: `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
   - Set env vars:
     - `export MONGO_URI="mongodb://localhost:27017"`
     - (optional) `export OPENAI_API_KEY="sk-..."`
   - `uvicorn main:app --reload --port 8000`
3. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`
   - Open `http://localhost:5173`

## Notes
- This demo is intentionally small to be easy to run and present.
- Edit README and other plain-text files in your own words before submission if required.
