# skg/contradiction.py  –  final version (Dec 2025)

from typing import Dict, Any

OPPOSITES = {
    "loves": "hates",
    "hates": "loves",
    "friend": "enemy",
    "enemy": "friend",
    "alive": "dead",
    "dead": "alive",
    "in": "out",
    "out": "in",
}

def detect_and_repair(core) -> None:
    """
    Called after every add_triples(). Repairs mutual-exclusion contradictions.
    Works with current SKG Pentagon core data layout.
    """
    # Guard against empty graphs
    if 0 not in core.levels or core.levels[0].number_of_edges() == 0:
        return

    g = core.levels[0]  # base level DiGraph
    removed = 0

    # Build quick lookup: (subject, object) → list of (predicate, weight, key)
    candidates: Dict[tuple, list] = {}
    for u, v, data in g.edges(data=True):
        key = (u, v)
        pred = data.get("predicate")
        if pred and pred in OPPOSITES:
            candidates.setdefault(key, []).append((pred, data.get("weight", 1.0), (u, v)))

    for (s, o), entries in candidates.items():
        # See if we have both sides of any opposite pair
        seen = {pred for pred, _, _ in entries}
        for pred in seen:
            if OPPOSITES[pred] in seen:
                # Contradiction! Keep the highest-confidence one
                entries.sort(key=lambda x: x[1], reverse=True)  # highest weight first
                winner_pred, winner_weight, _ = entries[0]
                for loser_pred, _, edge_key in entries[1:]:
                    if g.has_edge(*edge_key):
                        g.remove_edge(*edge_key)
                        removed += 1
                # Update winner with the best weight
                g[s][o]["predicate"] = winner_pred
                g[s][o]["weight"] = winner_weight
                print(f"[SKG] repaired contradiction {loser_pred} → kept {winner_pred} ({s} → {o})")
                break  # only one repair per (s,o) pair

    if removed:
        print(f"[SKG] total contradictions repaired: {removed}")