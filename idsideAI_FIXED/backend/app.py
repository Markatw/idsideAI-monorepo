import time
import os
from fastapi.responses import Response
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel  # added

class HealthResponse(BaseModel):
    status: str = "ok"

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.middleware.tenant import TenantContextMiddleware
from backend.routers.graphs import router as graphs_router
from backend.routers.billing import router as billing_router
from backend.auth import jwt_auth
from backend.routers.metrics import router as metrics_router
from backend.auth.middleware import get_auth, inject_tenant_headers
from backend.routers.exports import router as exports_router
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from security_toolkit.security_utils import wire_security
from security_toolkit.hardening import wire_security_full

app = FastAPI(openapi_version="3.0.3", title="IDECIDE Graph API (Neo4j)", version="0.1.0")
app = wire_security_full(app)  # security headers + optional rate limiting
app.add_middleware(TenantContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.router_autoinclude import autoload_routers
autoload_routers(app, "backend.routers")

# app.include_router(graphs_router, prefix="/graphs", tags=["graphs"])
# 0
# 0

@app.get("/health", response_model=HealthResponse, summary="Health")
async def health():
    return {"status":"ok"}

# alias for previous checks
@app.get("/healthz", response_model=HealthResponse, summary="Health (alias)")
async def healthz():
    return {"status": "ok"}


EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)
app.mount("/exports", StaticFiles(directory=EXPORT_DIR), name="exports")

# 0

REQUEST_COUNT = Counter("http_requests_total","Total HTTP requests",["method","path","status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds","Request latency",["path"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    dur = time.time()-start
    try:
        REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
        REQUEST_LATENCY.labels(request.url.path).observe(dur)
    except Exception as e:
        print(f"Error in metrics middleware: {e}")
    return response

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/metrics/whoami", summary="Current identity/context")
async def whoami(request: Request):
    """Return the current request context.

    Includes:
    - `tenant_id` (from TenantContextMiddleware)
    - `user` (if present, else a placeholder)
    - `request_id` (if middleware supplies one)
    - server status summary
    """
    payload = await get_auth(request)
    tenant, workspace = inject_tenant_headers(request)
    return {"auth": bool(payload), "claims": payload or {}, "tenant": tenant, "workspace": workspace}
# ---- debug: list all registered routes (safe) ----
from fastapi import APIRouter
_debug_router = APIRouter(prefix="/metrics", tags=["metrics"])

@_debug_router.get("/_debug/routes", tags=["_debug"])
def _debug_routes():
    return [{"path": r.path, "name": r.name, "methods": list(getattr(r, "methods", []))} for r in app.router.routes]

if os.getenv("APP_ENV", "dev") != "prod":
    app.include_router(_debug_router)
#     app.include_router(_debug_router)

# ----------------------------------------------------------------------
# 🧭 Debug Router — lists all registered FastAPI routes
# ----------------------------------------------------------------------
from fastapi import APIRouter
_debug_router = APIRouter()

@_debug_router.get("/_debug/routes", tags=["_debug"])
def _debug_routes():
    """Return all registered route paths and methods."""
    return [
        {
            "path": route.path,
            "name": route.name,
            "methods": list(getattr(route, "methods", []))
        }
        for route in app.router.routes
    ]

if os.getenv("APP_ENV", "dev") != "prod":
    app.include_router(_debug_router)
#     app.include_router(_debug_router)

# normalized include for billing
# app.include_router(billing_router)

# normalized include for exports
# app.include_router(exports_router)

# normalized include for metrics
# app.include_router(metrics_router)

# normalized include for graphs
# app.include_router(graphs_router)

if os.getenv("APP_ENV", "dev") != "prod":
    app.include_router(_debug_router)

