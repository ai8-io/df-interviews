# Acme Corp HR Chatbot

An internal HR assistant that answers questions about employee data — compensation, team structure, and general HR queries.

## Prerequisites

- **Docker** (with Docker Compose)
- **Python 3.12+** with [uv](https://docs.astral.sh/uv/)
- **Node.js 20+** with npm

## Quick Start

```bash
# 1. Copy the env file and add your OpenRouter API key
cp .env.example backend/.env
# Edit backend/.env and set OPENROUTER_API_KEY

# 2. Start everything
chmod +x start.sh
./start.sh
```

This will:
- Start Postgres and Inngest via Docker Compose
- Install Python and Node dependencies
- Launch the FastAPI backend on **:8000**
- Launch the Vite frontend on **:5173**

## Manual Start

If you prefer to run things separately:

```bash
# Infrastructure
docker compose up -d

# Backend (in one terminal)
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000 --app-dir src

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── contracts/           # Shared type contracts
│   ├── python/          # Pydantic models (source of truth)
│   └── typescript/      # Zod schemas (mirrors Python)
├── backend/             # FastAPI application
│   ├── db/              # Employee data (CSV)
│   └── src/app/         # Application code
│       ├── chat/        # Conversation persistence
│       ├── clients/     # Employee data access
│       ├── ml/          # LLM agent integration
│       └── inngest_app/ # Background job functions
├── frontend/            # React + Vite + Tailwind
│   └── src/
│       ├── api/         # Backend API calls
│       ├── hooks/       # React hooks
│       └── components/  # UI components
├── docker-compose.yml   # Postgres + Inngest
└── init.sql             # Database schema
```

## URLs

| Service  | URL                          |
| -------- | ---------------------------- |
| Frontend | http://localhost:5173        |
| API Docs | http://localhost:8000/docs   |
| Inngest  | http://localhost:8388        |
