# file: graph_distance_diameter.py
import networkx as nx
import random
import math

print("Φόρτωση γραφήματος...")
G = nx.read_edgelist("edges.txt", nodetype=int, data=False)

# --- Μεγαλύτερο συνδεδεμένο component ---
if not nx.is_connected(G):
    largest_cc = max(nx.connected_components(G), key=len)
    Gc = G.subgraph(largest_cc).copy()
    print(f"Το γράφημα δεν είναι πλήρως συνδεδεμένο. "
          f"Υπολογισμοί στο μεγαλύτερο component ({len(Gc)} nodes).")
else:
    Gc = G
    print("Το γράφημα είναι συνδεδεμένο.")

# --- Διάμετρος (με προσέγγιση BFS από πολλούς κόμβους) ---
def approximate_diameter(G, samples=300):
    nodes = list(G.nodes())
    sample_nodes = random.sample(nodes, min(samples, len(nodes)))
    max_dist = 0
    for node in sample_nodes:
        lengths = nx.single_source_shortest_path_length(G, node)
        local_max = max(lengths.values())
        if local_max > max_dist:
            max_dist = local_max
    return max_dist

# --- Μέση απόσταση με sampling ---
def approximate_avg_distance(G, samples=500):
    nodes = list(G.nodes())
    sample_nodes = random.sample(nodes, min(samples, len(nodes)))
    total = 0
    count = 0
    for node in sample_nodes:
        lengths = nx.single_source_shortest_path_length(G, node)
        total += sum(lengths.values())
        count += len(lengths) - 1
    return total / count

print("Υπολογισμός average shortest path length (με sampling)...")
avg_distance = approximate_avg_distance(Gc, samples=500)

print("Υπολογισμός διαμέτρου (προσέγγιση)...")
diameter = approximate_diameter(Gc, samples=300)

# --- Ερμηνεία Small-world ---
N = Gc.number_of_nodes()
expected_small = math.log(N)
expected_ultra = math.log(math.log(N))

if avg_distance <= 2 * expected_ultra:
    world_type = "Ultra-small world"
elif avg_distance <= 2 * expected_small:
    world_type = "Small-world"
else:
    world_type = "None"

print("\n— ΑΠΟΤΕΛΕΣΜΑΤΑ (g) —")
print(f"Average distance (ℓ): {avg_distance:.3f}")
print(f"Diameter (approx): {diameter}")
print(f"log(N) ≈ {expected_small:.2f}, log(log(N)) ≈ {expected_ultra:.2f}")
print(f"Κατηγοριοποίηση: {world_type}")
