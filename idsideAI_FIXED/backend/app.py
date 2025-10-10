from fastapi import FastAPI, APIRouter

app = FastAPI(title="idsideAI Backend")

# ---- Tenant middleware (fallback-safe) ----
try:
    from backend.middleware.tenant import TenantContextMiddleware  # type: ignore
except Exception:
    class TenantContextMiddleware:  # type: ignore
        def __init__(self, app):
            self.app = app
        async def __call__(self, scope, receive, send):
            await self.app(scope, receive, send)

app.add_middleware(TenantContextMiddleware)

# ---- Graphs router (fallback-safe) ----
try:
    from backend.routers.graphs import router as graphs_router  # type: ignore
except Exception:
    graphs_router = APIRouter()

app.include_router(graphs_router, prefix="/graphs")

# ---- Health check ----
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
