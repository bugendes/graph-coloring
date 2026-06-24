#!/usr/bin/env python3
"""Benchmark suite comparing graph coloring algorithms across different graph types.

Generates performance metrics (colors used, runtime, iterations) across:
  - Random graphs G(n, p) with varying density
  - Complete graphs K_n
  - Cycle graphs C_n (even and odd)
  - Bipartite graphs
  - The Petersen graph

Results are printed as a formatted table and optionally saved as CSV.
"""

from __future__ import annotations

import csv
import sys
import time
from dataclasses import dataclass, field
from typing import List

sys.path.insert(0, "..")

from graph_coloring import (
    Graph,
    greedy_coloring,
    dsatur_coloring,
    welsh_powell_coloring,
    backtracking_coloring,
    is_valid_coloring,
    generate_random_graph,
    generate_complete_graph,
    generate_cycle,
)
from graph_coloring.utils import generate_bipartite, generate_petersen


@dataclass
class BenchmarkResult:
    graph_name: str
    n: int
    m: int
    algorithm: str
    num_colors: int
    valid: bool
    runtime_ms: float
    iterations: int


def run_benchmark(
    graph: Graph,
    graph_name: str,
    algorithms: dict,
) -> List[BenchmarkResult]:
    """Run all algorithms on a single graph and collect results."""
    results = []
    for name, algo_fn in algorithms.items():
        t0 = time.perf_counter()
        result = algo_fn(graph)
        elapsed = (time.perf_counter() - t0) * 1000
        valid = is_valid_coloring(graph, result)
        results.append(BenchmarkResult(
            graph_name=graph_name,
            n=graph.n,
            m=graph.num_edges,
            algorithm=name,
            num_colors=result.num_colors,
            valid=valid,
            runtime_ms=round(elapsed, 3),
            iterations=result.iterations,
        ))
    return results


def main():
    algorithms = {
        "greedy": greedy_coloring,
        "welsh-powell": welsh_powell_coloring,
        "dsatur": dsatur_coloring,
        "backtracking": lambda g: backtracking_coloring(g),
    }

    test_graphs = []

    # Small structured graphs
    test_graphs.append(("K_5", generate_complete_graph(5)))
    test_graphs.append(("K_8", generate_complete_graph(8)))
    test_graphs.append(("C_6 (even)", generate_cycle(6)))
    test_graphs.append(("C_7 (odd)", generate_cycle(7)))
    test_graphs.append(("Petersen", generate_petersen()))
    test_graphs.append(("Bipartite 5x5", generate_bipartite(5, 5, 0.4, seed=42)))

    # Random graphs with varying density
    for n in [10, 20, 30]:
        for p in [0.2, 0.4, 0.6]:
            test_graphs.append(
                (f"G({n},{p})", generate_random_graph(n, p, seed=42))
            )

    all_results: List[BenchmarkResult] = []
    for name, g in test_graphs:
        print(f"  Running {name} (n={g.n}, m={g.num_edges})...")
        all_results.extend(run_benchmark(g, name, algorithms))

    # Print table
    header = f"{'Graph':<20} {'n':>4} {'m':>5} {'Algorithm':<15} {'Colors':>6} {'Valid':>5} {'Time(ms)':>9} {'Iter':>8}"
    print()
    print(header)
    print("-" * len(header))
    for r in all_results:
        print(
            f"{r.graph_name:<20} {r.n:>4} {r.m:>5} {r.algorithm:<15} "
            f"{r.num_colors:>6} {'  OK' if r.valid else 'FAIL':>5} "
            f"{r.runtime_ms:>9.3f} {r.iterations:>8}"
        )

    # Save CSV
    csv_path = "benchmark_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["graph", "n", "m", "algorithm", "colors", "valid", "time_ms", "iterations"])
        for r in all_results:
            writer.writerow([r.graph_name, r.n, r.m, r.algorithm, r.num_colors, r.valid, r.runtime_ms, r.iterations])
    print(f"
Results saved to {csv_path}")


if __name__ == "__main__":
    main()
