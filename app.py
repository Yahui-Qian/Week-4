
import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Define the graph structure
graph = {
    'Origin': {'A': 40, 'B': 60, 'C': 50},
    'A': {'B': 10, 'D': 70},
    'B': {'C': 20, 'D': 55, 'E': 40},
    'C': {'D': 50},
    'D': {'E': 10, 'Destination': 60},
    'E': {'Destination': 80},
    'Destination': {}
}

# Step 2: Dijkstra's algorithm implementation
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return cost, path
        visited.add(node)
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return float("inf"), []

# Step 3: Streamlit interface
st.title("Shortest Path Finder: Dijkstra’s Algorithm")

st.write("Welcome! This tool visualizes shortest paths on a graph using Dijkstra’s algorithm.")

start = st.selectbox("Choose a starting town", list(graph.keys()))
end = st.selectbox("Choose a destination town", list(graph.keys()))

if st.button("Find Shortest Path"):
    if start == end:
        st.warning("Start and destination are the same.")
    else:
        cost, path = dijkstra(graph, start, end)
        if cost < float("inf"):
            st.success(f"Shortest path: {' ➝ '.join(path)} (Total distance: {cost} miles)")
        else:
            st.error("No valid route found between selected towns.")

# Step 4: Graph visualization title
st.subheader("Graph Visualization of Town Network")

import matplotlib.pyplot as plt
import networkx as nx

def draw_network(graph_dict, path=None):
    # Create directed graph
    G = nx.DiGraph()
    for u in graph_dict:
        for v, w in graph_dict[u].items():
            G.add_edge(u, v, weight=w)

    # Positioning
    pos = nx.circular_layout(G)

    # Get weights as edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Start plotting
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1200)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # Highlight shortest path (if available)
    if path and len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=1300)

    plt.title("Town Graph – Distances as Edge Weights", fontsize=14)
    plt.axis('off')
    st.pyplot(plt.gcf())

# Call function
draw_network(graph, path=path if 'path' in locals() else None)
