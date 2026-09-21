# file: create_edge_list.py
import pandas as pd

# 1. Φόρτωση του αρχείου
print("Φόρτωση connections_princeton.csv ...")
df = pd.read_csv("connections_princeton.csv")

print("Στήλες αρχείου:", df.columns.tolist())
print("Σύνολο γραμμών:", len(df))

# 2. Κρατάμε μόνο τις απαραίτητες στήλες (pre_root_id και post_root_id)
df = df[["pre_root_id", "post_root_id"]]

# 3. Δημιουργούμε ένα set με όλες τις συνδέσεις
edges_set = set(zip(df["pre_root_id"], df["post_root_id"]))

# 4. Φιλτράρουμε μόνο τις αμφίδρομες (reciprocal) συνδέσεις
reciprocal_edges = set()
for a, b in edges_set:
    if (b, a) in edges_set and a < b:  # a<b για να μην επαναλαμβάνεται η ίδια σύνδεση
        reciprocal_edges.add((a, b))

print(f"Αμφίδρομες συνδέσεις που βρέθηκαν: {len(reciprocal_edges):,}")

# 5. Αποθήκευση σε αρχείο edge-list
with open("edges.txt", "w") as f:
    for a, b in sorted(reciprocal_edges):
        f.write(f"{a} {b}\n")

print("✅ Το αρχείο edges.txt δημιουργήθηκε επιτυχώς!")

