# Advanced AI Stock Analysis Assistant

## Project structure

- `/backend` - FastAPI backend + LangChain agent
- `/frontend` - React + TypeScript UI (Vite)

## Quick start

1. Backend
   - `cd backend`
   - `uv run main.py`
2. Frontend
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Calls

- Frontend POST `/api/chat` -> Backend agent streaming with SSE.
