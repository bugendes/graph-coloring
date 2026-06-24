"""Welsh-Powell graph coloring algorithm.

The Welsh-Powell algorithm (1967) sorts vertices by descending degree, then
greedily assigns colors. This heuristic tends to produce fewer colors than
naive greedy ordering.

Upper bound: uses at most Delta + 1 colors (Delta = max degree).
Theorem (Welsh-Powell): chi(G) <= 1 + max_{v in V} min(deg(v), |N(v)|)

Time complexity:  O(V^2) due to the degree-based sorting and neighbor checks.
Space complexity: O(V + E)
"""

from __future__ import annotations

from graph_coloring.models import ColorAssignment, Graph


def welsh_powell_coloring(graph: Graph) -> ColorAssignment:
    """Color a graph using the Welsh-Powell heuristic.

    Vertices are processed in descending order of degree. For each vertex,
    the smallest color not conflicting with already-colored neighbors is used.

    Args:
        graph: The input graph.

    Returns:
        ColorAssignment with the coloring result.
    """
    # Sort vertices by descending degree (break ties by vertex ID)
    order = sorted(range(graph.n), key=lambda v: (-graph.degree(v), v))

    colors = {}
    iterations = 0

    for v in order:
        iterations += 1
        used = {colors[u] for u in graph.neighbors(v) if u in colors}
        c = 0
        while c in used:
            c += 1
        colors[v] = c

    return ColorAssignment(
        colors=colors,
        algorithm="welsh-powell",
        num_colors=max(colors.values()) + 1 if colors else 0,
        iterations=iterations,
    )
