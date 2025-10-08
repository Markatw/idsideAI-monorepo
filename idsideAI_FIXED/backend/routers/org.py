from fastapi import APIRouter
router = APIRouter(prefix="/org", tags=["org"])

@router.post("/dev-seed")
def dev_seed():
    # minimal seed response for verification
    return {"ok": True, "seeded": True}
