import osmnx as ox
import matplotlib.pyplot as plt
import heapq
from collections import defaultdict


# downloading data

print("Downloading map data... (please wait)")

center_point = (28.6315, 77.2167)  # Connaught Place
G_osm = ox.graph_from_point(center_point, dist=1500, network_type="drive", simplify=True)        #receives data as multidi- graph

print("Download complete!")
print(f"Nodes: {len(G_osm.nodes)} | Edges: {len(G_osm.edges)}")

# -------------------------------------------------
# 2. Convert OSMnx graph → Our own adjacency list
# -------------------------------------------------
graph = defaultdict(list)          # node → [(neighbor, weight), ...]
nodes_data = {}                    # store lat/lon for later



for u, v,data in G_osm.edges(data=True):
    length = data.get("length", 1.0)
    graph[u].append((v, length))

    if not data.get("oneway", False):                      #if it is a bidirectional edge
        graph[v].append((u, length))

# Store coordinates of every node
for node, data in G_osm.nodes(data = True):
    nodes_data[node] = (data["y"], data["x"])  # (lat, lon)

print("Graph converted to adjacency list successfully!")


# creating the file garph_data.txt

with open("graph_data.txt", "w") as f:
    for node in graph:
        for neighbor, weight in graph[node]:
            f.write(f"{node} {neighbor} {weight}\n")

print("Graph saved to graph_data.txt")


##creating node data.txt

with open("nodes_data.txt", "w") as f:
    for node, (lat, lon) in nodes_data.items():
        f.write(f"{node} {lat} {lon}\n")

print("nodes_data.txt created successfully!")



print("\nDone!")