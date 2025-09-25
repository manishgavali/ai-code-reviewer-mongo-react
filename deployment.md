# Deployment instructions (React + FastAPI + MongoDB)

## Prerequisites
- Node 18+ and npm
- Python 3.10+
- MongoDB (local or Atlas)

## Backend (api)
1. Create virtualenv:
   ```
   cd api
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `MONGO_URI` e.g. `mongodb://localhost:27017` or Atlas connection string
   - (optional) `OPENAI_API_KEY` to enable LLM summaries
3. Run:
   ```
   uvicorn main:app --reload --port 8000
   ```

## Frontend
1. Install:
   ```
   cd frontend
   npm install
   npm run dev
   ```
2. Open `http://localhost:5173`

## Deploying
- For production, build frontend (`npm run build`) and serve static files; host backend on Railway/Render/Vercel (serverless) and set MONGO_URI.
