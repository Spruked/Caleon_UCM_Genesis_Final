from fastapi import APIRouter

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("/status")
async def status():
    return {"UCM": "online", "bubble": "ready"}