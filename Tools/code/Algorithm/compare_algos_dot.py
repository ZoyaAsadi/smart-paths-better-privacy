# tools/compare_algos_dot.py
# Compare multiple removal algorithms on a DOT graph (G0.dot) and report counts & diffs.
# Outputs:
#   artefacts/results/G0_alg_eval.csv
#   artefacts/results/G0_alg_eval.md
#   artefacts/graphs/G1_<Algo>.dot + .png (pruned graphs after removals)

import argparse, os, random, csv, itertools, pathlib
import pydot, networkx as nx
from networkx.drawing.nx_pydot import from_pydot, to_pydot

# ---------- I/O ----------
def load_dot_to_digraph(dot_path: str) -> nx.DiGraph:
    pd = pydot.graph_from_dot_file(dot_path)[0]
    MG = from_pydot(pd)
    # Coerce to simple DiGraph (ignore parallel edges)
    G = nx.DiGraph()
    for u, v in MG.edges():
        G.add_edge(str(u), str(v))
    # normalize node labels to str
    _ = [str(n) for n in G.nodes()]
    return G

def write_graph_dot_png(G: nx.DiGraph, dot_path: pathlib.Path):
    dot_path.parent.mkdir(parents=True, exist_ok=True)
    to_pydot(G).write_raw(str(dot_path))
    # try PNG if graphviz is available
    png_path = dot_path.with_suffix(".png")
    try:
        import subprocess, shutil
        if shutil.which("dot"):
            subprocess.check_call(["dot", "-Tpng", str(dot_path), "-o", str(png_path)])
    except Exception:
        pass

# ---------- Constraints autodetect ----------
DEFAULT_PAGES = {
    "Home","Discover","SearchBooks","Audiobooks","DigitalMag",
    "Membership","ContactUs","Login"
}
DEFAULT_SERVICES = {
    "SecuritySvc","AnalyticsSvc","ExtMediaSvc",
    "SupportSvc","PaymentsSvc","PersonalSvc"
}

def autodetect_sets(G: nx.DiGraph):
    starts = [n for n in G.nodes() if n in DEFAULT_PAGES]
    services = [n for n in G.nodes() if n in DEFAULT_SERVICES]
    if not starts:
        # fallback: any node with out-degree > 0 and name looks like a page
        starts = [n for n in G.nodes() if G.out_degree(n) > 0 and n[0].isupper()]
    if not services:
        services = [n for n in G.nodes() if n.endswith("Svc")]
    return starts, services

def build_constraints(G: nx.DiGraph, starts, services):
    # all page→service pairs (multi-target multi-source)
    return [(s, t) for s in starts for t in services if s in G and t in G]

# ---------- Utility ----------
def any_reachable_pair(G: nx.DiGraph, constraints):
    for s, t in constraints:
        try:
            if nx.has_path(G, s, t):
                return s, t
        except nx.NetworkXError:
            continue
    return None

# ---------- Algorithms (edge sets to remove) ----------

def algo_remove_random_edge(G: nx.DiGraph, constraints, seed=0):
    rnd = random.Random(seed)
    H = G.copy()
    removed = set()
    while True:
        pair = any_reachable_pair(H, constraints)
        if not pair: break
        s, t = pair
        try:
            path = nx.shortest_path(H, s, t)
        except nx.NetworkXNoPath:
            continue
        if len(path) < 2:  # nothing to remove
            break
        i = rnd.randrange(len(path) - 1)
        e = (path[i], path[i+1])
        if H.has_edge(*e):
            H.remove_edge(*e)
            removed.add(e)
    return removed

def algo_remove_first_edge(G: nx.DiGraph, constraints):
    # For each reachable (s,t), remove the first edge on ONE shortest s→t path
    removed = set()
    for s, t in constraints:
        try:
            path = nx.shortest_path(G, s, t)
        except nx.NetworkXNoPath:
            continue
        if len(path) >= 2:
            e = (path[0], path[1])
            removed.add(e)
    return removed

def algo_remove_min_cut_union(G: nx.DiGraph, constraints):
    # union of minimum edge cuts for each (s,t)
    removed = set()
    for s, t in constraints:
        try:
            cut = nx.minimum_edge_cut(G, s, t)  # capacity-less (structural)
        except (nx.NetworkXNoPath, nx.NetworkXError):
            continue
        removed.update(cut)
    return removed

