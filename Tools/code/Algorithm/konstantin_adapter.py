# tools/konstantin_adapter.py
from __future__ import annotations
from typing import Tuple, List, Dict, Set, Iterable
import os, json, random, itertools
import networkx as nx

# 
from . import algorithms_local as kalg


# -----------------------
# JSON
# -------------------------------
def _load_graph(graph_json_path: str) -> Tuple[nx.DiGraph, List[Tuple[str, str]]]:
   # -------------------------------

    data = json.load(open(graph_json_path, "r"))
    G = nx.DiGraph()
    for n in data.get("nodes", []):
        G.add_node(n)

# -------------------------------

    for e in data.get("edges", []):
        u, v = e["src"], e["dst"]
        cap = e.get("capacity", 1)
        cost = e.get("cost", 1)
        G.add_edge(u, v, capacity=cap, cost=cost)

    starts = data.get("startNodes", [])
    target = data.get("target")
    constraints: List[Tuple[str, str]] = [(s, target) for s in starts if s in G and target in G]
    return G, constraints


# -------------------------------
#  Tools
# -------------------------------
def _edges_list(G: nx.DiGraph) -> Set[Tuple[str, str]]:
    return set((u, v) for u, v in G.edges())

def _remove_edges(G: nx.DiGraph, edges: Iterable[Tuple[str, str]]) -> None:
    for u, v in edges:
        if G.has_edge(u, v):
            G.remove_edge(u, v)

def _disconnects_all(G: nx.DiGraph, constraints: List[Tuple[str, str]]) -> bool:
    for s, t in constraints:
        if s in G and t in G and nx.has_path(G, s, t):
            return False
    return True

def _reachable_from_sources(G: nx.DiGraph, sources: List[str]) -> Set[str]:
    seen: Set[str] = set()
    for s in sources:
        if s not in G: 
            continue
        for node in nx.descendants(G, s) | {s}:
            seen.add(node)
    return seen

def _reachable_to_target(G: nx.DiGraph, target: str) -> Set[str]:
    if target not in G:
        return set()
    RG = G.reverse(copy=False)
    return nx.descendants(RG, target) | {target}


# -------------------------------
# Implementations
# -------------------------------
def _fast_min_cut_union(G: nx.DiGraph, constraints: List[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    """
    Remove Min-Cut (s-t min cut union):
    """
    removed: Set[Tuple[str, str]] = set()
    for s, t in constraints:
        if s not in G or t not in G:
            continue
        cut_val, (S, T) = nx.minimum_cut(G, s, t, capacity="capacity")
        for u, v in G.edges():
            if u in S and v in T:
                removed.add((u, v))
    return removed


def _bruteforce_min_multi_cut(G: nx.DiGraph, constraints: List[Tuple[str, str]], kmax: int = 3) -> Set[Tuple[str, str]]:
    """
    Brute Force 
    """
    starts = [s for s, _ in constraints]
    targets = list({t for _, t in constraints})
    G_nodes_from_s = _reachable_from_sources(G, starts)
    G_nodes_to_t = set()
    for t in targets:
        G_nodes_to_t |= _reachable_to_target(G, t)

    candidates = [(u, v) for (u, v) in G.edges() if (u in G_nodes_from_s and v in G_nodes_to_t)]
    candidates = list(dict.fromkeys(candidates))  #

    if _disconnects_all(G, constraints):
        return set()

    for k in range(1, kmax + 1):
        for combo in itertools.combinations(candidates, k):
            # تست
            H = G.copy()
            _remove_edges(H, combo)
            if _disconnects_all(H, constraints):
                return set(combo)

    return _fast_min_cut_union(G, constraints)


# -------------------------------
#Algorithm
# -------------------------------
_NAME_MAP = {
    # Algorithm names
    "remove random edge": "random_edge",
    "remove first edge" : "first_edge",
    "remove min-cut"    : "min_cut_union",
    "remove minmc"      : "minmc_union",
    "brute force"       : "bruteforce",

    # 
    "random_edge"         : "random_edge",
    "first_edge"          : "first_edge",
    "st_cut"              : "min_cut_union",
    "optimisation_approx" : "minmc_union",
    "bruteforce"          : "bruteforce",
    "matrix_bruteforce"   : "bruteforce",
    "disconnect"          : "disconnect",
}

def _normalize_algo_name(name: str) -> str:
    key = (name or "").strip().lower()
    if key not in _NAME_MAP:
        raise ValueError(f"Unknown algo '{name}'. Valid: {sorted(set(_NAME_MAP))}")
    return _NAME_MAP[key]


# -------------------------------
#  
# -------------------------------
def run_algorithm(graph_json_path: str, algo_name: str, out_dir: str) -> Dict:
    """
    """
    # 
    seed_env = os.getenv("PYTHONHASHSEED")
    if seed_env and seed_env.isdigit():
        random.seed(int(seed_env))
    else:
        random.seed(42)

    G, constraints = _load_graph(graph_json_path)
    before = _edges_list(G)

    norm = _normalize_algo_name(algo_name)

    #  Run Algorithms
    if norm == "disconnect":

    #
    # 
        G0 = G.copy()
        kalg.disconnect_the_source(G0, constraints)
        after = set(G0.edges())
        removed = sorted(before - after)

    elif norm == "random_edge":
        G0 = G.copy()
        kalg.remove_random_edge(G0, constraints)
        after = set(G0.edges())
        removed = sorted(before - after)

    elif norm == "first_edge":
        G0 = G.copy()
        kalg.remove_first_edge(G0, constraints)
        after = set(G0.edges())
        removed = sorted(before - after)

    elif norm == "min_cut_union":
        # NetworkX 
        rem = _fast_min_cut_union(G, constraints)
        removed = sorted(rem)

    elif norm == "minmc_union":


        rem = _fast_min_cut_union(G, constraints)
        removed = sorted(rem)

    elif norm == "bruteforce":
        kmax = int(os.getenv("KON_BF_KMAX", "3"))
        rem = _bruteforce_min_multi_cut(G, constraints, kmax=kmax)
        removed = sorted(rem)

    else:
        raise ValueError(f"Algorithm '{algo_name}' is mapped to unknown key '{norm}'")

    result = {
        "algo": algo_name,
        "removed_count": len(removed),
        "removed": [[u, v] for (u, v) in removed],
    }
    return result

