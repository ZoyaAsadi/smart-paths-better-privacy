# tools/apply_on_dot.py
import argparse, json, random, shutil, subprocess, pathlib, re
import pydot
import networkx as nx

# ---------- helpers ----------
def load_dot(dot_path: str) -> nx.DiGraph:
    pd = pydot.graph_from_dot_file(dot_path)[0]
    G  = nx.drawing.nx_pydot.from_pydot(pd)
    # labels may come as '\n"txt"' -> normalize to plain str
    for u, v, d in G.edges(data=True):
        lab = d.get("label")
        if isinstance(lab, (list, tuple)):
            lab = " ".join(map(str, lab))
        if lab is None:
            lab = ""
        d["label"] = str(lab)
    return G

def detect_services(G: nx.DiGraph):
    return sorted([n for n in G.nodes() if str(n).endswith("Svc")])

def detect_consent_sources(G: nx.DiGraph):
    # AcceptAll, Save,   Acc...  (AccSecurity, AccAnalytics, ...)
    nodes = set()
    for n in G.nodes():
        s = str(n)
        if s == "AcceptAll" or s == "Save" or s.startswith("Acc"):
            nodes.add(n)
    return sorted(nodes)

def consent_edges(G: nx.DiGraph, consent_srcs, services):
    """Edges that directly 'unlock' a service from consent sources."""
    E = []
    for u, v, d in G.edges(data=True):
        if u in consent_srcs and v in services:
            E.append((u, v))
    return sorted(set(E))

def ensure_outdir(outdir: pathlib.Path):
    outdir.mkdir(parents=True, exist_ok=True)

def write_json(outpath: pathlib.Path, algo_name: str, removed):
    obj = {
        "algo": algo_name,
        "removed_count": len(removed),
        "removed": [(str(u), str(v)) for (u, v) in removed],
    }
    outpath.write_text(json.dumps(obj, ensure_ascii=False, indent=2))

def colorize_removed(G: nx.DiGraph, removed):
    H = G.copy()
    # annotate removed edges in red, dashed
    for (u, v) in H.edges():
        H.edges[u, v]["color"] = "black"
        H.edges[u, v]["penwidth"] = "1"
        H.edges[u, v]["style"] = "solid"
    for (u, v) in removed:
        if H.has_edge(u, v):
            H.edges[u, v]["color"] = "red"
            H.edges[u, v]["penwidth"] = "2"
            H.edges[u, v]["style"] = "dashed"
    return H

def to_dot(G: nx.DiGraph, path: pathlib.Path, title: str = None):
    # add nice header
    g = pydot.Dot(graph_type="digraph", rankdir="LR")
    if title:
        g.set_label(title); g.set_labelloc("top"); g.set_fontsize("10")

    # add nodes
    for n, d in G.nodes(data=True):
        nd = pydot.Node(str(n), **{k:str(v) for k,v in d.items() if v is not None})
        g.add_node(nd)

    # add edges
    for u, v, d in G.edges(data=True):
        attrs = {k:str(vv) for k,vv in d.items() if vv is not None}
        g.add_edge(pydot.Edge(str(u), str(v), **attrs))

    g.write_raw(path.as_posix())

def render_png(dot_path: pathlib.Path, png_path: pathlib.Path):
    dot = shutil.which("dot")
    if not dot:
        return False
    subprocess.check_call([dot, "-Tpng", dot_path.as_posix(), "-o", png_path.as_posix()])
    return True

# ---------- algorithms ----------
def alg_remove_random(G: nx.DiGraph, consent_srcs, services):
    """Iteratively remove random consent→service edges until none remains."""
    E = consent_edges(G, consent_srcs, services)
    removed = []
    rng = random.Random(int(pathlib.os.environ.get("PYTHONHASHSEED", "0") or 0))
    H = G.copy()
    while True:
        E = [(u, v) for (u, v) in E if H.has_edge(u, v)]
        if not E:
            break
        e = rng.choice(E)
        H.remove_edge(*e)
        removed.append(e)
    return removed

def alg_remove_first(G: nx.DiGraph, consent_srcs, services):
    """Remove ALL consent→service edges (first edges on consent chains)."""
    return consent_edges(G, consent_srcs, services)

def choose_one_incoming(consent_edges_for_service):
    """Pick which incoming to cut first (preference: AcceptAll -> Save -> Acc*)"""
    def score(u):
        s = str(u)
        if s == "AcceptAll": return 0
        if s == "Save":      return 1
        if s.startswith("Acc"): return 2
        return 3
    u_candidates = sorted(consent_edges_for_service, key=lambda e: score(e[0]))
    return u_candidates[0] if u_candidates else None

def alg_min_cut_like(G: nx.DiGraph, consent_srcs, services):
    """For each service, remove one incoming from consent sources."""
    removed = []
    E = consent_edges(G, consent_srcs, services)
    by_svc = {}
    for (u, v) in E:
        by_svc.setdefault(v, []).append((u, v))
    for svc, incs in by_svc.items():
        pick = choose_one_incoming(incs)
        if pick:
            removed.append(pick)
    return sorted(removed)