def algo_remove_minmc_greedy(G: nx.DiGraph, constraints):
    # Greedy "multi-cut": iteratively remove the single edge that appears most
    # frequently across current pairwise min-cuts, until all pairs are disconnected.
    H = G.copy()
    removed = set()
    while True:
        # collect pairwise cuts for reachable pairs
        freq = {}
        reachable = False
        for s, t in constraints:
            try:
                if not nx.has_path(H, s, t):
                    continue
                reachable = True
                cut = nx.minimum_edge_cut(H, s, t)
                for e in cut:
                    freq[e] = freq.get(e, 0) + 1
            except (nx.NetworkXNoPath, nx.NetworkXError):
                continue
        if not reachable:
            break
        if not freq:
            # fallback: break a random reachable path
            s, t = any_reachable_pair(H, constraints)
            if not (s and t): break
            path = nx.shortest_path(H, s, t)
            e = (path[0], path[1])
            if H.has_edge(*e):
                H.remove_edge(*e); removed.add(e)
            continue
        # choose the most frequent edge
        e_star = max(freq, key=freq.get)
        if H.has_edge(*e_star):
            H.remove_edge(*e_star)
            removed.add(e_star)
        else:
            break
    return removed

def algo_bruteforce_min_hitset(G: nx.DiGraph, constraints, kmax=4):
    # Find the smallest set of edges (|E'|<=kmax) whose removal disconnects all (s,t)
    E = list(G.edges())
    for k in range(1, kmax+1):
        for combo in itertools.combinations(E, k):
            H = G.copy()
            H.remove_edges_from(combo)
            ok = True
            for s, t in constraints:
                try:
                    if nx.has_path(H, s, t):
                        ok = False; break
                except nx.NetworkXError:
                    continue
            if ok:
                return set(combo)
    return set()  # not found within kmax

# ---------- Runner ----------
ALGOS = [
    ("Remove Random Edge",  algo_remove_random_edge),
    ("Remove First Edge",   algo_remove_first_edge),
    ("Remove Min-Cut",      algo_remove_min_cut_union),
    ("Remove MinMC",        algo_remove_minmc_greedy),
    ("Brute Force",         algo_bruteforce_min_hitset),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dot", required=True, help="input DOT file (e.g., artefacts/graphs/G0.dot)")
    ap.add_argument("--outdir", default="artefacts/results", help="where to write summaries")
    ap.add_argument("--png", action="store_true", help="also render .png with graphviz")
    ap.add_argument("--seed", type=int, default=int(os.environ.get("PYTHONHASHSEED","0")))
    ap.add_argument("--kmax", type=int, default=int(os.environ.get("KON_BF_KMAX","4")))
    args = ap.parse_args()

    outdir = pathlib.Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)

    G0 = load_dot_to_digraph(args.dot)
    N0, M0 = G0.number_of_nodes(), G0.number_of_edges()

    starts, services = autodetect_sets(G0)
    constraints = build_constraints(G0, starts, services)

    rows = []
    md = []
    md.append(f"**Baseline:** `{os.path.basename(args.dot)}`  nodes={N0}  edges={M0}")
    md.append(f"**Starts:** {', '.join(starts)}")
    md.append(f"**Services:** {', '.join(services)}\n")

    for name, fn in ALGOS:
        G = G0.copy()
        # run algo → removed edge set
        if name == "Remove Random Edge":
            rem = fn(G, constraints, seed=args.seed)
        elif name == "Brute Force":
            rem = fn(G, constraints, kmax=args.kmax)
        else:
            rem = fn(G, constraints)

        # prune a copy for export
        GP = G0.copy()
        GP.remove_edges_from(rem)
        removed_count = len(rem)
        remaining = M0 - removed_count

        # write pruned graph
        gfile = outdir.parent / "graphs" / f"G1_{name.replace(' ','_')}.dot"
        write_graph_dot_png(GP, gfile)  # will also attempt PNG

        # collect summaries
        rows.append((name, removed_count, remaining))
        md.append(f"\n## {name}")
        md.append(f"- removed: **{removed_count}**  | remaining: **{remaining}**")
        if removed_count:
            md.append("- removed edges:")
            for (u,v) in sorted(rem):
                md.append(f"  - `{u}` → `{v}`")
        else:
            md.append("- removed edges: (none)")

    # CSV
    with open(outdir/"G0_alg_eval.csv","w",newline='') as f:
        w=csv.writer(f); w.writerow(["algorithm","removed","remaining"])
        w.writerows(rows)

    # Markdown
    with open(outdir/"G0_alg_eval.md","w") as f:
        f.write("\n".join(md) + "\n")

    print("Done.")
    print(" Summary CSV :", (outdir/'G0_alg_eval.csv').as_posix())
    print(" Summary MD  :", (outdir/'G0_alg_eval.md').as_posix())
    print(" Pruned DOTs :", (outdir.parent/'graphs').as_posix(), "(+ PNG if dot is available)")

if __name__ == "__main__":
    main()

