#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, json, pathlib
import networkx as nx
import pydot

def load_graph(graph_path):
    d = json.load(open(graph_path))
    G = nx.DiGraph()
    for n in d.get("nodes", []):
        G.add_node(n)
    for e in d.get("edges", []):
        G.add_edge(e["src"], e["dst"], kind=e.get("kind",""), cost=e.get("cost"))
    starts = d.get("startNodes", [])
    target = d.get("target")
    return G, starts, target

def load_removed(removed_path):
    d = json.load(open(removed_path))
    rem = [tuple(x) for x in d.get("removed", [])]
    return rem, d.get("algo","")

def build_pydot(G, starts, target, highlight_edges=None, title=None):
    highlight_edges = set(highlight_edges or [])
    dot = pydot.Dot(graph_type="digraph", rankdir="LR", labelloc="t", fontsize="18")
    if title:
        dot.set_label(title)

    # Nodes
    for n in G.nodes():
        attrs = {"shape":"box", "style":"filled", "fillcolor":"white"}
        if n in starts:
            attrs["fillcolor"] = "lightblue"
        if n == target:
            attrs["fillcolor"] = "palegreen"
        dot.add_node(pydot.Node(n, **attrs))

    # Edges
    for u, v, data in G.edges(data=True):
        label = data.get("kind", "")
        if data.get("cost") is not None:
            label = (label + (" (" if label else "") + f"{data['cost']}" + (")" if label else ""))
        attrs = {"label": label, "arrowsize":"0.7"}
        if (u, v) in highlight_edges:
            attrs.update({"color":"red", "penwidth":"3"})
        else:
            attrs.update({"color":"#888888", "penwidth":"1"})
        dot.add_edge(pydot.Edge(u, v, **attrs))

    return dot

def main():
    ap = argparse.ArgumentParser(description="Visualize graph before/after removing edges")
    ap.add_argument("--graph", required=True, help="Path to consent_graph.json")
    ap.add_argument("--removed", required=True, help="Path to removed_*.json produced by an algorithm")
    ap.add_argument("--out", required=True, help="Output directory")
    ap.add_argument("--fmt", default="png", choices=["png","svg","pdf"], help="image format")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    G, starts, target = load_graph(args.graph)
    rem, algo_name = load_removed(args.removed)
    rem_set = set(rem)

    # 1) original
    dot_orig = build_pydot(G, starts, target, highlight_edges=None, title="Original graph")
    dot_orig.write_raw(str(out_dir/"original.dot"))
    getattr(dot_orig, f"write_{args.fmt}")(str(out_dir/f"original.{args.fmt}"))

    # 2) diff on original (removed edges in red)
    dot_diff = build_pydot(G, starts, target, highlight_edges=rem_set, title=f"Diff (highlight removed) — {algo_name}")
    dot_diff.write_raw(str(out_dir/"diff.dot"))
    getattr(dot_diff, f"write_{args.fmt}")(str(out_dir/f"diff.{args.fmt}"))

    # 3) pruned graph
    Gp = G.copy()
    Gp.remove_edges_from(rem)
    dot_pruned = build_pydot(Gp, starts, target, highlight_edges=None, title=f"Pruned graph — {algo_name}")
    dot_pruned.write_raw(str(out_dir/"pruned.dot"))
    getattr(dot_pruned, f"write_{args.fmt}")(str(out_dir/f"pruned.{args.fmt}"))

    print("Wrote:")
    print(" -", (out_dir/"original.dot").as_posix(), (out_dir/f"original.{args.fmt}").as_posix())
    print(" -", (out_dir/"diff.dot").as_posix(),     (out_dir/f"diff.{args.fmt}").as_posix())
    print(" -", (out_dir/"pruned.dot").as_posix(),   (out_dir/f"pruned.{args.fmt}").as_posix())

if __name__ == "__main__":
    main()

