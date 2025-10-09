from fastapi import APIRouter
from idsideai.services.telemetry import Telemetry
router = APIRouter(prefix="/telemetry", tags=["telemetry"])
@router.get("")
async def get_telemetry():
    return {"events": Telemetry.dump()}
