#!/bin/bash
# Mac-optimized startup script for idsideAI

echo "🚀 Starting idsideAI on Mac..."

# Check Python version
python3 --version

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Set environment variables
export PYTHONPATH="$PWD:$PYTHONPATH"

# Start the application
echo "🌐 Starting server on http://localhost:8013"
python3 run.py
