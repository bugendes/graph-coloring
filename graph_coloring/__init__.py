"""Graph Coloring Toolkit — multiple algorithms for the vertex coloring problem."""

from graph_coloring.models import Graph, ColorAssignment
from graph_coloring.greedy import greedy_coloring
from graph_coloring.dsatur import dsatur_coloring
from graph_coloring.welsh_powell import welsh_powell_coloring
from graph_coloring.backtracking import backtracking_coloring
from graph_coloring.utils import (
    generate_random_graph,
    generate_erdos_renyi,
    generate_complete_graph,
    generate_cycle,
    generate_bipartite,
    generate_petersen,
    chromatic_number_estimate,
    is_valid_coloring,
)

__all__ = [
    "Graph",
    "ColorAssignment",
    "greedy_coloring",
    "dsatur_coloring",
    "welsh_powell_coloring",
    "backtracking_coloring",
    "generate_random_graph",
    "generate_erdos_renyi",
    "generate_complete_graph",
    "generate_cycle",
    "generate_bipartite",
    "generate_petersen",
    "chromatic_number_estimate",
    "is_valid_coloring",
]
