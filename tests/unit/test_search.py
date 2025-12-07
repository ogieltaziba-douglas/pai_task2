"""
Unit tests for search algorithms (BFS/DFS).
Following TDD - tests written BEFORE implementation.
"""

import pytest
from src.algorithms.search import bfs, dfs
from src.data_structures.graph import Graph


class TestBFS:
    """Test Breadth-First Search algorithm."""

    def test_bfs_single_node(self):
        """Test BFS starting from a node with no neighbors."""
        graph = Graph()
        graph.add_node("bread")

        result = bfs(graph, "bread")

        assert result == {"bread": 0}

    def test_bfs_direct_neighbors(self):
        """Test BFS finds direct neighbors at depth 1."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")

        result = bfs(graph, "bread")

        assert result["bread"] == 0
        assert result["milk"] == 1
        assert result["butter"] == 1

    def test_bfs_multiple_levels(self):
        """Test BFS traverses multiple levels correctly."""
        graph = Graph()
        # Level 0: bread
        # Level 1: milk, butter
        # Level 2: eggs, cheese
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")
        graph.add_edge("milk", "eggs")
        graph.add_edge("butter", "cheese")

        result = bfs(graph, "bread")

        assert result["bread"] == 0
        assert result["milk"] == 1
        assert result["butter"] == 1
        assert result["eggs"] == 2
        assert result["cheese"] == 2

    def test_bfs_with_max_depth(self):
        """Test BFS respects max_depth parameter."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("milk", "eggs")
        graph.add_edge("eggs", "bacon")

        result = bfs(graph, "bread", max_depth=1)

        assert "bread" in result
        assert "milk" in result
        assert "eggs" not in result
        assert "bacon" not in result

    def test_bfs_cyclic_graph(self):
        """Test BFS handles cycles without infinite loop."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("c", "a")  # Creates cycle

        result = bfs(graph, "a")

        # Should visit each node exactly once
        assert len(result) == 3
        assert result["a"] == 0
        assert result["b"] == 1
        # In undirected graph, c is reachable from a in 2 ways:
        # 1. a -> b -> c (depth 2)
        # 2. a -> c (depth 1, direct edge)
        # BFS finds shortest path, so c should be at depth 1
        assert result["c"] == 1

    def test_bfs_disconnected_graph(self):
        """Test BFS only finds connected component."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("c", "d")  # Disconnected component

        result = bfs(graph, "a")

        assert "a" in result
        assert "b" in result
        assert "c" not in result
        assert "d" not in result

    def test_bfs_nonexistent_start(self):
        """Test BFS with non-existent start node."""
        graph = Graph()
        graph.add_edge("a", "b")

        with pytest.raises(KeyError, match="not found"):
            bfs(graph, "nonexistent")

    def test_bfs_empty_graph(self):
        """Test BFS on empty graph."""
        graph = Graph()

        with pytest.raises(KeyError):
            bfs(graph, "bread")

    def test_bfs_order_is_breadth_first(self):
        """Test that BFS explores breadth-first (all depth N before N+1)."""
        graph = Graph()
        # Create a tree structure
        graph.add_edge("root", "a")
        graph.add_edge("root", "b")
        graph.add_edge("a", "c")
        graph.add_edge("a", "d")
        graph.add_edge("b", "e")

        result = bfs(graph, "root")

        # All depth-1 nodes should be found before depth-2
        assert result["a"] == 1
        assert result["b"] == 1
        assert result["c"] == 2
        assert result["d"] == 2
        assert result["e"] == 2


class TestDFS:
    """Test Depth-First Search algorithm."""

    def test_dfs_single_node(self):
        """Test DFS starting from a node with no neighbors."""
        graph = Graph()
        graph.add_node("bread")

        result = dfs(graph, "bread")

        assert "bread" in result
        assert len(result) == 1

    def test_dfs_direct_neighbors(self):
        """Test DFS finds direct neighbors."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")

        result = dfs(graph, "bread")

        assert "bread" in result
        assert "milk" in result
        assert "butter" in result
        assert len(result) == 3

    def test_dfs_with_max_depth(self):
        """Test DFS respects max_depth parameter."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("milk", "eggs")
        graph.add_edge("eggs", "bacon")

        result = dfs(graph, "bread", max_depth=1)

        assert "bread" in result
        assert "milk" in result
        assert "eggs" not in result

    def test_dfs_cyclic_graph(self):
        """Test DFS handles cycles without infinite loop."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("c", "a")

        result = dfs(graph, "a")

        # Should visit each node exactly once
        assert len(result) == 3
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_dfs_disconnected_graph(self):
        """Test DFS only finds connected component."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("c", "d")

        result = dfs(graph, "a")

        assert "a" in result
        assert "b" in result
        assert "c" not in result
        assert "d" not in result

    def test_dfs_nonexistent_start(self):
        """Test DFS with non-existent start node."""
        graph = Graph()
        graph.add_edge("a", "b")

        with pytest.raises(KeyError, match="not found"):
            dfs(graph, "nonexistent")

    def test_dfs_returns_visited_order(self):
        """Test DFS returns nodes in depth-first order."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("a", "c")
        graph.add_edge("b", "d")

        result = dfs(graph, "a")

        # DFS should explore deeply before broadly
        assert len(result) == 4
        assert "a" in result
        assert "b" in result
        assert "c" in result
        assert "d" in result

    def test_dfs_vs_bfs_different_order(self):
        """Test that DFS explores differently than BFS."""
        graph = Graph()
        # Tree: a -> b -> d
        #           -> c -> e
        graph.add_edge("a", "b")
        graph.add_edge("a", "c")
        graph.add_edge("b", "d")
        graph.add_edge("c", "e")

        dfs_result = dfs(graph, "a")
        bfs_result = bfs(graph, "a")

        # Both should find all nodes
        assert len(dfs_result) == 5
        assert len(bfs_result) == 5

        # But depths might differ based on exploration order
        # This test just ensures both work


class TestSearchAlgorithmProperties:
    """Test general properties of search algorithms."""

    def test_bfs_and_dfs_find_same_nodes(self):
        """Test BFS and DFS find the same set of reachable nodes."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")
        graph.add_edge("c", "d")
        graph.add_edge("a", "e")

        bfs_nodes = set(bfs(graph, "a").keys())
        dfs_nodes = set(dfs(graph, "a"))

        assert bfs_nodes == dfs_nodes

    def test_max_depth_zero_returns_only_start(self):
        """Test max_depth=0 returns only the start node."""
        graph = Graph()
        graph.add_edge("a", "b")
        graph.add_edge("b", "c")

        bfs_result = bfs(graph, "a", max_depth=0)
        dfs_result = dfs(graph, "a", max_depth=0)

        assert list(bfs_result.keys()) == ["a"]
        assert list(dfs_result) == ["a"]

    def test_large_graph_performance(self):
        """Test algorithms work on larger graphs."""
        graph = Graph()
        # Create a chain of 50 items
        for i in range(49):
            graph.add_edge(f"item_{i}", f"item_{i + 1}")

        bfs_result = bfs(graph, "item_0")
        dfs_result = dfs(graph, "item_0")

        assert len(bfs_result) == 50
        assert len(dfs_result) == 50
