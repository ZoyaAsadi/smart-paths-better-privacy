import networkx as nx
from networkx.drawing.nx_agraph import read_dot, write_dot
from algorithms import remove_st_cuts

# Load the graph from DOT file
G = read_dot("accurate_expanded_website_graph.dot")

# Assign default capacity if not present
for u, v in G.edges():
    if 'capacity' not in G[u][v]:
        G[u][v]['capacity'] = 1

# Define source-target constraints (example: EssentialCookies to DownloadBook)
constraints = [("EssentialCookies", "DownloadBook")]

# Apply the minimum s-t cut removal algorithm
remove_st_cuts(G, constraints)

# Save the modified graph to a new DOT file
write_dot(G, "accurate_expanded_website_graph_min_cut.dot")

print("Min-cut applied. Modified graph saved as accurate_expanded_website_graph_min_cut.dot")
