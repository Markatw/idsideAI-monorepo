from fastapi.responses import Response
from fastapi.responses import JSONResponse
from fastapi import Request
import time
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from idsideai.routers import decision_models, telemetry
from security_toolkit.security_utils import wire_security
from security_toolkit.hardening import wire_security_full
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(
    openapi_tags=[
        {'name': 'telemetry', 'description': 'Health & metrics'},
        {'name': 'decision-models', 'description': 'Run decision models'}
    ],
    docs_url='/docs',
    openapi_version='3.0.3',
    title='idsideAI - Decision Layer'
)

from backend.router_autoinclude import autoload_routers
autoload_routers(app, "backend.routers")

# Apply security middleware
app = wire_security_full(app)

# Dev-only healthz bypass so perf skims don't hit rate limits
@app.middleware("http")
async def _dev_bypass_healthz(request: Request, call_next):
    if os.getenv("APP_ENV", "dev") == "dev" and request.url.path == "/healthz":
        return JSONResponse({"status": "ok"})
    return await call_next(request)

# Simple /status endpoint with uptime
START_TS = time.time()
@app.get("/status", tags=["telemetry"])
async def status():
    return {"status": "ok", "uptime_s": int(time.time() - START_TS)}

# Quiet auto-requested icons/favicons
@app.get("/apple-touch-icon.png")
@app.get("/apple-touch-icon-precomposed.png")
@app.get("/favicon.ico")
async def _icons():
    return Response(status_code=204)


# --- health endpoint (auto) ---
@app.get("/healthz", include_in_schema=False)
async def healthz():
    return {"status": "ok"}

# --- auto-wired routers ---
app.include_router(telemetry.router)
app.include_router(decision_models.router)

# --- CORS for local Vite dev server ---
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- end CORS ---
