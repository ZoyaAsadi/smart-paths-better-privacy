import sys, argparse, shutil, pathlib
import pydot
import networkx as nx
from networkx.drawing.nx_pydot import from_pydot, to_pydot

SERVICES = {
    "SecuritySvc", "AnalyticsSvc", "ExtMediaSvc",
    "SupportSvc", "PaymentsSvc", "PersonalSvc",
}

BACKBONE = [
    ("BannerToast","LetMeChoose"),
    ("LetMeChoose","Modal"),
    ("Modal","Save"),
]

def load_dot(dot_path: pathlib.Path):
    graphs = pydot.graph_from_dot_file(str(dot_path))
    if not graphs:
        raise RuntimeError(f"Cannot parse DOT: {dot_path}")
    return graphs[0]

def write_dot_png(pdot, out_dot: pathlib.Path, out_png: pathlib.Path):
    out_dot.write_text(pdot.to_string())
    if shutil.which("dot"):
        pdot.write_png(str(out_png))

def to_nx(pdot):
    return from_pydot(pdot)

def ensure_backbone(pdot):
    for u,v in BACKBONE:
        if not any(e.get_source()==u and e.get_destination()==v for e in pdot.get_edges()):
            pdot.add_edge(pydot.Edge(u,v,label="auto-backbone"))

def remove_accept_all_shortcuts(pdot):
    for e in list(pdot.get_edges()):
        if e.get_source() == "AcceptAll":
            pdot.del_edge(e.get_source(), e.get_destination())

def keep_only_save_to(pdot, required_service: str):
    for e in list(pdot.get_edges()):
        if e.get_source()=="Save" and e.get_destination() in SERVICES:
            if e.get_destination() != required_service:
                pdot.del_edge("Save", e.get_destination())

def add_missing_save_edge(pdot, required_service: str):
    if not any(e.get_source()=="Save" and e.get_destination()==required_service for e in pdot.get_edges()):
        pdot.add_edge(pydot.Edge("Save", required_service, label="selected? unlock"))

def shortest_clicks(pdot, start_node: str, target_node: str) -> int:
    G = to_nx(pdot)
    if start_node not in G or target_node not in G:
        return 10**9
    try:
        return nx.shortest_path_length(G, start_node, target_node)
    except nx.NetworkXNoPath:
        return 10**9

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dot", required=True, help="path to G0.dot")
    ap.add_argument("--start", required=True, help="start page, e.g., Audiobooks")
    ap.add_argument("--service", required=True, help="required service node, e.g., ExtMediaSvc")
    ap.add_argument("--outdir", default="artefacts/graphs", help="output dir for variants")
    args = ap.parse_args()

    dot_path = pathlib.Path(args.dot)
    outdir   = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # قبل
    g0 = load_dot(dot_path)
    before = shortest_clicks(g0, args.start, args.service)

    # بعد (نسخه بهینه)
    g1 = load_dot(dot_path)
    ensure_backbone(g1)
    remove_accept_all_shortcuts(g1)
    keep_only_save_to(g1, args.service)
    add_missing_save_edge(g1, args.service)
    after = shortest_clicks(g1, args.start, args.service)

    prefix = f"{args.start}__{args.service}"
    write_dot_png(g0, outdir / f"G0_{prefix}.dot", outdir / f"G0_{prefix}.png")
    write_dot_png(g1, outdir / f"G1_{prefix}.dot", outdir / f"G1_{prefix}.png")

    INF = 10**9
    def norm(x): return "∞" if x>=INF else str(x)
    print(f"[{args.start} → {args.service}]  clicks_before={norm(before)}  clicks_after={norm(after)}")
    if after < before:
        print("Path shortened while removing risky shortcuts (AcceptAll).")
    else:
        print(" No shorter path was found with removals only; consider UI preselection to make Save one-click.")

if __name__ == "__main__":
    main()

