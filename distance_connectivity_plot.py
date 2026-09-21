# file: distance_connectivity_plot.py
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re
from scipy.spatial.distance import pdist, squareform

print("Φόρτωση δεδομένων...")
G = nx.read_edgelist("edges.txt", nodetype=int, data=False)

# --- 1. Διαβάζουμε coordinates ---
coords = pd.read_csv("coordinates.csv")
coords["position"] = coords["position"].apply(lambda s: re.sub(r"[\[\]]", "", str(s)).strip())
xyz = coords["position"].str.split(r"\s+", expand=True).astype(float)
coords = pd.concat([coords[["root_id"]], xyz], axis=1)
coords = coords.rename(columns={"root_id": "id"}).dropna(subset=[0,1,2])
coords.columns = ["id", "x", "y", "z"]
coords = coords.drop_duplicates(subset=["id"]).set_index("id")
print(f"Νευρώνες με έγκυρες συντεταγμένες: {len(coords):,}")

# --- 2. Υποδειγματοληψία για ταχύτητα ---
np.random.seed(0)
sample_nodes = np.random.choice(coords.index, size=20000, replace=False)
coords_sub = coords.loc[sample_nodes]
print(f"Δείγμα κόμβων για ανάλυση: {len(coords_sub)}")

# --- 3. Αποστάσεις όλων των pairs στο δείγμα ---
positions = coords_sub[["x","y","z"]].values
dist_matrix = squareform(pdist(positions))
distances = dist_matrix[np.triu_indices(len(coords_sub), k=1)]

# --- 4. Συνδέσεις μόνο μέσα στο ίδιο δείγμα ---
edges_sub = [(u,v) for u,v in G.edges() if u in coords_sub.index and v in coords_sub.index]
print(f"Αριθμός συνδέσεων στο δείγμα: {len(edges_sub):,}")
if len(edges_sub)==0:
    raise RuntimeError("Δεν βρέθηκαν συνδέσεις μέσα στο δείγμα κόμβων!")

# --- 5. Υπολογισμός αποστάσεων για τις συνδεδεμένες ακμές ---
A = coords_sub.loc[[u for u,v in edges_sub], ["x","y","z"]].values
B = coords_sub.loc[[v for u,v in edges_sub], ["x","y","z"]].values
dist_conn = np.linalg.norm(A - B, axis=1)

# --- 6. Λογαριθμικά bins και υπολογισμός P(d) ---
bins = np.logspace(np.log10(min(distances.min(), dist_conn.min())+1e-9),
                   np.log10(max(distances.max(), dist_conn.max())+1e-9), 40)
hist_all, _ = np.histogram(distances, bins=bins)
hist_conn, _ = np.histogram(dist_conn, bins=bins)
p_d = hist_conn / np.maximum(hist_all, 1)
bin_centers = np.sqrt(bins[:-1] * bins[1:])

# --- 7. Plot ---
plt.figure(figsize=(7,5))
plt.scatter(bin_centers, p_d, s=15, alpha=0.7)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Distance d (nm)")
plt.ylabel("Connection probability P(d)")
plt.title("P(d) vs Distance (log–log)")
plt.grid(True, which="both", ls="--", lw=0.3)
plt.tight_layout()
plt.savefig("distance_connectivity_loglog.png", dpi=300)


print("✅ Δημιουργήθηκε το γράφημα distance_connectivity_loglog.png")

