"""Test suite for graph coloring algorithms."""

import pytest

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


class TestGraph:
    def test_empty_graph(self):
        g = Graph(n=0)
        assert g.n == 0
        assert g.num_edges == 0

    def test_single_vertex(self):
        g = Graph(n=1)
        assert g.degree(0) == 0

    def test_add_edge(self):
        g = Graph(n=3)
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        assert g.degree(0) == 1
        assert g.degree(1) == 2
        assert g.degree(2) == 1
        assert g.num_edges == 2

    def test_no_self_loop(self):
        g = Graph(n=2)
        g.add_edge(0, 0)
        assert g.num_edges == 0

    def test_from_edges(self):
        g = Graph.from_edges(4, [(0, 1), (1, 2), (2, 3)])
        assert g.n == 4
        assert g.num_edges == 3

    def test_edges_sorted(self):
        g = Graph.from_edges(3, [(2, 0), (1, 2)])
        assert g.edges == [(0, 2), (1, 2)]


class TestGreedy:
    def test_empty(self):
        g = Graph(n=0)
        r = greedy_coloring(g)
        assert r.num_colors == 0

    def test_single_vertex(self):
        g = Graph(n=1)
        r = greedy_coloring(g)
        assert r.num_colors == 1
        assert is_valid_coloring(g, r)

    def test_complete_graph(self):
        g = generate_complete_graph(5)
        r = greedy_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 5

    def test_bipartite(self):
        g = generate_bipartite(3, 3, edge_probability=1.0)
        r = greedy_coloring(g)
        assert is_valid_coloring(g, r)

    def test_valid_on_random(self):
        g = generate_random_graph(20, 0.3, seed=42)
        r = greedy_coloring(g)
        assert is_valid_coloring(g, r)


class TestWelshPowell:
    def test_complete_graph(self):
        g = generate_complete_graph(6)
        r = welsh_powell_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 6

    def test_valid_on_random(self):
        g = generate_random_graph(25, 0.4, seed=42)
        r = welsh_powell_coloring(g)
        assert is_valid_coloring(g, r)


class TestDSATUR:
    def test_bipartite_optimal(self):
        """DSATUR should find optimal 2-coloring for bipartite graphs."""
        g = generate_bipartite(5, 5, edge_probability=0.6, seed=42)
        r = dsatur_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 2

    def test_petersen_graph(self):
        """Petersen graph has chromatic number 3."""
        g = generate_petersen()
        r = dsatur_coloring(g)
        assert is_valid_coloring(g, r)
        # DSATUR heuristic should get close to 3
        assert r.num_colors <= 4

    def test_exact_petersen(self):
        """DSATUR exact should find chi(Petersen) = 3."""
        g = generate_petersen()
        r = dsatur_coloring(g, exact=True)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 3


class TestBacktracking:
    def test_empty(self):
        g = Graph(n=0)
        r = backtracking_coloring(g)
        assert r.num_colors == 0

    def test_complete_graph(self):
        g = generate_complete_graph(4)
        r = backtracking_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 4

    def test_cycle_even(self):
        """Even cycle has chromatic number 2."""
        g = generate_cycle(6)
        r = backtracking_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 2

    def test_cycle_odd(self):
        """Odd cycle has chromatic number 3."""
        g = generate_cycle(7)
        r = backtracking_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 3

    def test_petersen_optimal(self):
        """Backtracking should find chi(Petersen) = 3."""
        g = generate_petersen()
        r = backtracking_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 3


class TestGenerators:
    def test_random_graph_properties(self):
        g = generate_random_graph(20, 0.5, seed=42)
        assert g.n == 20
        assert g.num_edges > 0

    def test_erdos_renyi_exact_edges(self):
        from graph_coloring.utils import generate_erdos_renyi
        g = generate_erdos_renyi(10, 15, seed=42)
        assert g.n == 10
        assert g.num_edges == 15

    def test_bipartite_chromatic(self):
        """Non-empty bipartite graph should be 2-colorable."""
        g = generate_bipartite(4, 4, edge_probability=0.5, seed=42)
        r = dsatur_coloring(g)
        assert is_valid_coloring(g, r)
        assert r.num_colors == 2

    def test_complete_graph_chromatic(self):
        """K_n has chromatic number n."""
        for n in [3, 5, 7]:
            g = generate_complete_graph(n)
            r = greedy_coloring(g)
            assert r.num_colors == n
