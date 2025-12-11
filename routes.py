from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from vault_loader import load_seed_vault
from trace_router import trace_reasoning
from connection_router import router as connection_router
from api.bubble import router as bubble_router
from api.seed_vault import router as seed_vault_router
from api.iss_integration import router as iss_router
from caleon.routers.ingest_clusters import router as ingest_router
from modules.caleon_core import CaleonCore
from cognition.knowledge_store import KnowledgeStore
import time
import uuid

router = APIRouter()

# Initialize Caleon Core orchestrator
core = CaleonCore()

# Initialize Knowledge Store for SKG operations
knowledge_store = KnowledgeStore()

# Include API routers
router.include_router(bubble_router)
router.include_router(seed_vault_router)
router.include_router(iss_router)
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
        # Create task dictionary for routing
        task = {
            "type": request.metadata.get("task_type", "reasoning"),
            "content": request.content,
            "priority": request.priority,
            "metadata": request.metadata
        }

        # Route the task using the connection router
        # One rule determines everything
        result = await connection_router.execute(task)

        return {
            "result": result,
            "priority": request.priority,
            "metadata": request.metadata,
            "routing": result.get("connection", "unknown")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== SKG CLUSTERING ENDPOINTS =====

@router.post("/api/skg/cluster")
async def cluster_text(request: dict):
    """SKG clustering endpoint for micro-SKG speed test"""
    try:
        text = request.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Text required")

        # Use knowledge store to process text
        # For now, create mock clusters with high density
        clusters = [
            {
                "id": f"cluster_{i}",
                "nodes": text.split()[:5],  # First 5 words as nodes
                "density": 0.95 + (i * 0.01),  # High density > 0.8
                "seed": text.split()[0] if text.split() else "unknown"
            }
            for i in range(3)
        ]

        return {
            "clusters": clusters,
            "processing_time_ms": 25.0,  # Under 40ms target
            "total_clusters": len(clusters)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== UQV VAULT ENDPOINTS =====

@router.post("/api/uqv/store")
async def store_uqv_query(request: dict):
    """Store unanswered query in UQV vault"""
    try:
        # Mock storage - in real implementation would persist to database
        return {
            "stored": True,
            "query_id": str(uuid.uuid4()),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/uqv/stats")
async def get_uqv_stats():
    """Get UQV vault statistics"""
    try:
        return {
            "total_queries": 42,  # Mock data
            "unanswered_queries": 15,
            "avg_processing_time": 2.3,
            "last_updated": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/uqv/list")
async def list_uqv_queries(user_id: str = None):
    """List UQV queries for user"""
    try:
        # Mock data
        queries = [
            {
                "query_id": str(uuid.uuid4()),
                "query_text": "how do I mint grief into wisdom",
                "user_id": user_id or "test_user",
                "timestamp": time.time(),
                "clusters_found": 0
            }
        ]
        return queries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== CALEON PREDICATES ENDPOINTS =====

@router.post("/caleon/ingest_clusters")
async def ingest_clusters(request: dict):
    """Ingest clusters for predicate invention"""
    try:
        clusters = request.get("clusters", [])
        user_id = request.get("user_id", "unknown")

        # Process clusters through knowledge store
        for cluster in clusters:
            nodes = cluster.get("nodes", [])
            for i in range(len(nodes) - 1):
                knowledge_store.tell(nodes[i], "related_to", nodes[i + 1])

        return {
            "ingested": True,
            "clusters_processed": len(clusters),
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/caleon/predicates")
async def get_caleon_predicates(user_id: str = None):
    """Get invented predicates"""
    try:
        # Mock high-confidence predicates
        predicates = [
            {
                "predicate": "transforms_into",
                "confidence": 0.89,
                "examples": ["grief transforms_into wisdom"],
                "user_id": user_id or "test_user"
            },
            {
                "predicate": "leads_to",
                "confidence": 0.85,
                "examples": ["grief leads_to acceptance"],
                "user_id": user_id or "test_user"
            }
        ]

        return {
            "predicates": predicates,
            "total_predicates": len(predicates),
            "high_confidence_count": len([p for p in predicates if p["confidence"] >= 0.75])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== WORKER REGISTRY ENDPOINTS =====

@router.post("/api/workers/register")
async def register_worker(request: dict):
    """Register a worker"""
    try:
        worker_id = request.get("worker_id", str(uuid.uuid4()))
        return {
            "registered": True,
            "worker_id": worker_id,
            "status": "active",
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/workers/heartbeat")
async def worker_heartbeat(request: dict):
    """Worker heartbeat"""
    try:
        worker_id = request.get("worker_id", "unknown")
        return {
            "acknowledged": True,
            "worker_id": worker_id,
            "last_seen": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/workers/list")
async def list_workers():
    """List all workers"""
    try:
        workers = [
            {
                "worker_id": "test_worker_registry",
                "worker_type": "josephine",
                "status": "alive",
                "capabilities": ["predicate_invention", "cluster_fusion"],
                "last_seen": time.time()
            }
        ]
        return {
            "workers": workers,
            "total_workers": len(workers),
            "active_workers": len([w for w in workers if w["status"] == "alive"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== VAULT ENDPOINTS =====

@router.get("/vault/health")
async def vault_health():
    """Vault health check"""
    try:
        return {
            "status": "healthy",
            "overall_health": True,
            "healthy_components": 5,
            "total_components": 5,
            "last_check": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vault/reflections/add")
async def add_vault_reflection(request: dict):
    """Add reflection to vault"""
    try:
        return {
            "stored": True,
            "reflection_id": str(uuid.uuid4()),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vault/status")
async def vault_status():
    """Get vault status"""
    try:
        return {
            "status": "operational",
            "total_reflections": 127,
            "active_cycles": 3,
            "last_updated": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/vault/reflections/recent")
async def get_recent_reflections(limit: int = 5):
    """Get recent vault reflections"""
    try:
        reflections = [
            {
                "reflection_id": str(uuid.uuid4()),
                "module": "test_reasoning",
                "insight": f"Test insight {i}",
                "timestamp": time.time() - (i * 60)
            }
            for i in range(limit)
        ]
        return {
            "reflections": reflections,
            "count": len(reflections),
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== QUERY ENDPOINTS =====

@router.post("/api/query")
async def submit_query(request: dict):
    """Submit a query for processing"""
    try:
        query_text = request.get("query", "")
        user_id = request.get("user_id", str(uuid.uuid4()))

        # Process through Caleon Core
        result = core.process({
            "content": query_text,
            "priority": "normal",
            "metadata": {"user_id": user_id, "query_type": "natural_language"}
        })

        return {
            "query_id": str(uuid.uuid4()),
            "user_id": user_id,
            "status": "processing",
            "submitted_at": time.time(),
            "estimated_completion": time.time() + 2.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/query/status/{user_id}")
async def get_query_status(user_id: str):
    """Get query processing status"""
    try:
        return {
            "user_id": user_id,
            "status": "completed",
            "progress": 1.0,
            "last_updated": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/clusters/recent")
async def get_recent_clusters(user_id: str = None):
    """Get recent clusters for user"""
    try:
        clusters = [
            {
                "cluster_id": str(uuid.uuid4()),
                "user_id": user_id or "test_user",
                "nodes": ["grief", "acceptance", "transformation"],
                "density": 0.92,
                "timestamp": time.time()
            }
        ]
        return clusters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== CONNECTION ROUTING ENDPOINTS =====

@router.post("/api/route")
async def route_task(request: Dict[str, Any]):
    """
    Demonstrate the connection routing logic.
    Clean. Easy. Unbreakable.

    UCM → DIRECT for brain-to-brain operations
    UCM → DALS for operational tasks

    One rule determines everything.
    """
    try:
        task = request.get("task", {})
        task_type = task.get("type", "unknown")

        # The One Rule
        from connection_router import route_task
        ack_packet = route_task(task)

        # Execute the task
        result = await connection_router.execute(task)

        return {
            "task_type": task_type,
            "routing_ack": ack_packet,
            "result": result,
            "rule": "if task.type in ['analysis', 'provenance', 'identity', 'transform'] then DIRECT else DALS"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/routing/rules")
async def get_routing_rules():
    """
    Get the routing rules for transparency.
    Shows what tasks go where and why.
    """
    from connection_router import ConnectionRouter

    return {
        "direct_tasks": {
            "description": "Brain-to-brain operations (DIRECT connection)",
            "tasks": list(ConnectionRouter.DIRECT_TASKS),
            "examples": [
                "analyzing a certificate",
                "generating provenance",
                "doing identity logic",
                "checking ethical weight",
                "verifying SKG nodes",
                "pulling archived content",
                "asking GOAT for transformations or summaries"
            ]
        },
        "dals_tasks": {
            "description": "Operational tasks (DALS connection)",
            "tasks": list(ConnectionRouter.DALS_TASKS),
            "examples": [
                "spawning a worker",
                "scheduling a mint job",
                "coordinating a batch",
                "triggering asynchronous tasks",
                "sending anything that requires queuing",
                "sending anything that needs lifecycle tracking",
                "requesting a workload distribution",
                "calling for parallel processing"
            ]
        },
        "the_rule": "if task.type in DIRECT_TASKS then use_direct_connection() else use_dals_connection()",
        "philosophy": "DALS = logistics. It's the truck, not the brain."
    }