# Brain Network Analysis

This repository contains a small network-science project that analyzes a brain connectivity graph derived from the Princeton neuroanatomy dataset. It builds an undirected graph from reciprocal connections, computes basic graph metrics, and explores degree distributions, distance-connectivity relationships, and small-world structure.

## Overview

The project is designed to study the topology of a brain network using graph-theoretic tools. The workflow includes:

- constructing an undirected edge list from reciprocal connections
- computing global network statistics
- fitting the degree distribution to a power-law model
- plotting the nearest-neighbor degree relationship
- evaluating the relationship between spatial distance and connection probability
- approximating average path length and diameter

## Dataset

The project uses the following data files:

- `connections_princeton.csv`: original connectivity data with pairs of brain regions
- `coordinates.csv`: spatial coordinates for each node
- `edges.txt`: filtered undirected edge list used for analysis

## Repository structure

```text
.
├── analyze_network.py
├── create_edge_list.py
├── degree_distribution.py
├── distance_connectivity_plot.py
├── graph_distance_diameter.py
├── knn_plot.py
├── connections_princeton.csv
├── coordinates.csv
├── edges.txt
├── degree_distribution.csv
├── degree_fit_results.json
├── stats_e.json
├── degree_distribution_loglog.png
├── distance_connectivity_loglog.png
├── knn_loglog.png
├── README.md
├── requirements.txt
├── .gitignore
└── Assignment2_report.pdf
```

## Requirements

This project uses Python 3 and the following packages:

- `networkx`
- `numpy`
- `matplotlib`
- `pandas`
- `scipy`
- `powerlaw`

Install them with:

```bash
pip install -r requirements.txt
```

## Usage

Run the scripts in the following order:

1. Build the edge list from the raw connectivity file:

```bash
python create_edge_list.py
```

2. Compute the main graph statistics:

```bash
python analyze_network.py
```

3. Plot and analyze the degree distribution:

```bash
python degree_distribution.py
```

4. Plot the average nearest-neighbor degree:

```bash
python knn_plot.py
```

5. Estimate distance-based connectivity and graph diameter:

```bash
python graph_distance_diameter.py
python distance_connectivity_plot.py
```

## Output files

The scripts generate several outputs used for analysis and reporting:

- `edges.txt`: filtered undirected graph data
- `stats_e.json`: basic graph statistics
- `degree_distribution.csv`: degree counts
- `degree_fit_results.json`: power-law fitting summary
- `degree_distribution_loglog.png`: degree distribution plot
- `knn_loglog.png`: nearest-neighbor degree plot
- `distance_connectivity_loglog.png`: distance-connectivity plot

## Main findings

This analysis is intended to characterize the brain network as a sparse, spatially embedded graph with nontrivial topology. Typical questions addressed by the project include:

- whether the network is sparse or dense
- whether the degree distribution follows a power law
- whether edges are preferentially formed by degree correlations
- whether the graph shows small-world or ultra-small-world behavior
- how connection probability changes with spatial distance

## Notes

- The graph is treated as undirected.
- Reciprocal edges are retained to reduce duplicates and noise.
- Some computations use sampling or approximations for efficiency, especially for large-distance and diameter analyses.

## License

This project is provided for academic and research use. Add a license if you plan to publish it publicly on GitHub.

## GitHub publishing

Once the repository is ready, initialize the remote and push it to GitHub:

```bash
git remote add origin <your-github-repository-url>
git branch -M main
git push -u origin main
```

If you want, you can also connect this repository to a GitHub repo created from the browser and then run the push command afterward.
