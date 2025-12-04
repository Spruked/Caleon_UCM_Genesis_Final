"""
Unified Cognition Module  –  SKG-backed knowledge store
(drop-in replacement; old API unchanged)
"""
from .skg.core import SKGCore

class KnowledgeStore:
    __slots__ = ("_skg",)
    def __init__(self, db_path=None):
        self._skg = SKGCore()
    def tell(self, sub, pred, obj, confidence=1.0):
        self._skg.add_triples([(sub, pred, obj)])
        self._skg.expand_recursive()
    def ask(self, pattern, top_k=10):
        # pattern = [sub,pred,obj]  None = wildcard
        g = self._skg.levels.get(0)
        if not g:
            return []
        match = [(u,v,d) for u,v,d in g.edges(data=True)
                 if (pattern[0] is None or u==pattern[0]) and
                    (pattern[1] is None or d.get("predicate")==pattern[1]) and
                    (pattern[2] is None or v==pattern[2])]
        return match[:top_k]
    def snapshot(self):
        # future: git-like commit hash
        pass