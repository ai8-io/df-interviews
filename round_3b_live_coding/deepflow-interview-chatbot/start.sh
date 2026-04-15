#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Starting infrastructure (Postgres + Inngest)..."
docker compose up -d --wait

echo ""
echo "Installing backend dependencies..."
cd backend && uv sync && cd ..

echo ""
echo "Installing frontend dependencies..."
cd frontend && npm install --silent && cd ..

echo ""
echo "Running database migrations..."
cd backend && .venv/bin/alembic upgrade head && cd ..

echo ""
echo "================================================"
echo "  Acme Corp HR Chatbot is running!"
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:8000/docs"
echo "  Inngest:   http://localhost:8388"
echo "================================================"
echo ""

echo "Starting backend (FastAPI on :8000)..."
backend/.venv/bin/python -m uvicorn app.main:app --reload --port 8000 --app-dir backend/src &
BACKEND_PID=$!

echo "Starting frontend (Vite on :5173)..."
cd frontend && npm run dev &
FRONTEND_PID=$!
cd ..

cleanup() {
    echo "Shutting down..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    docker compose down
}
trap cleanup EXIT

wait
