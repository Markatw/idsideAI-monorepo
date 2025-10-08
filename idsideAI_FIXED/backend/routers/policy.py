from fastapi import APIRouter
router = APIRouter(prefix="/policy", tags=["policy"])

@router.get("/packs")
def list_packs():
    return {
        "packs": [
            {"id": "core", "name": "Core Policies", "count": 5},
            {"id": "security", "name": "Security Baseline", "count": 8},
        ]
    }
