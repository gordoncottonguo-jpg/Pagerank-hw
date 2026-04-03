import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# 1. Generate a fixed random graph
# -----------------------------
N = 1000
alpha = 0.85
seed = 42

rng = np.random.default_rng(seed)

# Barabasi-Albert graph, then convert to directed by replacing each undirected edge with two directed edges
G_und = nx.barabasi_albert_graph(N, 4, seed=seed)
G = G_und.to_directed()

# adjacency list
successors = [list(G.successors(i)) for i in range(N)]

# -----------------------------
# 2. Build PageRank transition matrix M = alpha P + (1-alpha) Delta
# -----------------------------
Delta = (np.ones((N, N)) - np.eye(N)) / (N - 1)
P = np.zeros((N, N), dtype=float)

for i in range(N):
    nbrs = successors[i]
    if len(nbrs) > 0:
        P[i, nbrs] = 1.0 / len(nbrs)
    else:
        # handle dangling node with Delta-row convention
        P[i, :] = Delta[i, :]

M = alpha * P + (1.0 - alpha) * Delta

# numerical safety
M = M / M.sum(axis=1, keepdims=True)

# -----------------------------
# 3. Power iteration
# -----------------------------
def power_iteration(M, tol=1e-12, max_iter=20000):
    n = M.shape[0]
    pi = np.ones(n) / n
    history = []

    for k in range(max_iter):
        pi_next = pi @ M
        err = np.linalg.norm(pi_next - pi, ord=1)
        history.append((k + 1, err))
        pi = pi_next
        if err < tol:
            break

    pi = pi / pi.sum()
    hist_df = pd.DataFrame(history, columns=["iteration", "l1_error"])
    return pi, hist_df

pi_m, conv_df = power_iteration(M)

# -----------------------------
# 4. Random walk simulation for lengths 10^3 ... 10^7
# -----------------------------
def random_other_node(cur, n, rng):
    j = rng.integers(n - 1)
    return j if j < cur else j + 1

def pagerank_step(cur, successors, alpha, rng, n):
    # teleport with probability (1-alpha)
    if rng.random() < (1.0 - alpha):
        return random_other_node(cur, n, rng)

    nbrs = successors[cur]
    if len(nbrs) == 0:
        return random_other_node(cur, n, rng)

    return nbrs[rng.integers(len(nbrs))]

def simulate_snapshots(successors, lengths, alpha=0.85, seed=42):
    rng = np.random.default_rng(seed)
    n = len(successors)
    counts = np.zeros(n, dtype=np.int64)
    current = rng.integers(n)
    snapshots = {}

    targets = sorted(lengths)
    target_idx = 0
    max_steps = targets[-1]

    for t in range(1, max_steps + 1):
        counts[current] += 1
        if t == targets[target_idx]:
            snapshots[t] = counts / counts.sum()
            target_idx += 1
            if target_idx == len(targets):
                break
        current = pagerank_step(current, successors, alpha, rng, n)

    return snapshots

lengths = [10**3, 10**4, 10**5, 10**6, 10**7]
walk_snapshots = simulate_snapshots(successors, lengths, alpha=alpha, seed=seed)

# -----------------------------
# 5. Ranking and permutation distance
#    We choose Spearman footrule:
#    F(sigma, tau) = sum_i |rank_sigma(i) - rank_tau(i)|
# -----------------------------
def order_from_scores(scores):
    return np.argsort(-scores)

def ranks_from_order(order):
    r = np.empty_like(order)
    r[order] = np.arange(len(order))
    return r

def spearman_footrule(order1, order2):
    r1 = ranks_from_order(order1)
    r2 = ranks_from_order(order2)
    return np.abs(r1 - r2).sum()

order_m = order_from_scores(pi_m)

rows = []
for L in lengths:
    pi_s = walk_snapshots[L]
    order_s = order_from_scores(pi_s)

    rows.append({
        "walk_length": L,
        "l1_distance": np.linalg.norm(pi_s - pi_m, ord=1),
        "l2_distance": np.linalg.norm(pi_s - pi_m, ord=2),
        "spearman_footrule": spearman_footrule(order_m, order_s),
        "top10_power": list(order_m[:10]),
        "top10_walk": list(order_s[:10]),
    })

results_df = pd.DataFrame(rows)

# -----------------------------
# 6. Save tables
# -----------------------------
conv_df.to_csv("pagerank_power_convergence.csv", index=False)
results_df.to_csv("pagerank_comparison.csv", index=False)

top_nodes_df = pd.DataFrame({
    "rank": np.arange(1, 21),
    "node": order_m[:20],
    "pagerank_score": pi_m[order_m[:20]]
})
top_nodes_df.to_csv("pagerank_top20_power.csv", index=False)

# -----------------------------
# 7. Plots
# -----------------------------
plt.figure(figsize=(7, 4))
plt.plot(conv_df["iteration"], conv_df["l1_error"])
plt.yscale("log")
plt.xlabel("Iteration")
plt.ylabel("L1 error")
plt.title("Power iteration convergence")
plt.tight_layout()
plt.savefig("pagerank_power_convergence.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(results_df["walk_length"], results_df["spearman_footrule"], marker="o")
plt.xscale("log")
plt.xlabel("Walk length")
plt.ylabel("Spearman footrule distance")
plt.title("Ranking distance: power iteration vs random walk")
plt.tight_layout()
plt.savefig("pagerank_ranking_distance.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(results_df["walk_length"], results_df["l1_distance"], marker="o", label="L1")
plt.plot(results_df["walk_length"], results_df["l2_distance"], marker="s", label="L2")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Walk length")
plt.ylabel("Distance")
plt.title("Distribution distance: power iteration vs random walk")
plt.legend()
plt.tight_layout()
plt.savefig("pagerank_distribution_distance.png", dpi=200)
plt.close()

# scatter for the longest walk
pi_s_long = walk_snapshots[10**7]
plt.figure(figsize=(5.5, 5.5))
plt.scatter(pi_m, pi_s_long, s=10, alpha=0.6)
mn = min(pi_m.min(), pi_s_long.min())
mx = max(pi_m.max(), pi_s_long.max())
plt.plot([mn, mx], [mn, mx], "r--", linewidth=1)
plt.xlabel("Power iteration PageRank")
plt.ylabel("Random walk frequency (10^7)")
plt.title("Stationary distribution comparison")
plt.tight_layout()
plt.savefig("pagerank_scatter_1e7.png", dpi=200)
plt.close()

print("Done.")
print(results_df[["walk_length", "l1_distance", "l2_distance", "spearman_footrule"]])
print("\nTop 10 nodes from power iteration:")
print(order_m[:10])