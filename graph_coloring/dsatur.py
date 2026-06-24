"""DSATUR (Degree of Saturation) graph coloring algorithm.

DSATUR (Brelaz, 1979) is a backtracking-free heuristic that dynamically
selects the next vertex based on its "saturation degree" — the number of
distinct colors already used among its neighbors.

Selection rule:
  1. Pick the uncolored vertex with the highest saturation degree.
  2. Ties are broken by highest uncolored degree, then lowest vertex ID.
  3. Assign the smallest available color.

For bipartite graphs, DSATUR is guaranteed to find the optimal 2-coloring.

Time complexity:  O(V^2) — at each of V steps, we scan V vertices.
Space complexity: O(V + E)

This implementation includes an optional exact mode that combines DSATUR
ordering with branch-and-bound backtracking for guaranteed optimality
on small graphs (n <= ~50).
"""

from __future__ import annotations

from typing import Dict, Optional, Set

from graph_coloring.models import ColorAssignment, Graph


def _saturation_degree(v: int, colors: Dict[int, int], graph: Graph) -> int:
    """Count distinct colors used by colored neighbors of v."""
    return len({colors[u] for u in graph.neighbors(v) if u in colors})


def dsatur_coloring(
    graph: Graph,
    exact: bool = False,
) -> ColorAssignment:
    """Color a graph using the DSATUR heuristic.

    Args:
        graph: The input graph.
        exact: If True, use DSATUR with backtracking for exact solution
               (only practical for small graphs).

    Returns:
        ColorAssignment with the coloring result.
    """
    if exact:
        return _dsatur_exact(graph)

    return _dsatur_heuristic(graph)


def _dsatur_heuristic(graph: Graph) -> ColorAssignment:
    """Pure DSATUR heuristic (no backtracking)."""
    colors: Dict[int, int] = {}
    iterations = 0
    uncolored = set(range(graph.n))

    while uncolored:
        iterations += 1
        # Select vertex with max saturation; break ties by max degree, then min ID
        best_v = max(
            uncolored,
            key=lambda v: (
                _saturation_degree(v, colors, graph),
                graph.degree(v),
                -v,
            ),
        )
        # Assign smallest available color
        used = {colors[u] for u in graph.neighbors(best_v) if u in colors}
        c = 0
        while c in used:
            c += 1
        colors[best_v] = c
        uncolored.remove(best_v)

    return ColorAssignment(
        colors=colors,
        algorithm="dsatur",
        num_colors=max(colors.values()) + 1 if colors else 0,
        iterations=iterations,
    )


def _dsatur_exact(graph: Graph) -> ColorAssignment:
    """DSATUR with branch-and-bound for exact chromatic number.

    Uses the DSATUR ordering as a heuristic within a backtracking search.
    Maintains a global upper bound and prunes branches that would exceed it.
    """
    best_colors: Dict[int, int] = {}
    best_num = graph.n  # worst case: every vertex gets its own color
    iterations = [0]

    def _upper_bound() -> int:
        """Greedy upper bound: Delta + 1."""
        if graph.n == 0:
            return 0
        return max(graph.degree(v) for v in range(graph.n)) + 1

    def _lower_bound(colors: Dict[int, int]) -> int:
        """Lower bound: number of colors used so + at least 1 if uncolored remain."""
        if not colors:
            return 1
        return max(colors.values()) + 1

    def _select_next(colors: Dict[int, int], uncolored: Set[int]) -> int:
        """Select the uncolored vertex with highest saturation."""
        return max(
            uncolored,
            key=lambda v: (
                _saturation_degree(v, colors, graph),
                graph.degree(v),
                -v,
            ),
        )

    def _backtrack(colors: Dict[int, int], uncolored: Set[int]) -> None:
        nonlocal best_colors, best_num
        iterations[0] += 1

        if not uncolored:
            num = max(colors.values()) + 1
            if num < best_num:
                best_num = num
                best_colors = dict(colors)
            return

        v = _select_next(colors, uncolored)
        used = {colors[u] for u in graph.neighbors(v) if u in colors}

        # Try colors from smallest to largest
        for c in range(min(best_num, len(used) + 1)):
            if c in used:
                continue
            colors[v] = c
            if max(colors.values()) + 1 >= best_num:
                # Pruning: this partial coloring already uses too many colors
                del colors[v]
                continue
            uncolored.remove(v)
            _backtrack(colors, uncolored)
            uncolored.add(v)
            del colors[v]

    _backtrack({}, set(range(graph.n)))

    return ColorAssignment(
        colors=best_colors,
        algorithm="dsatur-exact",
        num_colors=best_num,
        iterations=iterations[0],
    )
