# PageRank: Modeling and Simulation

This repository contains my course project on **PageRank as a Markov chain on a graph**.

The project studies how PageRank can be computed and approximated in two different ways:

1. **Power iteration**
2. **Random-walk simulation**

It follows the assignment requirements for the course project *“PageRank : modélisation et simulation”*.

---

## Project objective

The purpose of this project is to:

- generate a random graph,
- build the modified PageRank transition matrix,
- compute the stationary distribution by power iteration,
- simulate random walks of different lengths,
- compare the resulting rankings using numerical and ranking distances.

The PageRank transition matrix is defined as

\[
M = \alpha P + (1-\alpha)\Delta
\]

with \(\alpha = 0.85\), where \(P\) is the graph-based transition matrix and \(\Delta\) is the teleportation matrix.

---

## Repository contents

### Main code
- `pagerank.py` — main Python script for graph generation, power iteration, random-walk simulation, ranking comparison, and figure export

### Report
- `pagerank_report.markdown` — written report in Markdown format

### Results
All generated outputs are stored in the `results/` folder:

#### CSV files
- `pagerank_comparison.csv` — comparison between power iteration and random walk for different walk lengths
- `pagerank_power_convergence.csv` — convergence history of the power iteration method
- `pagerank_top20_power.csv` — top 20 ranked nodes according to the power iteration result

#### Figures
- `pagerank_distribution_distance.png` — distribution distance between power iteration and random walk
- `pagerank_power_convergence.png` — convergence curve of power iteration
- `pagerank_ranking_distance.png` — ranking distance between methods
- `image-1.png`, `image-2.png`, `image.png` — additional figures used in the project

---

## Methodology

The project follows these steps:

1. Generate a fixed random graph of size around 1000
2. Construct the PageRank transition matrix
3. Compute the stationary distribution using power iteration
4. Simulate random walks of length \(10^3, 10^4, 10^5, 10^6, 10^7\)
5. Estimate visit frequencies from the simulated walks
6. Compare the rankings obtained from both methods

The comparison is based on:

- \(L^1\) distance
- \(L^2\) distance
- Spearman footrule distance

---

## Main findings

The experimental results show that:

- power iteration converges quickly,
- random-walk estimates improve as the walk length increases,
- both probability-distance measures and ranking-distance measures decrease with longer walks,
- the top-ranked nodes become stable relatively early.

Example results from the final experiment include:

- \(L^1\) distance decreases from about **0.8693** at \(10^3\) steps to **0.0084** at \(10^7\) steps
- \(L^2\) distance decreases from about **0.0360** to **0.00035**
- Spearman footrule distance decreases from **295520** to **18080**

These results suggest that long random walks provide a good empirical approximation of the PageRank stationary distribution.

---

## How to run

Install dependencies first:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python pagerank.py
```

This will reproduce the main PageRank computation and generate result files.

---

## Reproducibility

This repository is intended to be reproducible:

- the code is provided in a single script,
- the generated CSV files are included,
- the output figures are included,
- the report is included in Markdown format.

---

