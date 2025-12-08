# cognition/skg/invent_predicate.py  (70 lines)
import networkx as nx
from networkx.algorithms import community
from collections import defaultdict

def maybe_invent_predicate(core, thresh=0.3):
    # Guard against missing levels or insufficient data
    if 2 not in core.levels or core.levels[2].number_of_edges() < 5:
        return

    g = core.levels[2]                      # meta-meta graph
    if g.number_of_edges() < 5: return
    # greedy modularity
    clusters = community.greedy_modularity_communities(g)
    for c in clusters:
        if len(c) < 2: continue
        density = nx.density(g.subgraph(c))
        if density > thresh:
            name = f"cluster_{abs(hash(tuple(sorted(c))))}"[:12]
            # inject back into K⁰ as a synthetic predicate
            core.add_triples([(name, "isA", "invented_predicate")])
            for n in c:
                core.add_triples([(n, "member_of", name)])
            print(f"[SKG] invented predicate  {name}  (density={density:.2f})")