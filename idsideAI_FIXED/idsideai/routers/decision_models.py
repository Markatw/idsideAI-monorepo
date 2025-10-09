from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from idsideai.services.dsl import parse_sdl, DecisionModelSpec
from idsideai.services.engine import run_model
router = APIRouter(prefix="/decision-models", tags=["decision-models"])
class RunRequest(BaseModel):
    sdl_text: str
    inputs: dict = {}

@router.post("/run")
async def run_decision_model(
        req: RunRequest = Body(
            ...,
            example={
                "sdl_text": """name: demo
    steps:
        - id: s1
        type: prompt
        prompt: "Echo: {text}"
    """,
                "inputs": {"text": "Hello"},
            },
        )
):

    try:
        spec: DecisionModelSpec = parse_sdl(req.sdl_text)
    except Exception as e:
        raise HTTPException(400, f"SDL parse error: {e}")
    try:
        result = await run_model(spec, req.inputs)
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Missing input: {e.args[0]}")
    except Exception:
        raise HTTPException(status_code=500, detail="Execution error")
    return result
