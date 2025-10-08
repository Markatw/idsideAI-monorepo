from fastapi import APIRouter
router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/overview")
def overview():
    return {
        "users": 1,
        "workspaces": 1,
        "graphs": 0,
        "requests_24h": 0,
        "status": "ok"
    }
