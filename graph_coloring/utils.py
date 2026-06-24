"""Utility functions for graph generation and validation."""

from __future__ import annotations

import random
from typing import Optional, Set

from graph_coloring.models import ColorAssignment, Graph


def generate_random_graph(
    n: int,
    edge_probability: float = 0.3,
    seed: Optional[int] = None,
) -> Graph:
    """Generate a random graph using the Erdos-Renyi G(n, p) model.

    Each possible edge is included independently with probability p.

    Args:
        n: Number of vertices.
        edge_probability: Probability of each edge existing (0 to 1).
        seed: Random seed for reproducibility.

    Returns:
        A randomly generated Graph.
    """
    rng = random.Random(seed)
    g = Graph(n=n)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < edge_probability:
                g.add_edge(u, v)
    return g


def generate_erdos_renyi(
    n: int,
    m: int,
    seed: Optional[int] = None,
) -> Graph:
    """Generate a random graph with exactly m edges (uniform G(n, m) model).

    Args:
        n: Number of vertices.
        m: Number of edges.
        seed: Random seed for reproducibility.

    Returns:
        A randomly generated Graph with exactly m edges.
    """
    rng = random.Random(seed)
    max_edges = n * (n - 1) // 2
    m = min(m, max_edges)

    all_pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    selected = rng.sample(all_pairs, m)
    return Graph.from_edges(n, selected)


def generate_bipartite(
    n1: int,
    n2: int,
    edge_probability: float = 0.5,
    seed: Optional[int] = None,
) -> Graph:
    """Generate a random bipartite graph K_{n1, n2} with edge probability p.

    Bipartite graphs have chromatic number exactly 2 (if connected and non-empty).

    Args:
        n1: Size of the first partition.
        n2: Size of the second partition.
        edge_probability: Probability of each cross-partition edge.
        seed: Random seed for reproducibility.

    Returns:
        A randomly generated bipartite Graph.
    """
    rng = random.Random(seed)
    g = Graph(n=n1 + n2)
    for u in range(n1):
        for v in range(n1, n1 + n2):
            if rng.random() < edge_probability:
                g.add_edge(u, v)
    return g


def generate_complete_graph(n: int) -> Graph:
    """Generate the complete graph K_n (chromatic number = n)."""
    g = Graph(n=n)
    for u in range(n):
        for v in range(u + 1, n):
            g.add_edge(u, v)
    return g


def generate_cycle(n: int) -> Graph:
    """Generate a cycle graph C_n.

    Chromatic number: 2 if n is even, 3 if n is odd.
    """
    g = Graph(n=n)
    for i in range(n):
        g.add_edge(i, (i + 1) % n)
    return g


def generate_petersen() -> Graph:
    """Generate the Petersen graph (chromatic number = 3)."""
    g = Graph(n=10)
    # Outer cycle: 0-1-2-3-4
    for i in range(5):
        g.add_edge(i, (i + 1) % 5)
    # Inner star: 5-7-9-6-8-5
    inner = [5, 7, 9, 6, 8]
    for i in range(5):
        g.add_edge(inner[i], inner[(i + 1) % 5])
    # Spokes
    for i in range(5):
        g.add_edge(i, i + 5)
    return g


def is_valid_coloring(graph: Graph, result: ColorAssignment) -> bool:
    """Verify that no two adjacent vertices share the same color.

    Returns True if the coloring is valid (proper).
    """
    for u in range(graph.n):
        if u not in result.colors:
            return False
        for v in graph.neighbors(u):
            if v not in result.colors:
                return False
            if result.colors[u] == result.colors[v]:
                return False
    return True


def chromatic_number_estimate(graph: Graph) -> int:
    """Quick estimate of the chromatic number using DSATUR.

    This is an upper bound, not the exact value.
    """
    from graph_coloring.dsatur import dsatur_coloring
    return dsatur_coloring(graph).num_colors
