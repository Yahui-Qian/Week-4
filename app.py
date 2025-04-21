
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Shortest Path Visualizer", layout="centered")

st.title("🚗 最短路径可视化 - 城镇导航")

# 定义图
G = nx.DiGraph()

edges = [
    ("Origin", "A", 40),
    ("Origin", "B", 60),
    ("Origin", "C", 50),
    ("A", "B", 10),
    ("A", "D", 70),
    ("B", "C", 20),
    ("B", "D", 55),
    ("B", "E", 40),
    ("C", "E", 50),
    ("C", "Destination", 80),
    ("D", "E", 10),
    ("D", "Destination", 60),
    ("E", "Destination", 60)
]

G.add_weighted_edges_from(edges)

# 最短路径计算
shortest_path = nx.dijkstra_path(G, source="Origin", target="Destination")
shortest_distance = nx.dijkstra_path_length(G, source="Origin", target="Destination")

# 展示最短路径
st.markdown(f"### ✅ 最短路径: {' → '.join(shortest_path)}")
st.markdown(f"### 📏 最短距离: {shortest_distance} miles")

# 可视化图形
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1200, font_size=14)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})

# 高亮最短路径
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3)

st.pyplot(plt)