def alg_minmc_greedy(G: nx.DiGraph, consent_srcs, services):
    """Greedy approximate: very similar to min-cut here."""
    # On this graph, it's effectively the same decision as min_cut_like.
    return alg_min_cut_like(G, consent_srcs, services)

def alg_bruteforce(G: nx.DiGraph, consent_srcs, services, kmax=3):
    """Find smallest set (k<=kmax) that removes at least one incoming per service."""
    E = consent_edges(G, consent_srcs, services)
    by_svc = {}
    for (u, v) in E:
        by_svc.setdefault(v, []).append((u, v))

    # quick lower bound: need at least #services edges (one per service)
    # so if kmax < len(services), just return 'one per service' as baseline
    if kmax < len(services):
        return alg_min_cut_like(G, consent_srcs, services)

    # otherwise brute-force small search: try to pick exactly one per service
    # (cartesian product of choices)
    from itertools import product
    choices = []
    for svc in services:
        inc = by_svc.get(svc, [])
        if not inc:
            # service has no consent incoming; nothing to cut for it
            continue
        choices.append(inc)
    best = None
    for combo in product(*choices):
        S = set(combo)  # one per service
        if best is None or len(S) < len(best):
            best = S
    return sorted(best or [])

# ---------- main ----------
ALGOS = {
    "Remove Random Edge": alg_remove_random,
    "Remove First Edge":  alg_remove_first,
    "Remove Min-Cut":     alg_min_cut_like,
    "Remove MinMC":       alg_minmc_greedy,
    "Brute Force":        lambda G, c, s: alg_bruteforce(G, c, s, kmax=6),
}

def run_all(dot_path: str, outdir: str):
    outdir = pathlib.Path(outdir)
    ensure_outdir(outdir)

    G = load_dot(dot_path)
    services = detect_services(G)
    consent  = detect_consent_sources(G)

    summary_rows = []
    md_lines = []
    md_lines.append(f"**Total nodes:** {G.number_of_nodes()}  |  **Total edges:** {G.number_of_edges()}")
    md_lines.append(f"**Services:** {', '.join(map(str, services))}")
    md_lines.append(f"**Consent sources:** {', '.join(map(str, consent))}\n")
    md_lines.append("| Algorithm | Removed | Remaining |")
    md_lines.append("|-----------|-------:|----------:|")

    for name, fn in ALGOS.items():
        removed = fn(G, consent, services)
        removed = sorted(set(removed))
        # JSON
        json_path = outdir / f"removed_{re.sub(r'[^A-Za-z0-9]+','_',name).lower()}.json"
        write_json(json_path, name, removed)

        # annotated DOT/PNG (original with removed in red)
        ann = colorize_removed(G, removed)
        dot_ann = outdir / f"G0_{re.sub(r'[^A-Za-z0-9]+','_',name)}_annotated.dot"
        to_dot(ann, dot_ann, title=f"{name} — removed edges in red")
        if shutil.which("dot"):
            render_png(dot_ann, dot_ann.with_suffix(".png"))

        # pruned graph G' (after removal)
        Gp = G.copy()
        for e in removed:
            if Gp.has_edge(*e):
                Gp.remove_edge(*e)
        dot_pruned = outdir / f"G1_{re.sub(r'[^A-Za-z0-9]+','_',name)}.dot"
        to_dot(Gp, dot_pruned, title=f"{name} — pruned graph (G')")
        if shutil.which("dot"):
            render_png(dot_pruned, dot_pruned.with_suffix(".png"))

        remain = G.number_of_edges() - len(removed)
        summary_rows.append((name, len(removed), remain))
        md_lines.append(f"| {name} | {len(removed)} | {remain} |")

    # write CSV + Markdown
    (outdir / "alg_summary.csv").write_text(
        "algo,removed,remaining\n" +
        "\n".join(f"{a},{r},{m}" for a, r, m in summary_rows) + "\n"
    )
    (outdir / "alg_summary.md").write_text("\n".join(md_lines) + "\n")

    print("Done. Wrote:")
    print(" -", (outdir / "alg_summary.csv").as_posix())
    print(" -", (outdir / "alg_summary.md").as_posix())
    for name in ALGOS:
        stem = re.sub(r'[^A-Za-z0-9]+','_',name)
        print(f" - JSON:   { (outdir / f'removed_{stem.lower()}.json').name }")
        print(f" - DOT(ann): G0_{stem}_annotated.dot  (+ .png if graphviz present)")
        print(f" - DOT(G′):  G1_{stem}.dot            (+ .png if graphviz present)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dot", required=True, help="Path to G0.dot")
    ap.add_argument("--outdir", default="artefacts/graphs", help="Output directory")
    ap.add_argument("--seed", type=int, default=0, help="Random seed for Remove Random Edge")
    args = ap.parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    run_all(args.dot, args.outdir)

if __name__ == "__main__":
    main()

