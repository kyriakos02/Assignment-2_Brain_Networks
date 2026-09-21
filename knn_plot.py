# file: knn_plot.py
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

print("Φόρτωση γραφήματος...")
G = nx.read_edgelist("edges.txt", nodetype=int, data=False)

print("Υπολογισμός μέσου βαθμού γειτόνων (k_nn)...")
knn_dict = nx.average_neighbor_degree(G)

# Ομαδοποίηση κατά βαθμό
degree_dict = dict(G.degree())
degree_knn = {}
for node, k in degree_dict.items():
    if k not in degree_knn:
        degree_knn[k] = []
    degree_knn[k].append(knn_dict[node])

k_values = np.array(sorted(degree_knn.keys()))
knn_values = np.array([np.mean(degree_knn[k]) for k in k_values])

# --- Plot σε log–log scale ---
plt.figure(figsize=(7,5))
plt.scatter(k_values, knn_values, s=10, alpha=0.7)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Degree k")
plt.ylabel("Average neighbor degree k_nn(k)")
plt.title("k_nn(k) vs k (log–log scale)")
plt.grid(True, which="both", ls="--", lw=0.3)
plt.tight_layout()
plt.savefig("knn_loglog.png", dpi=300)


# --- Εκτίμηση συσχέτισης (assortativity coefficient) ---
r = nx.degree_assortativity_coefficient(G)
print("\n— ΑΠΟΤΕΛΕΣΜΑΤΑ (h) —")
print(f"Degree assortativity coefficient (r): {r:.4f}")

if r > 0.05:
    trend = "Assortative"
elif r < -0.05:
    trend = "Disassortative"
else:
    trend = "Uncorrelated"

print(f"Κατηγοριοποίηση: {trend}")
print("✅ Δημιουργήθηκε το γράφημα knn_loglog.png")
