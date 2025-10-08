from fastapi import APIRouter
router = APIRouter(prefix="/compose", tags=["compose"])

@router.get("/schema")
def compose_schema():
    return {
        "fields": [
            {"name": "to", "type": "string", "required": True},
            {"name": "subject", "type": "string"},
            {"name": "body", "type": "string"},
        ]
    }
