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

# Step 4: Graph visualization
st.subheader("Graph Visualization of Town Network")

# Convert to NetworkX graph
G = nx.DiGraph()
for u in graph:
    for v, w in graph[u].items():
        G.add_edge(u, v, weight=w)

# Draw the graph
pos = nx.spring_layout(G, seed=42)  # Stable layout
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1800, font_size=12, arrows=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Town Graph - Distances as Edge Weights")

# Display the plot in Streamlit
st.pyplot(plt.gcf())
