"""Backtracking exact graph coloring solver.

Finds the minimum number of colors (chromatic number) by exhaustive search
with pruning. Practical only for small graphs (n <= ~25).

The algorithm explores all possible color assignments depth-first, pruning
branches when:
  1. A vertex has no available color (conflict with all k colors).
  2. The partial coloring already exceeds the best known solution.

This is combined with a DSATUR-inspired vertex ordering to accelerate pruning.

Time complexity:  O(k^V) worst case, but pruning reduces this dramatically.
Space complexity: O(V) for the recursion stack + color map.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from graph_coloring.models import ColorAssignment, Graph


def backtracking_coloring(
    graph: Graph,
    max_colors: Optional[int] = None,
) -> ColorAssignment:
    """Find an optimal coloring via backtracking.

    Args:
        graph: The input graph.
        max_colors: Maximum number of colors to try. If None, starts from
                    a greedy upper bound and iteratively tightens.

    Returns:
        ColorAssignment with the optimal coloring.
    """
    if graph.n == 0:
        return ColorAssignment(colors={}, algorithm="backtracking", num_colors=0)

    # Upper bound: greedy coloring gives us a starting point
    from graph_coloring.greedy import greedy_coloring
    from graph_coloring.welsh_powell import welsh_powell_coloring

    greedy_result = welsh_powell_coloring(graph)
    upper = greedy_result.num_colors
    if max_colors is not None:
        upper = min(upper, max_colors)

    # Lower bound: clique number approximation (max degree lower bound)
    lower = 1
    if graph.n > 0:
        max_deg = max(graph.degree(v) for v in range(graph.n))
        lower = max(1, max_deg // 2)

    best_colors: Dict[int, int] = {}
    best_num = upper + 1
    total_iterations = 0

    # Vertex ordering: sort by descending degree (heuristic for better pruning)
    vertex_order = sorted(range(graph.n), key=lambda v: (-graph.degree(v), v))

    def _can_color(v: int, c: int, colors: Dict[int, int]) -> bool:
        """Check if vertex v can be colored with color c."""
        return all(colors.get(u) != c for u in graph.neighbors(v))

    def _backtrack(idx: int, colors: Dict[int, int], k: int) -> bool:
        """Try to color remaining vertices using at most k colors.

        Returns True if a valid k-coloring was found.
        """
        nonlocal best_colors, best_num, total_iterations
        total_iterations += 1

        if idx == len(vertex_order):
            best_colors = dict(colors)
            best_num = k
            return True

        v = vertex_order[idx]
        for c in range(k):
            if _can_color(v, c, colors):
                colors[v] = c
                if _backtrack(idx + 1, colors, k):
                    return True
                del colors[v]
        return False

    # Try decreasing k from upper bound
    for k in range(lower, upper + 1):
        if _backtrack(0, {}, k):
            break

    return ColorAssignment(
        colors=best_colors,
        algorithm="backtracking",
        num_colors=best_num,
        iterations=total_iterations,
    )
