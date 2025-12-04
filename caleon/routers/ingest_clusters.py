"""
/caleon/ingest_clusters
Helix-safe, vault-audited, zero side-effects.
Only writes to approved tables: ClusterNode, ClusterEdge, Predicate, VaultLog.
"""
from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Annotated
import uuid, time, aiohttp, os
from sqlalchemy.ext.asyncio import AsyncSession
from deps import get_caleon_db, get_vault_db
from models.caleon import ClusterNode, ClusterEdge, Predicate
from models.vault import VaultLog               # audit trail

router = APIRouter(prefix="/caleon", tags=["ingest"])

WORKER_BROADCAST = os.getenv("WORKER_BROADCAST", "http://localhost:9999/broadcast")
HELIX_VERSION    = os.getenv("HELIX_VERSION", "1.0.0")   # immutable core marker

class ClusterIn(BaseModel):
    id: str
    nodes: Annotated[List[str], Field(min_items=2)]
    density: float = Field(ge=0.0, le=1.0)
    seed: str

class IngestRequest(BaseModel):
    user_id: str
    worker: str
    clusters: List[ClusterIn]
    timestamp: float = Field(default_factory=time.time)
    helix_version: str = HELIX_VERSION        # safety checksum


# ---------- core route ----------
@router.post("/ingest_clusters", response_model=Dict[str, Any])
async def ingest_clusters(
    body: IngestRequest,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_caleon_db),
    vdb: AsyncSession = Depends(get_vault_db)
):
    if body.helix_version != HELIX_VERSION:
        raise ValueError("Helix version mismatch – core immutable.")

    new_pred_queue = []
    for clus in body.clusters:
        cluster_hash = "|".join(sorted(clus.nodes))
        node_objs = [await ClusterNode.get_or_create(db, lbl) for lbl in clus.nodes]

        # audit log (vault)
        await VaultLog.log(vdb, kind="cluster_ingest", payload={
            "user_id": body.user_id, "worker": body.worker,
            "cluster_hash": cluster_hash, "density": clus.density
        })

        # edge fusion + predicate invention
        for i in range(len(node_objs)):
            for j in range(i+1, len(node_objs)):
                u, v = node_objs[i], node_objs[j]
                edge = await ClusterEdge.fuse(db, u.id, v.id, clus.density, body.user_id)

                if edge.cross_count >= 3 and edge.confidence < 0.95:
                    pred_name = _invent_predicate(u.label, v.label, edge)
                    pred = await Predicate.get_or_create(db, pred_name, [u.label, v.label])
                    if pred.fresh:
                        new_pred_queue.append(pred)

    if new_pred_queue:
        background.add_task(_broadcast_to_workers, new_pred_queue)

    return {"status": "ok", "new_predicates": len(new_pred_queue), "helix_safe": True}


# ---------- invention (immutable rules) ----------
def _invent_predicate(a: str, b: str, edge: ClusterEdge) -> str:
    if edge.density >= 0.98: return "entails"
    if _is_cross_domain(a, b): return "relies_on"
    if _is_contradiction(a, b): return "contradicts"
    return "co_occurs_strong"


def _is_cross_domain(a: str, b: str) -> bool:
    domains = {
        "emotion": {"grief", "joy", "anger", "fear"},
        "logic":   {"axiom", "proof", "theorem"},
        "physics": {"force", "mass", "energy"},
        "narrative": {"conflict", "resolution", "climax"}
    }
    a_dom = next((k for k, v in domains.items() if a in v), None)
    b_dom = next((k for k, v in domains.items() if b in v), None)
    return a_dom != b_dom and None not in (a_dom, b_dom)


def _is_contradiction(a: str, b: str) -> bool:
    pairs = {tuple(sorted((a, b))) for a, b in [
        ("success", "failure"), ("love", "hate"), ("truth", "lie"),
        ("forgiveness", "revenge"), ("freedom", "oppression")
    ]}
    return tuple(sorted((a, b))) in pairs


# ---------- broadcast ----------
async def _broadcast_to_workers(preds: List[Predicate]):
    payload = [p.to_broadcast_dict() for p in preds]
    async with aiohttp.ClientSession() as sess:
        await sess.post(WORKER_BROADCAST, json=payload, timeout=1.5)