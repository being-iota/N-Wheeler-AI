#!/bin/bash

# Start script for backend

echo "🚀 Starting Vehicle Maintenance AI System Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration before continuing."
fi

# Start the server
echo "✅ Starting FastAPI server..."
uvicorn main:app --reload --port 8000 --host 0.0.0.0

