# Graph Coloring Toolkit

A computational toolkit implementing four distinct algorithms for the **vertex coloring problem** — one of the foundational problems in combinatorial optimization and graph theory.

## The Problem

Given an undirected graph *G = (V, E)*, a **proper vertex coloring** assigns a color to each vertex such that no two adjacent vertices share the same color. The **chromatic number** χ(*G*) is the minimum number of colors required.

Graph coloring is **NP-complete** in general (Karp, 1972). No polynomial-time algorithm is known to find χ(*G*) for arbitrary graphs, and it is widely believed that none exists. This makes heuristic and exact approaches both practically and theoretically important.

## Algorithms

### Greedy Coloring

The simplest approach: process vertices in a fixed order, assigning each vertex the smallest color not used by its already-colored neighbors.

- **Time complexity:** O(V + E)
- **Color bound:** At most Δ + 1 colors (Δ = maximum vertex degree)
- **Optimality:** No guarantee. Vertex ordering dramatically affects quality — the same graph can yield colorings using 2 colors or n/2 colors depending on the order.

The greedy algorithm underpins compiler register allocation, where variables are vertices and interference edges connect variables live at the same program point.

### Welsh-Powell Heuristic

Welsh and Powell (1967) proposed sorting vertices by descending degree before applying the greedy strategy. This simple modification yields a provably better upper bound:

**Theorem:** χ(*G*) ≤ 1 + max_i min(deg(v_i), i − 1)

where v_1, v_2, ..., v_n is the degree-sorted order.

- **Time complexity:** O(V²) due to sorting and neighbor scanning
- **Practical advantage:** High-degree vertices are colored first, leaving low-degree vertices with more available colors. This reduces the total color count on most real-world graphs.

### DSATUR (Degree of Saturation)

Brelaz (1979) introduced a dynamic ordering strategy. Instead of fixing the order upfront, DSATUR selects the next vertex based on its **saturation degree** — the number of distinct colors already present among its neighbors.

**Selection rule at each step:**
1. Among uncolored vertices, pick the one with the highest saturation degree.
2. Break ties by highest uncolored degree, then lowest vertex ID.
3. Assign the smallest available color.

- **Time complexity:** O(V²) — each of V steps scans all remaining vertices
- **Special property:** DSATUR is **exact for bipartite graphs** — it always finds the optimal 2-coloring without backtracking.
- **Exact variant:** When combined with backtracking and branch-and-bound pruning, DSATUR finds the true chromatic number. The dynamic ordering accelerates pruning by revealing conflicts early.

### Backtracking (Exact Solver)

A depth-first search that tries all viable color assignments with aggressive pruning:

1. Maintain the best solution found so far (upper bound).
2. At each vertex, only try colors 0 through k−1 (where k is the current upper bound).
3. If a partial coloring already uses ≥ k colors, prune the branch.
4. Vertices are processed in descending-degree order for faster pruning.

- **Time complexity:** O(k^V) worst case, but pruning reduces this dramatically in practice.
- **Practical limit:** ~25 vertices for exact solutions within seconds.

## Mathematical Background

### Bounds on the Chromatic Number

| Bound | Formula | Notes |
|-------|---------|-------|
| Lower | χ(G) ≥ ω(G) | ω = clique number (largest complete subgraph) |
| Lower | χ(G) ≥ n / α(G) | α = independence number |
| Upper | χ(G) ≤ Δ + 1 | Greedy bound (Brook's theorem tightens this) |
| Upper | χ(G) ≤ Δ | Unless G is complete or an odd cycle (Brook, 1941) |

### Brook's Theorem

For any connected graph G that is neither a complete graph nor an odd cycle:

χ(G) ≤ Δ(G)

This is tight: greedy with Δ + 1 colors is never worse, but Brook's bound tells us we can usually do better.

### NP-Completeness

Determining whether χ(G) ≤ 3 is NP-complete (reduction from 3-SAT). This means:
- No known polynomial algorithm exists (unless P = NP).
- Approximation is hard: it is NP-hard to approximate χ(G) within n^{1−ε} for any ε > 0 (Zuckerman, 2007).

## Applications

**Register Allocation (Compilers):** Variables are graph vertices; edges connect variables that are simultaneously live. Colors map to physical registers. The greedy algorithm with graph coloring is used in GCC and LLVM.

**Map Coloring:** The Four Color Theorem (Appel & Haken, 1976) states that every planar graph has χ ≤ 4. Graph coloring algorithms verify and construct such colorings for geographic maps.

**Frequency Assignment:** Radio towers are vertices; edges connect towers that would interfere if using the same frequency. Minimizing colors minimizes the spectrum required.

**Scheduling:** Exam timetabling (vertices = exams, edges = shared students), sports league scheduling, and resource allocation all reduce to graph coloring.

**Network Analysis:** Community detection, conflict resolution in distributed systems, and Sudoku solving are all instances of graph coloring.

## Project Structure

```
graph_coloring/
├── __init__.py          # Public API
├── models.py            # Graph and ColorAssignment data structures
├── greedy.py            # Greedy coloring algorithm
├── welsh_powell.py      # Welsh-Powell heuristic
├── dsatur.py            # DSATUR heuristic + exact variant
├── backtracking.py      # Exact backtracking solver
├── utils.py             # Graph generators and validation
└── visualization.py     # Matplotlib-based graph visualization
benchmarks/
└── benchmark.py         # Comparative benchmarking suite
tests/
└── test_algorithms.py   # Algorithm correctness tests
```
