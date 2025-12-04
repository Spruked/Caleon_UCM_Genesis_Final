from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from models import Base

class VaultLog(Base):
    __tablename__ = "vault_log"
    id = Column(Integer, primary_key=True)
    kind      = Column(String(50), index=True)   # cluster_ingest | predicate_invent
    payload   = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    @staticmethod
    async def log(db, kind: str, payload: dict):
        db.add(VaultLog(kind=kind, payload=payload))
        await db.flush()