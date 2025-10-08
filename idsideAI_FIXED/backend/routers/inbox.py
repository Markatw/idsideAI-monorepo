from fastapi import APIRouter
router = APIRouter(prefix="/inbox", tags=["inbox"])

@router.get("")
def list_inbox():
    return {"items": [], "next": None}
