# file: degree_distribution.py
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import powerlaw
import json

EDGES_FILE = "edges.txt"

print("Φόρτωση γραφήματος...")
G = nx.read_edgelist(EDGES_FILE, nodetype=int, data=False)  # undirected

# Βαθμοί κόμβων
degrees = [d for _, d in G.degree()]
n = len(degrees)
k_max = max(degrees) if degrees else 0
print(f"Σύνολο κόμβων: {n}")
print(f"Μέγιστος βαθμός: {k_max}")

# Κατανομή βαθμών (count ανά k)
counter = Counter(degrees)
unique_k = np.array(sorted(counter.keys()))
counts = np.array([counter[k] for k in unique_k])

# --- Plot degree distribution σε log–log ---
plt.figure(figsize=(7,5))
plt.scatter(unique_k, counts, s=8, alpha=0.8)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Degree (k)")
plt.ylabel("Count P(k)")
plt.title("Degree Distribution (log–log)")
plt.grid(True, which="both", ls="--", lw=0.3)
plt.tight_layout()
plt.savefig("degree_distribution_loglog.png", dpi=300)


# --- Αποθήκευση κατανομής σε CSV για το report ---
import csv
with open("degree_distribution.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["k", "count"])
    for k, c in zip(unique_k, counts):
        w.writerow([int(k), int(c)])

# --- Power-law fitting (χωρίς επιπλέον σχήματα) ---
# Χρησιμοποιούμε discrete True γιατί οι βαθμοί είναι ακέραιοι.
# Το powerlaw θα εκτιμήσει αυτόματα το xmin (cutoff της ουράς).
fit = powerlaw.Fit(degrees, discrete=True, xmin=None, verbose=False)
gamma = fit.power_law.alpha
xmin = fit.power_law.xmin

# Σύγκριση με λογαριθμοκανονική για καλή πρακτική
R, p = fit.distribution_compare("power_law", "lognormal")

# Εκτύπωση καθαρών αποτελεσμάτων
print("\n— ΑΠΟΤΕΛΕΣΜΑΤΑ (f) —")
print(f"Estimated power-law exponent γ: {gamma:.4f}")
print(f"Estimated xmin (cutoff): {xmin}")
print(f"Comparison (power_law vs lognormal): R={R:.4f}, p={p:.4f}")
if p > 0.05:
    print("Συμπέρασμα: Το power law είναι ΠΙΘΑΝΟ (δεν απορρίπτεται).")
else:
    print("Συμπέρασμα: Ασθενής ένδειξη υπέρ power law (προσοχή στη μοντελοποίηση).")

# Αποθήκευση αποτελεσμάτων για το report
out = {
    "nodes": n,
    "k_max": int(k_max),
    "powerlaw_gamma": float(gamma),
    "powerlaw_xmin": int(xmin) if hasattr(xmin, "__int__") else xmin,
    "compare_R": float(R),
    "compare_p": float(p),
}
with open("degree_fit_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("\n✅ Αποθηκεύτηκαν τα αρχεία:")
print(" - degree_distribution_loglog.png")
print(" - degree_distribution.csv")
print(" - degree_fit_results.json")
