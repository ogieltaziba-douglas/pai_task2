"""
Unit tests for Graph data structure.
Following TDD - tests written BEFORE implementation.
"""
import pytest
from src.data_structures.graph import Graph


class TestGraphInitialization:
    """Test graph initialization and basic properties."""

    def test_empty_graph_creation(self):
        """Test creating an empty graph."""
        graph = Graph()
        assert graph is not None
        assert graph.node_count() == 0
        assert graph.edge_count() == 0

    def test_empty_graph_has_no_nodes(self):
        """Test that a new graph has no nodes."""
        graph = Graph()
        assert graph.get_all_nodes() == []

    def test_empty_graph_has_no_edges(self):
        """Test that a new graph has no edges."""
        graph = Graph()
        assert graph.get_all_edges() == []


class TestAddEdge:
    """Test adding edges to the graph."""

    def test_add_single_edge(self):
        """Test adding a single edge between two items."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        
        assert graph.node_count() == 2
        assert graph.edge_count() == 1
        assert graph.has_edge("bread", "milk")
        assert graph.has_edge("milk", "bread")  # Undirected

    def test_add_edge_with_weight(self):
        """Test adding an edge with a specific weight."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=5)
        
        assert graph.get_edge_weight("bread", "milk") == 5
        assert graph.get_edge_weight("milk", "bread") == 5  # Symmetric

    def test_add_edge_default_weight(self):
        """Test that default weight is 1."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        
        assert graph.get_edge_weight("bread", "milk") == 1

    def test_add_duplicate_edge_increases_weight(self):
        """Test that adding same edge multiple times increases weight."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "milk", weight=3)
        
        # Total weight should be 1 + 1 + 3 = 5
        assert graph.get_edge_weight("bread", "milk") == 5

    def test_add_multiple_different_edges(self):
        """Test adding multiple different edges."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")
        graph.add_edge("milk", "cheese")
        
        assert graph.node_count() == 4
        assert graph.edge_count() == 3

    def test_add_edge_with_same_item(self):
        """Test that self-loops are not allowed."""
        graph = Graph()
        with pytest.raises(ValueError, match="Self-loops are not allowed"):
            graph.add_edge("bread", "bread")

    def test_add_edge_with_empty_string(self):
        """Test that empty item names are not allowed."""
        graph = Graph()
        with pytest.raises(ValueError, match="Item names cannot be empty"):
            graph.add_edge("", "milk")
        with pytest.raises(ValueError, match="Item names cannot be empty"):
            graph.add_edge("bread", "")

    def test_add_edge_with_negative_weight(self):
        """Test that negative weights are not allowed."""
        graph = Graph()
        with pytest.raises(ValueError, match="Weight must be positive"):
            graph.add_edge("bread", "milk", weight=-1)

    def test_add_edge_with_zero_weight(self):
        """Test that zero weight is not allowed."""
        graph = Graph()
        with pytest.raises(ValueError, match="Weight must be positive"):
            graph.add_edge("bread", "milk", weight=0)


class TestGetNeighbors:
    """Test retrieving neighbors of a node."""

    def test_get_neighbors_single_edge(self):
        """Test getting neighbors for a node with one edge."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        
        neighbors = graph.get_neighbors("bread")
        assert "milk" in neighbors
        assert neighbors["milk"] == 1

    def test_get_neighbors_multiple_edges(self):
        """Test getting neighbors for a node with multiple edges."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=5)
        graph.add_edge("bread", "butter", weight=3)
        graph.add_edge("bread", "cheese", weight=2)
        
        neighbors = graph.get_neighbors("bread")
        assert len(neighbors) == 3
        assert neighbors["milk"] == 5
        assert neighbors["butter"] == 3
        assert neighbors["cheese"] == 2

    def test_get_neighbors_isolated_node(self):
        """Test getting neighbors for a node with no edges."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_node("eggs")  # Isolated node
        
        neighbors = graph.get_neighbors("eggs")
        assert neighbors == {}

    def test_get_neighbors_nonexistent_node(self):
        """Test getting neighbors for a non-existent node."""
        graph = Graph()
        with pytest.raises(KeyError, match="not found in graph"):
            graph.get_neighbors("nonexistent")


