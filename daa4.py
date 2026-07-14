import streamlit as st
import heapq

st.set_page_config(page_title="MST Visualizer", page_icon="🌳", layout="wide")

st.title("🌳 Minimum Spanning Tree (MST)")
st.subheader("Kruskal's Algorithm vs Prim's Algorithm")

# ---------------- Union-Find ----------------

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


# ---------------- Kruskal ----------------

def kruskal(n, edges):

    edges = sorted(edges)

    uf = UnionFind(n)

    mst = []
    cost = 0

    for w, u, v in edges:

        if uf.union(u, v):

            mst.append((u, v, w))
            cost += w

            if len(mst) == n - 1:
                break

    return mst, cost


# ---------------- Prim ----------------

def prim(n, adj, start=0):

    key = [float("inf")] * n
    parent = [-1] * n
    visited = [False] * n

    key[start] = 0

    pq = [(0, start)]

    mst = []
    cost = 0

    while pq:

        w, u = heapq.heappop(pq)

        if visited[u]:
            continue

        visited[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w

        for v, wt in adj.get(u, []):

            if not visited[v] and wt < key[v]:

                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost


# ---------------- Sample Graph ----------------

n = 7

edges = [
    (7, 0, 1),
    (5, 0, 3),
    (8, 1, 2),
    (9, 1, 3),
    (7, 1, 4),
    (5, 2, 4),
    (15, 3, 4),
    (6, 3, 5),
    (8, 4, 5),
    (9, 4, 6),
    (11, 5, 6)
]

adj = {}

for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

# ---------------- Display Graph ----------------

st.header("Input Graph")

st.table(
    {
        "Node U": [u for w, u, v in edges],
        "Node V": [v for w, u, v in edges],
        "Weight": [w for w, u, v in edges]
    }
)

# ---------------- Buttons ----------------

col1, col2 = st.columns(2)

with col1:

    if st.button("Run Kruskal"):

        mst, cost = kruskal(n, edges)

        st.success("Kruskal's Algorithm Completed")

        st.write("### MST Edges")

        st.table(
            {
                "From": [u for u, v, w in mst],
                "To": [v for u, v, w in mst],
                "Weight": [w for u, v, w in mst]
            }
        )

        st.metric("Total Cost", cost)

with col2:

    if st.button("Run Prim"):

        mst, cost = prim(n, adj)

        st.success("Prim's Algorithm Completed")

        st.write("### MST Edges")

        st.table(
            {
                "From": [u for u, v, w in mst],
                "To": [v for u, v, w in mst],
                "Weight": [w for u, v, w in mst]
            }
        )

        st.metric("Total Cost", cost)

# ---------------- Compare ----------------

if st.button("Compare Both Algorithms"):

    kmst, kcost = kruskal(n, edges)
    pmst, pcost = prim(n, adj)

    st.header("Comparison")

    st.write("### Kruskal")

    st.table(
        {
            "From": [u for u, v, w in kmst],
            "To": [v for u, v, w in kmst],
            "Weight": [w for u, v, w in kmst]
        }
    )

    st.metric("Kruskal Cost", kcost)

    st.write("---")

    st.write("### Prim")

    st.table(
        {
            "From": [u for u, v, w in pmst],
            "To": [v for u, v, w in pmst],
            "Weight": [w for u, v, w in pmst]
        }
    )

    st.metric("Prim Cost", pcost)

    if kcost == pcost:
        st.success("Both algorithms produce the same Minimum Spanning Tree cost.")
