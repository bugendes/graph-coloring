#!/usr/bin/env python3
"""Graph Coloring Toolkit — interactive demo.

Demonstrates all four coloring algorithms on sample graphs.
"""

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
from graph_coloring.visualization import visualize_coloring


def demo():
    print("=" * 60)
    print("  Graph Coloring Toolkit — Algorithm Comparison")
    print("=" * 60)

    graphs = [
        ("Complete Graph K_6", generate_complete_graph(6)),
        ("Cycle C_7 (odd)", generate_cycle(7)),
        ("Petersen Graph", generate_petersen()),
        ("Bipartite 5x5", generate_bipartite(5, 5, 0.5, seed=42)),
        ("Random G(20, 0.3)", generate_random_graph(20, 0.3, seed=42)),
    ]

    algorithms = {
        "greedy": greedy_coloring,
        "welsh-powell": welsh_powell_coloring,
        "dsatur": dsatur_coloring,
        "backtracking": backtracking_coloring,
    }

    for graph_name, g in graphs:
        print(f"\n--- {graph_name} (n={g.n}, m={g.num_edges}) ---")
        for algo_name, algo_fn in algorithms.items():
            result = algo_fn(g)
            valid = is_valid_coloring(g, result)
            status = "OK" if valid else "FAIL"
            print(
                f"  {algo_name:<15} -> {result.num_colors} colors  "
                f"[{status}]  ({result.iterations} iterations)"
            )

    # Generate visualization for the Petersen graph
    print("\nGenerating visualization for Petersen graph (DSATUR)...")
    g = generate_petersen()
    result = dsatur_coloring(g)
    visualize_coloring(g, result, save_path="petersen_dsatur.png")
    print("Saved: petersen_dsatur.png")

    # Generate visualization for a random graph (backtracking)
    print("Generating visualization for random graph (backtracking)...")
    g = generate_random_graph(12, 0.35, seed=42)
    result = backtracking_coloring(g)
    visualize_coloring(g, result, save_path="random_backtracking.png")
    print("Saved: random_backtracking.png")


if __name__ == "__main__":
    demo()
