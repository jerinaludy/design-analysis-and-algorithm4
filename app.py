import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dijkstra's Algorithm", page_icon="🛣️", layout="wide")

# ---------------- Dijkstra Algorithm ----------------

def dijkstra(graph, source):

    n = len(graph)

    dist = [float("inf")] * n
    prev = [None] * n

    dist[source] = 0

    pq = [(0, source)]
    visited = set()

    while pq:

        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):

    path = []

    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


# ---------------- Sample Graph ----------------

graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

# ---------------- Sidebar ----------------

st.sidebar.title("Settings")

source = st.sidebar.number_input(
    "Source Vertex",
    min_value=0,
    max_value=len(graph)-1,
    value=0,
    step=1
)

run = st.sidebar.button("Run Dijkstra")

# ---------------- Title ----------------

st.title("🛣️ Dijkstra's Shortest Path Algorithm")

st.write("""
This application demonstrates **Dijkstra's Algorithm** using a **Min Heap (Priority Queue)**.

**Time Complexity:** O((V + E) log V)

**Space Complexity:** O(V)
""")

# ---------------- Draw Graph ----------------

G = nx.DiGraph()

for u in graph:
    for v, w in graph[u]:
        G.add_edge(u, v, weight=w)

fig, ax = plt.subplots(figsize=(8,5))

pos = nx.spring_layout(G, seed=42)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=900,
    node_color="skyblue",
    ax=ax
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=12,
    font_weight="bold",
    ax=ax
)

nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowsize=20,
    ax=ax
)

edge_labels = nx.get_edge_attributes(G, "weight")

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    ax=ax
)

ax.set_title("Graph Visualization")

st.pyplot(fig)

# ---------------- Run Algorithm ----------------

if run:

    dist, prev = dijkstra(graph, source)

    st.success(f"Dijkstra executed successfully from Source Vertex {source}")

    data = []

    for v in range(len(graph)):

        path = reconstruct_path(prev, source, v)

        if path:
            path_str = " → ".join(map(str, path))
        else:
            path_str = "No Path"

        distance = dist[v]

        if distance == float("inf"):
            distance = "INF"

        data.append({
            "Vertex": v,
            "Distance": distance,
            "Shortest Path": path_str
        })

    st.subheader("Shortest Distance Table")

    st.table(data)

    st.subheader("Detailed Results")

    for row in data:
        st.write(
            f"**Vertex {row['Vertex']}** | Distance = **{row['Distance']}** | Path = **{row['Shortest Path']}**"
        )
