import networkx as nx
from networkx.drawing.nx_agraph import read_dot
from algorithms import remove_random_edge

# Load graph
G = read_dot("Graph.dot")

# Set capacity=1 for every edge
for u, v, data in G.edges(data=True):
    if 'capacity' not in data:
        data['capacity'] = 1

# Constraint path to preserve
constraints = [('CookieConsent', 'DownloadBook')]
print("constraint:", constraints[0])

# Apply the algorithm
remove_random_edge(G, constraints)

# Save the result
nx.nx_agraph.write_dot(G, "output_graph_random_edge.dot")
print("✅ Graph saved as output_graph_random_edge.dot")
