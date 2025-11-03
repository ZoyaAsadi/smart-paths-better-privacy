# tools/batch_run.py
import json, argparse, os, csv
import networkx as nx

from tools.konstantin_adapter import run_algorithm as run_konst

ALGOS_DEFAULT = [
    "disconnect",
    "first_edge",
    "random_edge",          #   Random output
    "st_cut",
    "optimisation_approx",
    # "matrix_bruteforce",  #        
]

def load_graph_as_nx(path):
    d = json.load(open(path))
    G = nx.DiGraph()
    G.add_nodes_from(d["nodes"])
    for e in d["edges"]:
        #     Cost of Constantin Algorithms
        G.add_edge(e["src"], e["dst"], cost=int(e.get("cost", 1)), capacity=int(e.get("capacity", 1)))
    return d, G

def remove_edges(G, removed):
    for u, v in removed:
        if G.has_edge(u, v):
            G.remove_edge(u, v)

def min_path_cost(G, starts, target):
    best = None
    for s in starts:
        try:
            val = nx.shortest_path_length(G, s, target, weight="cost")
            best = val if best is None or val < best else best
        except nx.NetworkXNoPath:
            pass
    return best  # None   

def edge_cost(G, u, v):
    return G[u][v].get("cost", 1)

def compute_privacy_metrics(d, G):
    starts = d["startNodes"]
    T      = d["target"]

    #       
    best_to_target = min_path_cost(G, starts, T)

    #   spacial way
    # AcceptAll → S_decided
    m_acc_all = None
    if "AcceptAll" in G and G.has_edge("AcceptAll", T):
        #     AcceptAll +  Edge
        to_acc = min_path_cost(G, starts, "AcceptAll")
        if to_acc is not None:
            m_acc_all = to_acc + edge_cost(G, "AcceptAll", T)

    # Decline → S_decided
    m_decline = None
    if "Decline" in G and G.has_edge("Decline", T):
        to_dec = min_path_cost(G, starts, "Decline")
        if to_dec is not None:
            m_decline = to_dec + edge_cost(G, "Decline", T)

    # AcceptSelected → Apply → S_decided
    m_acc_sel = None
    if G.has_edge("AcceptSelected", "Apply") and G.has_edge("Apply", T):
        to_sel = min_path_cost(G, starts, "AcceptSelected")
        if to_sel is not None:
            m_acc_sel = to_sel + edge_cost(G, "AcceptSelected", "Apply") + edge_cost(G, "Apply", T)

    # / privacy
    accept_all_blocked  = (m_acc_all is None)        
    decline_available   = (m_decline is not None)
    dark_pattern        = (m_acc_all is not None and m_decline is not None and m_acc_all < m_decline)
    privacy_ok          = accept_all_blocked or (decline_available and not dark_pattern)

    return {
        "min_clicks_any_start_to_target": best_to_target,
        "min_clicks_accept_all": m_acc_all,
        "min_clicks_decline":    m_decline,
        "min_clicks_accept_selected": m_acc_sel,
        "accept_all_blocked": accept_all_blocked,
        "decline_available":  decline_available,
        "dark_pattern":       dark_pattern,
        "privacy_ok":         privacy_ok,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--out",   required=True)
    ap.add_argument("--algos", default=",".join(ALGOS_DEFAULT),
                    help=" disconnect,st_cut,optimisation_approx")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    algos = [a.strip() for a in args.algos.split(",") if a.strip()]

    #  CSV Report
    csv_path = os.path.join(args.out, "alg_eval.csv")
    with open(csv_path, "w", newline="") as fcsv:
        w = csv.writer(fcsv)
        w.writerow([
            "algo",
            "removed_count",
            "removed_edges",
            "min_clicks_any_start_to_target",
            "min_clicks_accept_all",
            "min_clicks_decline",
            "min_clicks_accept_selected",
            "accept_all_blocked",
            "decline_available",
            "dark_pattern",
            "privacy_ok",
        ])

        for algo in algos:
            #     Run Algorithm
            res = run_konst(args.graph, algo, args.out)
            removed = res["removed"]

            # Save in JSON  
            out_json = os.path.join(args.out, f"removed_{algo}.json")
            with open(out_json, "w") as jf:
                json.dump(res, jf, indent=2, ensure_ascii=False)

            #      Make a Grapg after removal of edges  
            d, G = load_graph_as_nx(args.graph)
            remove_edges(G, removed)
            metrics = compute_privacy_metrics(d, G)

            #  Report
            w.writerow([
                algo,
                res.get("removed_count", len(removed)),
                ";".join([f"{u}->{v}" for u, v in removed]),
                metrics["min_clicks_any_start_to_target"],
                metrics["min_clicks_accept_all"],
                metrics["min_clicks_decline"],
                metrics["min_clicks_accept_selected"],
                metrics["accept_all_blocked"],
                metrics["decline_available"],
                metrics["dark_pattern"],
                metrics["privacy_ok"],
            ])

            print(f"[{algo}] removed={len(removed)}  privacy_ok={metrics['privacy_ok']}  "
                  f"(accAll={metrics['min_clicks_accept_all']}, decline={metrics['min_clicks_decline']})")

    print(f"\nWrote summary: {csv_path}")

if __name__ == "__main__":
    main()

