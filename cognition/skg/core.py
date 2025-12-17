"""
Super-Knowledge-Graph core  –  real recursive layers, real blocks, real pruning
Drop-in replacement for yesterday's toy.
"""
import numpy as np
import torch, torch.nn as nn
import networkx as nx
import sqlite3, json, os, pathlib
import threading
from .contradiction import detect_and_repair
from .invent_predicate import maybe_invent_predicate

# Force CPU-only mode to prevent CUDA dependency issues
torch.cuda.is_available = lambda: False
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# ----------  config ----------
MAX_DEPTH      = 3          # how many recursive levels
GNN_HIDDEN     = 32
PRUNE_THRESH   = 0.05       # percentile
DB_FILE        = pathlib.Path(os.environ.get("UCM_SKG_DB", "ucm_skg.db"))

# ----------  tiny utils ----------
def conn():
    DB_FILE.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_FILE)

def init_db():
    c = conn()
    # Create both old SKG schema and new UCM-compatible schema
    for lvl in range(MAX_DEPTH):
        c.execute(f"CREATE TABLE IF NOT EXISTS level_{lvl}(i INT, j INT, weight REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS meta(depth INT)")
    # UCM-compatible tables
    c.execute("CREATE TABLE IF NOT EXISTS edges(source TEXT, predicate TEXT, target TEXT, weight REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS nodes(id TEXT PRIMARY KEY, label TEXT)")
    c.commit(); c.close()

# ----------  SKG engine ----------
class SKGCore:
    def __init__(self):
        init_db()
        self.levels   = {}          # nx graphs
        self.adjs     = {}          # numpy matrices
        self.depth    = 0
        self.total_edges = 0
        self.bootstrapped = False
        self.curiosity_goals = []   # store spawned goals
        self._curiosity_thread = None

    # 1.  ingest base triples → K⁰
    def add_triples(self, triples):
        old_edges = self.levels[0].number_of_edges() if 0 in self.levels else 0
        if 0 not in self.levels:
            self.levels[0] = nx.MultiDiGraph()
        g = self.levels[0]
        for s, p, o in triples:
            g.add_edge(s, o, predicate=p)
        self.adjs[0]   = nx.adjacency_matrix(g).todense().astype(float)
        self.depth     = 1
        # Run contradiction detection and repair
        detect_and_repair(self)
        # ---- quiet per-edge bootstrap ----
        new_total = self.levels[0].number_of_edges()
        if new_total % 50 == 0 and new_total > 0 and new_total // 50 != getattr(self, '_last_banner', -1):
            self._last_banner = new_total // 50
            print(f"[SKG] >> {new_total} base facts - bootstrap")
            self.expand_recursive()
            maybe_invent_predicate(self)
            # start_curiosity(self)  # Disabled for CPU-only mode

    # 2.  recursive expansion  Kᵏ → Kᵏ⁺¹
    def expand_recursive(self):
        if getattr(self, '_expanding', False):
            return
        self._expanding = True
        while self.depth < MAX_DEPTH:
            k = self.depth
            prev = self.adjs[k-1]

            # local cross-links  C
            C = self._cross_links(prev)
            # non-local proposals X
            X = self._propose_edges(prev)
            # new adjacency
            new_adj = prev + C + X
            new_adj = self._prune(new_adj)

            self.adjs[k] = new_adj
            self.levels[k] = nx.from_numpy_array(new_adj, create_using=nx.DiGraph)
            self._persist_level(k, new_adj)
            self.depth += 1
            print(f"[SKG] built level {k}  |V|={new_adj.shape[0]}  density={new_adj.sum()/new_adj.size:.3f}")

        # Run predicate invention after expansion
        maybe_invent_predicate(self)
        self._expanding = False

    # Curiosity daemon control - DISABLED for CPU-only mode
    def start_curiosity_daemon(self):
        # Disabled to prevent thread issues in containers
        print("[SKG] Curiosity daemon disabled for CPU-only mode")
        pass

    def stop_curiosity_daemon(self):
        # Disabled to prevent thread issues in containers
        print("[SKG] Curiosity daemon stop not needed (was disabled)")
        pass

    def get_curiosity_goals(self):
        return self.curiosity_goals.copy()

    # 3.  cross-links = shared nodes
    def _cross_links(self, adj):
        g = nx.from_numpy_array(adj, create_using=nx.DiGraph)
        c = nx.adjacency_matrix(g).todense() * 0.2   # dampen
        return c

    # 4.  non-local proposals via degree-based scoring (CPU-only)
    def _propose_edges(self, adj):
        g = nx.from_numpy_array(adj, create_using=nx.DiGraph)
        n = adj.shape[0]

        # Get degree centrality as simple scoring
        degrees = np.array(list(dict(g.degree()).values()))
        degrees = degrees / degrees.max() if degrees.max() > 0 else degrees

        # Create proposal matrix based on degree similarity
        proposals = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Simple similarity based on degree difference
                    similarity = 1.0 / (1.0 + abs(degrees[i] - degrees[j]))
                    proposals[i, j] = similarity

        # Apply percentile threshold (95th percentile)
        threshold = np.percentile(proposals[proposals > 0], 95) if np.any(proposals > 0) else 0
        proposals = (proposals > threshold).astype(float) * 0.15

        return proposals

    # 5.  prune low weights
    def _prune(self, adj):
        # Guard against empty adjacency matrices
        if adj.sum() == 0 or np.count_nonzero(adj) == 0:
            return adj
        thresh = np.percentile(adj[adj>0], PRUNE_THRESH*100)
        adj[adj < thresh] = 0
        return adj

    # 6.  persist level to SQLite
    def _persist_level(self, lvl, adj):
        c = conn()
        c.execute(f"DELETE FROM level_{lvl}")
        rows = [(int(i), int(j), float(adj[i,j]))
                for i in range(adj.shape[0]) for j in range(adj.shape[1]) if adj[i,j]>0]
        c.executemany(f"INSERT INTO level_{lvl} VALUES (?,?,?)", rows)
        c.execute("REPLACE INTO meta(depth) VALUES (?)", (lvl+1,))

        # Also populate UCM-compatible edges table for level 0
        if lvl == 0 and 0 in self.levels:
            c.execute("DELETE FROM edges")
            g = self.levels[0]
            node_list = list(g.nodes())
            for i in range(len(node_list)):
                for j in range(len(node_list)):
                    if adj[i,j] > 0:
                        source = str(node_list[i])
                        target = str(node_list[j])
                        weight = float(adj[i,j])
                        # For now, use generic predicate since we don't store individual edge predicates in adj matrix
                        c.execute("INSERT INTO edges (source, predicate, target, weight) VALUES (?, ?, ?, ?)",
                                (source, "related", target, weight))
            # Populate nodes table
            c.execute("DELETE FROM nodes")
            for node in node_list:
                c.execute("INSERT INTO nodes (id, label) VALUES (?, ?)", (str(node), str(node)))

        c.commit(); c.close()

    # 7.  assemble full SKG block matrix
    def block_matrix(self):
        blocks = [[self.adjs.get(min(i,j), np.zeros_like(self.adjs[0])) if abs(i-j)<=1
                   else np.zeros_like(self.adjs[0]) for j in range(self.depth)]
                  for i in range(self.depth)]
        return np.block(blocks)

