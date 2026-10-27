#!/usr/bin/env bash
set -e

echo "=== Starting Kasi-Logistics Local Environment ==="

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Kasi-Logistics API on http://127.0.0.1:8090..."
uvicorn app.main:app --host 127.0.0.1 --port 8090 --reload