class TestNodeOperations:
    """Test node-related operations."""

    def test_add_node_explicitly(self):
        """Test adding a node without edges."""
        graph = Graph()
        graph.add_node("bread")
        
        assert graph.node_count() == 1
        assert "bread" in graph.get_all_nodes()

    def test_add_duplicate_node(self):
        """Test that adding duplicate node doesn't create duplicates."""
        graph = Graph()
        graph.add_node("bread")
        graph.add_node("bread")
        
        assert graph.node_count() == 1

    def test_has_node(self):
        """Test checking if a node exists."""
        graph = Graph()
        graph.add_node("bread")
        
        assert graph.has_node("bread") is True
        assert graph.has_node("milk") is False

    def test_get_all_nodes(self):
        """Test retrieving all nodes."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("butter", "cheese")
        
        nodes = graph.get_all_nodes()
        assert len(nodes) == 4
        assert set(nodes) == {"bread", "milk", "butter", "cheese"}

    def test_remove_node(self):
        """Test removing a node and its edges."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")
        
        graph.remove_node("bread")
        
        assert graph.has_node("bread") is False
        assert graph.node_count() == 2  # milk and butter remain
        assert graph.edge_count() == 0  # Both edges removed


class TestEdgeOperations:
    """Test edge-related operations."""

    def test_has_edge(self):
        """Test checking if an edge exists."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        
        assert graph.has_edge("bread", "milk") is True
        assert graph.has_edge("milk", "bread") is True
        assert graph.has_edge("bread", "butter") is False

    def test_get_edge_weight_existing(self):
        """Test getting weight of existing edge."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=7)
        
        assert graph.get_edge_weight("bread", "milk") == 7

    def test_get_edge_weight_nonexistent(self):
        """Test getting weight of non-existent edge."""
        graph = Graph()
        assert graph.get_edge_weight("bread", "milk") == 0

    def test_get_all_edges(self):
        """Test retrieving all edges."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=5)
        graph.add_edge("bread", "butter", weight=3)
        
        edges = graph.get_all_edges()
        assert len(edges) == 2
        
        # Edges should be tuples of (item1, item2, weight)
        edge_set = {(e[0], e[1]) for e in edges}
        assert ("bread", "milk") in edge_set or ("milk", "bread") in edge_set
        assert ("bread", "butter") in edge_set or ("butter", "bread") in edge_set

    def test_remove_edge(self):
        """Test removing an edge."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")
        
        graph.remove_edge("bread", "milk")
        
        assert graph.has_edge("bread", "milk") is False
        assert graph.has_edge("bread", "butter") is True
        assert graph.edge_count() == 1


class TestGraphProperties:
    """Test graph property methods."""

    def test_node_count(self):
        """Test counting nodes."""
        graph = Graph()
        assert graph.node_count() == 0
        
        graph.add_node("bread")
        assert graph.node_count() == 1
        
        graph.add_edge("milk", "butter")
        assert graph.node_count() == 3

    def test_edge_count(self):
        """Test counting edges."""
        graph = Graph()
        assert graph.edge_count() == 0
        
        graph.add_edge("bread", "milk")
        assert graph.edge_count() == 1
        
        graph.add_edge("bread", "butter")
        assert graph.edge_count() == 2

    def test_degree(self):
        """Test getting degree of a node."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        graph.add_edge("bread", "butter")
        graph.add_edge("bread", "cheese")
        
        assert graph.degree("bread") == 3
        assert graph.degree("milk") == 1

    def test_is_empty(self):
        """Test checking if graph is empty."""
        graph = Graph()
        assert graph.is_empty() is True
        
        graph.add_node("bread")
        assert graph.is_empty() is False


class TestGraphRepresentation:
    """Test graph string representation."""

    def test_str_representation(self):
        """Test string representation of graph."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=5)
        
        graph_str = str(graph)
        assert "bread" in graph_str
        assert "milk" in graph_str

    def test_repr_representation(self):
        """Test repr representation of graph."""
        graph = Graph()
        graph.add_edge("bread", "milk")
        
        graph_repr = repr(graph)
        assert "Graph" in graph_repr
        assert "2 nodes" in graph_repr or "1 edge" in graph_repr


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_large_weight_value(self):
        """Test handling very large weight values."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=1000000)
        
        assert graph.get_edge_weight("bread", "milk") == 1000000

    def test_many_neighbors(self):
        """Test node with many neighbors."""
        graph = Graph()
        for i in range(100):
            graph.add_edge("bread", f"item_{i}")
        
        neighbors = graph.get_neighbors("bread")
        assert len(neighbors) == 100

    def test_whitespace_in_item_names(self):
        """Test that item names with whitespace are handled."""
        graph = Graph()
        graph.add_edge("whole wheat bread", "skim milk")
        
        assert graph.has_edge("whole wheat bread", "skim milk")

    def test_case_sensitivity(self):
        """Test that item names are case-sensitive."""
        graph = Graph()
        graph.add_edge("Bread", "bread")
        
        # Should be two different nodes
        assert graph.node_count() == 2
        assert graph.has_node("Bread")
        assert graph.has_node("bread")
