# Quickstart (Local)
## Backend
cd idsideAI_FIXED/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip "fastapi>=0.112" "uvicorn[standard]>=0.30"
uvicorn app:app --host 0.0.0.0 --port 8013

## Frontend (serve built dist)
cd ../frontend/dist
python3 -m http.server 5173
# open http://127.0.0.1:5173
