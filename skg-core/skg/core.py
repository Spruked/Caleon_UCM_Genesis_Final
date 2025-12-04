import networkx as nx, torch, numpy as np
from torch_geometric.utils import dense_to_sparse
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch.nn as nn

# ----------  original minimal_skg helpers ----------
def build_base_kg(triples):
    g = nx.DiGraph()
    for s, p, o in triples:
        g.add_edge(s, o, predicate=p)
    return g

def reify_edges(g: nx.DiGraph):
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

class EdgeScoreGNN(nn.Module):
    def __init__(self, in_dim, hidden=16):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden)
        self.conv2 = GCNConv(hidden, 1)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        return self.conv2(x, edge_index).squeeze(-1)

def self_prune(skg: nx.Graph, scores: np.ndarray, thresh=0.1):
    remove = [i for i, s in enumerate(scores) if s < thresh]
    skg.remove_nodes_from(remove)
    return skg

# ----------  UCM service wrapper ----------
from .db import init_db, add_triple, query_pattern
class SKGService:
    def __init__(self, db_path=None):
        if db_path: os.environ["UCM_SKG_DB"] = db_path
        init_db()
    def add(self, s, p, o, w=1.0):
        add_triple(s, p, o, w)
        # optional: trigger recursion once > N edges
        if len(query_pattern([None, None, None], k=1_000_000)) > 500:
            self._recurse_once()
    def query(self, pat, k=10):
        return query_pattern(pat, k)
    def _recurse_once(self):
        rows = query_pattern([None, None, None], k=1_000_000)
        g = build_base_kg(rows)
        skg, _ = reify_edges(g)
        # dummy GNN prune (degree as target)
        A = nx.adjacency_matrix(skg).todense()
        edge_index, _ = dense_to_sparse(torch.tensor(A, dtype=torch.float))
        x = torch.eye(skg.number_of_nodes())
        model = EdgeScoreGNN(x.size(1))
        opt = torch.optim.Adam(model.parameters(), lr=0.01)
        for _ in range(200):
            opt.zero_grad()
            out = model(x, edge_index)
            loss = nn.MSELoss()(out, torch.tensor(list(dict(skg.degree()).values()), dtype=torch.float))
            loss.backward(); opt.step()
        with torch.no_grad():
            scores = model(x, edge_index).numpy()
        skg = self_prune(skg, scores, np.percentile(scores, 30))
        # write back new meta-triples (here we just log count)
        print(f"[SKG] recursion done – meta-nodes {skg.number_of_nodes()}")