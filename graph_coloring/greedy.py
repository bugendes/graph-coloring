"""Greedy graph coloring algorithm.

The greedy algorithm processes vertices in a specified order and assigns
each vertex the smallest color not used by its already-colored neighbors.

Time complexity:  O(V + E) — each edge examined at most once per endpoint.
Space complexity: O(V) for the color map.

This does NOT guarantee optimality. In the worst case, the greedy algorithm
can use up to Delta + 1 colors (where Delta is the maximum degree), while
the chromatic number could be much smaller.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from graph_coloring.models import ColorAssignment, Graph


def greedy_coloring(
    graph: Graph,
    vertex_order: Optional[List[int]] = None,
    label: str = "greedy",
) -> ColorAssignment:
    """Color a graph using the greedy strategy.

    Args:
        graph: The input graph.
        vertex_order: Optional custom vertex ordering. Defaults to ascending ID.
        label: Algorithm label for the result.

    Returns:
        ColorAssignment with the coloring result.
    """
    if vertex_order is None:
        vertex_order = list(range(graph.n))

    colors = {}
    iterations = 0

    for v in vertex_order:
        iterations += 1
        # Collect colors used by already-colored neighbors
        used = {colors[u] for u in graph.neighbors(v) if u in colors}
        # Assign the smallest available color
        c = 0
        while c in used:
            c += 1
        colors[v] = c

    return ColorAssignment(
        colors=colors,
        algorithm=label,
        num_colors=max(colors.values()) + 1 if colors else 0,
        iterations=iterations,
    )
