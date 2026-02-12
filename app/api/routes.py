# app/api/routes.py

from fastapi import APIRouter, HTTPException

from app.schemas import EmailRequest
from app.services.orchestrator import EmailOrchestrator

router = APIRouter()
orchestrator = EmailOrchestrator()


@router.post("/compose-and-send")
def compose_and_send(request: EmailRequest):
    try:
        result = orchestrator.compose_and_send(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok"}
