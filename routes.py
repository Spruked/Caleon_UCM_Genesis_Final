from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from vault_loader import load_seed_vault
from trace_router import trace_reasoning
from api.bubble import router as bubble_router
from api.seed_vault import router as seed_vault_router
from caleon.routers.ingest_clusters import router as ingest_router

router = APIRouter()

# Include API routers
router.include_router(bubble_router)
router.include_router(seed_vault_router)
router.include_router(ingest_router)

class ReasonRequest(BaseModel):
    content: str
    priority: str
    metadata: Dict[str, Any]

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "Unified Cognition Module"}

@router.post("/reason")
async def reason(request: ReasonRequest):
    try:
        # Load seed vault
        seed_vault = load_seed_vault()

        # Perform reasoning (placeholder logic)
        response = await trace_reasoning(request.content, request.priority, request.metadata, seed_vault)

        return {"result": response, "priority": request.priority, "metadata": request.metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))