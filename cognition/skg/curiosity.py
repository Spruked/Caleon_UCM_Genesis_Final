# cognition/skg/curiosity.py  (80 lines)
import threading, time, random
from collections import defaultdict
import networkx as nx

ENTROPY_THRESH = 0.75

def entropy(cluster):
    n = len(cluster)
    unknown = sum(1 for u, v in cluster if u == "UNKNOWN" or v == "UNKNOWN")
    return unknown / n if n else 0

def curiosity_loop(core, interval=30):
    while True:
        time.sleep(interval)
        # Check both level-0 and level-2 for knowledge gaps
        for level in [0, 2]:
            g = core.levels.get(level)
            if not g: continue
            
            # Look for UNKNOWN values in edges
            unknown_edges = []
            for u, v, data in g.edges(data=True):
                if 'UNKNOWN' in str(u) or 'UNKNOWN' in str(v):
                    unknown_edges.append((u, v, data))
            
            if unknown_edges:
                # Sample a random unknown edge and create a curiosity goal
                u, v, data = random.choice(unknown_edges)
                predicate = data.get('predicate', 'related_to')
                goal = {
                    "type": "web_search", 
                    "pattern": [str(u), predicate, str(v)],
                    "level": level,
                    "unknown_entity": str(u) if 'UNKNOWN' in str(u) else str(v)
                }
                # store in core's goals list
                if hasattr(core, 'curiosity_goals'):
                    core.curiosity_goals.append(goal)
                print(f"[Curiosity] spawned goal {goal}")
                
            # Also check for high-entropy clusters in level-2
            if level == 2 and g.number_of_nodes() > 3:
                try:
                    clusters = list(nx.connected_components(g.to_undirected()))
                    for c in clusters:
                        edges = [(u,v) for u,v in g.subgraph(c).edges()]
                        if len(edges) > 2 and entropy(edges) > ENTROPY_THRESH:
                            goal = {
                                "type": "cluster_analysis",
                                "pattern": f"dense_cluster_{abs(hash(tuple(sorted(c))))}"[:12],
                                "level": level,
                                "cluster_size": len(c)
                            }
                            if hasattr(core, 'curiosity_goals'):
                                core.curiosity_goals.append(goal)
                            print(f"[Curiosity] spawned cluster goal {goal}")
                except:
                    pass  # Skip if graph analysis fails

def start_curiosity(core):
    threading.Thread(target=curiosity_loop, args=(core,), daemon=True).start()

# Placeholder for Cali's goal API - replace with actual implementation
def cali_add_goal(goal):
    print(f"[Cali] Added goal: {goal}")
    # TODO: Integrate with actual Cali goal system