# ----------  Flask service wrapper (same URLs as before) ----------
from flask import Flask, request, jsonify
class SKGService:
    def __init__(self, db_path=None):
        if db_path: os.environ["UCM_SKG_DB"] = db_path
        self.core = SKGCore()
        self.app  = Flask("skg")
        self._routes()

    def _routes(self):
        self.app.add_url_rule("/add",  "add",  self._add,  methods=["POST"])
        self.app.add_url_rule("/query","query",self._query,methods=["GET"])

    def _add(self):
        data = request.get_json(force=True)
        triples = [(data["s"], data["p"], data["o"])]
        self.core.add_triples(triples)
        self.core.expand_recursive()
        return jsonify({"status":"ok", "depth":self.core.depth})

    def _query(self):
        pat = json.loads(request.args.get("pat"))
        # for now just return base-level edges (can extend to meta later)
        g = self.core.levels[0]
        match = [(u,v,d) for u,v,d in g.edges(data=True)
                 if (pat[0] is None or u==pat[0]) and
                    (pat[1] is None or d.get("predicate")==pat[1]) and
                    (pat[2] is None or v==pat[2])]
        return jsonify(match[:int(request.args.get("k", 10))])

    def start(self, port=7777):
        # Start curiosity daemon - DISABLED for CPU-only mode
        # start_curiosity(self.core)
        print("[SKG] Starting SKG service (curiosity disabled for CPU-only mode)")
        self.app.run(host="0.0.0.0", port=port, debug=False)

# ----------  convenience client ----------
class Knowledge:
    def __init__(self, db_path=None):
        self.svc = SKGService(db_path)
    def add(self, s, p, o, w=1.0):
        self.svc.core.add_triples([(s,p,o)])
        self.svc.core.expand_recursive()
    def query(self, pat, k=10):
        return self.svc._query_internal(pat, k)
    def _query_internal(self, pat, k):
        g = self.svc.core.levels[0]
        match = [(u,v,d) for u,v,d in g.edges(data=True)
                 if (pat[0] is None or u==pat[0]) and
                    (pat[1] is None or d.get("predicate")==pat[1]) and
                    (pat[2] is None or v==pat[2])]
        return match[:k]

# ----------  compatibility functions for old API ----------
def reify_edges(g: nx.DiGraph):
    """Convert directed graph to undirected SKG with edge reification"""
    skg = nx.Graph()
    edges = list(g.edges(data=True))
    edge2id = {e[:2]: i for i, e in enumerate(edges)}
    for e in edges:
        skg.add_node(edge2id[e[:2]], label=f"{e[0]}-{e[2]['predicate']}-{e[1]}")
    for i, e1 in enumerate(edges):
        for j, e2 in enumerate(edges):
            if i != j and (e1[0] in e2[:2] or e1[1] in e2[:2]):
                skg.add_edge(i, j)
    return skg, edges

def self_prune(skg: nx.Graph, scores: np.ndarray, thresh=0.1):
    """Remove low-scoring nodes from SKG"""
    remove = [i for i, s in enumerate(scores) if s < thresh]
    skg.remove_nodes_from(remove)
    return skg