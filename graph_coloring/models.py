"""Core data structures for graph coloring."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Set, Tuple


@dataclass
class Graph:
    """Undirected graph represented via adjacency lists.

    Vertices are identified by integer IDs (0-indexed).
    Edges are stored symmetrically: if (u, v) exists, v appears in adj[u]
    and u appears in adj[v].
    """

    n: int  # number of vertices
    adj: Dict[int, Set[int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for v in range(self.n):
            self.adj.setdefault(v, set())

    def add_edge(self, u: int, v: int) -> None:
        """Add an undirected edge between u and v."""
        if u == v:
            return  # no self-loops
        self.adj.setdefault(u, set()).add(v)
        self.adj.setdefault(v, set()).add(u)

    def neighbors(self, v: int) -> Set[int]:
        """Return the neighbor set of vertex v."""
        return self.adj.get(v, set())

    def degree(self, v: int) -> int:
        """Return the degree of vertex v."""
        return len(self.neighbors(v))

    @property
    def edges(self) -> List[Tuple[int, int]]:
        """Return all edges as sorted (u, v) pairs with u < v."""
        seen: Set[FrozenSet[int]] = set()
        result = []
        for u in self.adj:
            for v in self.adj[u]:
                edge = frozenset((u, v))
                if edge not in seen:
                    seen.add(edge)
                    result.append((min(u, v), max(u, v)))
        return sorted(result)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    @classmethod
    def from_edges(cls, n: int, edges: List[Tuple[int, int]]) -> Graph:
        """Construct a graph from an edge list."""
        g = cls(n=n)
        for u, v in edges:
            g.add_edge(u, v)
        return g

    def __repr__(self) -> str:
        return f"Graph(n={self.n}, edges={self.num_edges})"


@dataclass
class ColorAssignment:
    """Result of a graph coloring algorithm.

    Attributes:
        colors: mapping from vertex -> color index (0-indexed).
        algorithm: name of the algorithm used.
        num_colors: total number of distinct colors used (= chromatic upper bound).
        iterations: number of algorithm iterations (for analysis).
    """

    colors: Dict[int, int]
    algorithm: str
    num_colors: int
    iterations: int = 0

    def __post_init__(self) -> None:
        if not self.colors:
            self.num_colors = 0
        elif self.num_colors == 0:
            self.num_colors = max(self.colors.values()) + 1

    def color_classes(self) -> Dict[int, List[int]]:
        """Group vertices by their assigned color."""
        classes: Dict[int, List[int]] = {}
        for v, c in sorted(self.colors.items()):
            classes.setdefault(c, []).append(v)
        return classes

    def __repr__(self) -> str:
        return (
            f"ColorAssignment(algo={self.algorithm!r}, "
            f"colors={self.num_colors}, vertices={len(self.colors)})"
        )
