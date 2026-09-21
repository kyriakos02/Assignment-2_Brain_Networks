# file: analyze_network.py
import networkx as nx
import json
from pathlib import Path

EDGES_PATH = Path("edges.txt")

print("Φόρτωση undirected γραφήματος από edges.txt ...")
G = nx.read_edgelist(EDGES_PATH, nodetype=int, data=False)  # undirected by default

n = G.number_of_nodes()
m = G.number_of_edges()

# Μέσος βαθμός: 2m / n
avg_degree = (2.0 * m) / n if n > 0 else 0.0

# Κόμβοι με βαθμό > 1 (να αγνοήσουμε degree-1 στο clustering)
nodes_deg_gt1 = [u for u, d in G.degree() if d > 1]

# Average clustering αγνοώντας degree-1
if nodes_deg_gt1:
    # Υπολογισμός clustering για αυτούς τους κόμβους
    c_by_node = nx.clustering(G, nodes=nodes_deg_gt1)
    avg_clustering_excl_deg1 = sum(c_by_node.values()) / len(nodes_deg_gt1)
else:
    avg_clustering_excl_deg1 = 0.0

# Εναλλακτικός έλεγχος (προαιρετικά): το standard average_clustering (περιλαμβάνει degree-1 ως 0)
avg_clustering_including_deg1 = nx.average_clustering(G)

results = {
    "total_nodes": n,
    "total_edges": m,
    "average_degree": avg_degree,
    "average_clustering_excluding_degree_1": avg_clustering_excl_deg1,
    "average_clustering_including_degree_1 (FYI)": avg_clustering_including_deg1,
}

print("\n— ΑΠΟΤΕΛΕΣΜΑΤΑ (e) —")
for k, v in results.items():
    if isinstance(v, float):
        print(f"{k}: {v:.6f}")
    else:
        print(f"{k}: {v}")

# Αποθήκευση και σε JSON για το report
with open("stats_e.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n✅ Ολοκληρώθηκε. Τα αποτελέσματα γράφτηκαν και στο stats_e.json")
