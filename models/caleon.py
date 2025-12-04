from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models import Base

class ClusterNode(Base):
    __tablename__ = "cluster_node"

    id = Column(Integer, primary_key=True)
    label = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    @classmethod
    async def get_or_create(cls, db, label: str):
        from sqlalchemy import select
        stmt = select(cls).where(cls.label == label)
        result = await db.execute(stmt)
        node = result.scalar_one_or_none()
        if not node:
            node = cls(label=label)
            db.add(node)
            await db.flush()
        return node

class ClusterEdge(Base):
    __tablename__ = "cluster_edge"

    id = Column(Integer, primary_key=True)
    node_a_id = Column(Integer, ForeignKey('cluster_node.id'), nullable=False)
    node_b_id = Column(Integer, ForeignKey('cluster_node.id'), nullable=False)
    confidence = Column(Float, default=0.0)
    density = Column(Float, default=0.0)
    users = Column(JSON)  # Set of user IDs
    created_at = Column(DateTime, server_default=func.now())

    node_a = relationship("ClusterNode", foreign_keys=[node_a_id])
    node_b = relationship("ClusterNode", foreign_keys=[node_b_id])

    @classmethod
    async def get_or_create(cls, db, a_id: int, b_id: int):
        from sqlalchemy import select, and_
        # Ensure consistent ordering
        if a_id > b_id:
            a_id, b_id = b_id, a_id
        stmt = select(cls).where(and_(cls.node_a_id == a_id, cls.node_b_id == b_id))
        result = await db.execute(stmt)
        edge = result.scalar_one_or_none()
        if not edge:
            edge = cls(node_a_id=a_id, node_b_id=b_id, users=[])
            db.add(edge)
            await db.flush()
        return edge

    @classmethod
    async def fuse(cls, db, a_id: int, b_id: int, density: float, user_id: str):
        edge = await cls.get_or_create(db, a_id, b_id)
        edge.confidence = 1 - (1 - edge.confidence) * (1 - density)  # probabilistic OR
        if edge.users is None:
            edge.users = []
        if user_id not in edge.users:
            edge.users.append(user_id)
        await db.flush()
        return edge

    @property
    def cross_count(self) -> int:
        return len(self.users) if self.users else 0

class Predicate(Base):
    __tablename__ = "predicate"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    signature = Column(JSON)  # List of node labels
    confidence = Column(Float, default=0.0)
    definition = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    @classmethod
    async def get_or_create(cls, db, name: str, signature: list):
        from sqlalchemy import select
        stmt = select(cls).where(cls.name == name)
        result = await db.execute(stmt)
        pred = result.scalar_one_or_none()
        if not pred:
            pred = cls(name=name, signature=signature)
            db.add(pred)
            await db.flush()
            pred.fresh = True
        else:
            pred.fresh = False
        return pred

    def to_broadcast_dict(self) -> dict:
        return {
            "predicate_id": self.id,
            "name": self.name,
            "signature": self.signature,
            "confidence": self.confidence,
            "definition": self.definition,
            "created_at": self.created_at.isoformat(),
            "helix_version": "1.0.0"
        }