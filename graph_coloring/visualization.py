"""Visualization utilities for graph coloring results.

Requires matplotlib. NetworkX is used as an optional layout backend.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from graph_coloring.models import ColorAssignment, Graph


# Distinct color palette (colorblind-friendly)
PALETTE = [
    "#E6194B", "#3CB44B", "#4363D8", "#F58231", "#911EB4",
    "#42D4F4", "#F032E6", "#BFEF45", "#FABED4", "#469990",
    "#DCBEFF", "#9A6324", "#800000", "#AAFFC3", "#808000",
    "#FFD8B1", "#000075", "#A9A9A9", "#FFFFFF", "#000000",
]


def _circular_layout(graph: Graph) -> Dict[int, Tuple[float, float]]:
    """Compute a circular layout for the graph vertices."""
    import math
    n = graph.n
    if n == 0:
        return {}
    if n == 1:
        return {0: (0.0, 0.0)}
    return {
        v: (math.cos(2 * math.pi * v / n), math.sin(2 * math.pi * v / n))
        for v in range(n)
    }


def _spring_layout(graph: Graph, iterations: int = 50) -> Dict[int, Tuple[float, float]]:
    """Simple force-directed (spring) layout algorithm.

    Repulsive forces between all pairs, attractive forces along edges.
    """
    import math
    import random
    rng = random.Random(42)
    n = graph.n
    if n == 0:
        return {}
    # Initialize random positions
    pos = {v: (rng.uniform(-1, 1), rng.uniform(-1, 1)) for v in range(n)}
    k = math.sqrt(4.0 / max(n, 1))  # optimal distance

    for _ in range(iterations):
        disp = {v: [0.0, 0.0] for v in range(n)}

        # Repulsive forces
        for u in range(n):
            for v in range(u + 1, n):
                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                dist = max(math.sqrt(dx * dx + dy * dy), 0.01)
                force = k * k / dist
                fx = dx / dist * force
                fy = dy / dist * force
                disp[u][0] += fx
                disp[u][1] += fy
                disp[v][0] -= fx
                disp[v][1] -= fy

        # Attractive forces
        for u in graph.adj:
            for v in graph.adj[u]:
                if v > u:
                    dx = pos[u][0] - pos[v][0]
                    dy = pos[u][1] - pos[v][1]
                    dist = max(math.sqrt(dx * dx + dy * dy), 0.01)
                    force = dist * dist / k
                    fx = dx / dist * force
                    fy = dy / dist * force
                    disp[u][0] -= fx
                    disp[u][1] -= fy
                    disp[v][0] += fx
                    disp[v][1] += fy

        # Update positions with cooling
        temp = 0.1 * (1 - _ / iterations)
        for v in range(n):
            d = math.sqrt(disp[v][0] ** 2 + disp[v][1] ** 2)
            if d > 0:
                scale = min(d, temp) / d
                pos[v] = (
                    pos[v][0] + disp[v][0] * scale,
                    pos[v][1] + disp[v][1] * scale,
                )

    return pos


def visualize_coloring(
    graph: Graph,
    result: ColorAssignment,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    layout: str = "spring",
    figsize: Tuple[int, int] = (10, 8),
) -> None:
    """Visualize a graph coloring result.

    Args:
        graph: The input graph.
        result: The coloring result.
        title: Optional plot title.
        save_path: If provided, save the figure to this path instead of displaying.
        layout: Layout algorithm: 'spring' or 'circular'.
        figsize: Figure size in inches.
    """
    if not HAS_MATPLOTLIB:
        print("matplotlib not installed — skipping visualization.")
        return

    if layout == "circular":
        pos = _circular_layout(graph)
    else:
        pos = _spring_layout(graph)

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # Draw edges
    for u, v in graph.edges:
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        ax.plot(x, y, color="#CCCCCC", linewidth=0.8, zorder=1)

    # Draw vertices
    for v in range(graph.n):
        color_idx = result.colors.get(v, 0) % len(PALETTE)
        ax.scatter(
            pos[v][0], pos[v][1],
            c=PALETTE[color_idx],
            s=300,
            edgecolors="black",
            linewidths=0.5,
            zorder=2,
        )
        ax.annotate(
            str(v),
            (pos[v][0], pos[v][1]),
            ha="center", va="center",
            fontsize=8, fontweight="bold",
            zorder=3,
        )

    # Legend
    color_classes = result.color_classes()
    patches = []
    for c in sorted(color_classes.keys()):
        patches.append(
            mpatches.Patch(color=PALETTE[c % len(PALETTE)], label=f"Color {c}")
        )
    ax.legend(handles=patches, loc="upper left", fontsize=8)

    algo_label = result.algorithm or "unknown"
    default_title = f"{algo_label} coloring — {result.num_colors} colors, {graph.n} vertices"
    ax.set_title(title or default_title, fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()
