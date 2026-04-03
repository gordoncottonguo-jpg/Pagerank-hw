# pagerank-markov-simulation
PageRank modeling and simulation using Markov chains

# PageRank Modeling and Simulation with Markov Chains

## Project overview
This repository studies PageRank as a Markov chain on a graph.

The project compares two approaches for estimating node importance:
- power iteration,
- random-walk simulation.

The goal is to understand how the empirical visit-frequency distribution from random walks approaches the stationary distribution computed by power iteration.

## Research question
For a fixed random graph, how close is the empirical PageRank vector obtained from random-walk simulation to the stationary PageRank vector obtained by power iteration as the walk length increases?

## Model
The PageRank transition matrix is defined by

\[
M = \alpha P + (1-\alpha)\Delta
\]

where:
- \(P\) is the transition matrix of the graph-based random walk,
- \(\Delta\) is the teleportation matrix,
- \(\alpha = 0.85\).

This modification makes the Markov chain more stable and avoids issues caused by disconnected or poorly connected graph structure.

## Method
The project combines:
- probabilistic modeling of PageRank as a finite-state Markov chain,
- computation of the stationary distribution by power iteration,
- random-walk simulation for lengths \(10^3, 10^4, 10^5, 10^6, 10^7\),
- comparison using \(L^1\) distance, \(L^2\) distance, and Spearman footrule distance,
- reproducible Python code, tables, and figures.

## Main findings
Based on the current computation:
- power iteration converges quickly and provides a stable reference PageRank vector,
- the random-walk estimate improves steadily as the walk length increases,
- the Top-10 ranking becomes very close to the power-iteration result from \(10^4\) onward,
- from \(10^5\) onward, the Top-10 ranking is almost stable.

More specifically:
- \(L^1\) distance decreases from **0.8693** at \(10^3\) steps to **0.0084** at \(10^7\) steps,
- \(L^2\) distance decreases from **0.0360** to **0.00035**,
- Spearman footrule distance decreases from **295520** to **18080**.

## Rule of thumb
Based on the current experiment:
- short random walks are too noisy for reliable ranking,
- medium-length random walks already recover the most important nodes well,
- long random walks provide a close approximation to the power-iteration PageRank vector.

## Repository structure
```text
pagerank-markov-simulation/
├── README.md
├── pagerank.py
├── pagerank_report.markdown
└── report/
    ├── pagerank_report.markdown
    ├── pagerank_report.pdf
    ├── image-1.png
    ├── image-2.png
    └── image.png
└── results/
    ├── pagerank_comparison.csv
    ├── pagerank_power_convergence.csv
    ├── pagerank_top20_power.csv
    ├── pagerank_distribution_distance.png
    ├── pagerank_power_convergence.png
    └── pagerank_ranking_distance.png
```

## Output
The repository includes:
- convergence results for power iteration,
- distribution-level comparison between power iteration and random walk,
- ranking-distance comparison,
- top-ranked nodes under the power-iteration solution,
- a written report summarizing the theoretical background, implementation, and findings.


