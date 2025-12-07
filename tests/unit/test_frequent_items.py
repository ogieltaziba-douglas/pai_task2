"""
Unit tests for frequent items analysis.
Following TDD - tests written BEFORE implementation.
"""

import pytest
from src.analysis.frequent_items import (
    find_items_bought_with,
    get_top_associations,
    get_frequent_pairs,
    get_top_bundles,
)
from src.data_structures.graph import Graph


class TestFindItemsBoughtWith:
    """Test finding items frequently bought with a specific item."""

    def test_find_direct_neighbors(self):
        """Test finding items directly bought with target item."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("bread", "butter", weight=5)
        graph.add_edge("bread", "eggs", weight=3)

        result = find_items_bought_with(graph, "bread")

        # Should return items sorted by weight descending
        assert len(result) == 3
        assert result[0] == ("milk", 10)
        assert result[1] == ("butter", 5)
        assert result[2] == ("eggs", 3)

    def test_find_with_min_frequency(self):
        """Test filtering by minimum co-occurrence frequency."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("bread", "butter", weight=5)
        graph.add_edge("bread", "eggs", weight=2)

        result = find_items_bought_with(graph, "bread", min_frequency=5)

        # Only items with weight >= 5
        assert len(result) == 2
        assert result[0] == ("milk", 10)
        assert result[1] == ("butter", 5)

    def test_find_with_limit(self):
        """Test limiting number of returned items."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("bread", "butter", weight=5)
        graph.add_edge("bread", "eggs", weight=3)

        result = find_items_bought_with(graph, "bread", limit=2)

        assert len(result) == 2
        assert result[0] == ("milk", 10)
        assert result[1] == ("butter", 5)

    def test_find_isolated_item(self):
        """Test finding items for an isolated node."""
        graph = Graph()
        graph.add_node("bread")
        graph.add_edge("milk", "eggs")

        result = find_items_bought_with(graph, "bread")

        assert result == []

    def test_find_nonexistent_item(self):
        """Test querying non-existent item."""
        graph = Graph()
        graph.add_edge("bread", "milk")

        with pytest.raises(KeyError, match="not found"):
            find_items_bought_with(graph, "nonexistent")

    def test_find_items_sorted_by_weight(self):
        """Test that results are sorted by weight (highest first)."""
        graph = Graph()
        graph.add_edge("bread", "a", weight=1)
        graph.add_edge("bread", "b", weight=100)
        graph.add_edge("bread", "c", weight=50)
        graph.add_edge("bread", "d", weight=75)

        result = find_items_bought_with(graph, "bread")

        weights = [weight for _, weight in result]
        assert weights == sorted(weights, reverse=True)


class TestGetTopAssociations:
    """Test getting top item associations."""

    def test_get_top_associations_basic(self):
        """Test getting top N associations for an item."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("bread", "butter", weight=5)

        result = get_top_associations(graph, "bread", n=1)

        assert len(result) == 1
        assert result[0] == ("milk", 10)

    def test_get_top_associations_more_than_available(self):
        """Test requesting more items than available."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)

        result = get_top_associations(graph, "bread", n=10)

        assert len(result) == 1

    def test_get_top_associations_with_depth(self):
        """Test finding associations within certain depth."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("milk", "cheese", weight=8)
        graph.add_edge("bread", "butter", weight=5)

        # Depth 1: only direct neighbors
        result_depth1 = get_top_associations(graph, "bread", n=10, max_depth=1)

        # Should only include milk and butter (direct)
        items = [item for item, _ in result_depth1]
        assert "milk" in items
        assert "butter" in items
        assert "cheese" not in items


class TestGetFrequentPairs:
    """Test finding frequent item pairs."""

    def test_get_all_pairs(self):
        """Test getting all item pairs with their frequencies."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("bread", "butter", weight=5)
        graph.add_edge("milk", "eggs", weight=3)

        result = get_frequent_pairs(graph)

        assert len(result) == 3
        # Results should be sorted by weight descending
        assert result[0][2] == 10  # ("bread", "milk", 10)

    def test_get_pairs_with_min_frequency(self):
        """Test filtering pairs by minimum frequency."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("bread", "butter", weight=5)
        graph.add_edge("milk", "eggs", weight=2)

        result = get_frequent_pairs(graph, min_frequency=5)

        # Only pairs with weight >= 5
        assert len(result) == 2

    def test_get_pairs_sorted_by_frequency(self):
        """Test that pairs are sorted by frequency."""
        graph = Graph()
        graph.add_edge("a", "b", weight=1)
        graph.add_edge("c", "d", weight=100)
        graph.add_edge("e", "f", weight=50)

        result = get_frequent_pairs(graph)

        # Should be in descending order of weight
        assert result[0][2] == 100
        assert result[1][2] == 50
        assert result[2][2] == 1

    def test_get_pairs_empty_graph(self):
        """Test getting pairs from empty graph."""
        graph = Graph()

        result = get_frequent_pairs(graph)

        assert result == []

    def test_get_pairs_no_edges(self):
        """Test getting pairs from graph with nodes but no edges."""
        graph = Graph()
        graph.add_node("bread")
        graph.add_node("milk")

        result = get_frequent_pairs(graph)

        assert result == []


class TestGetTopBundles:
    """Test getting top product bundles."""

    def test_get_top_bundles_basic(self):
        """Test getting top N most common product bundles."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)
        graph.add_edge("milk", "eggs", weight=5)
        graph.add_edge("bread", "butter", weight=3)

        result = get_top_bundles(graph, n=2)

        assert len(result) == 2
        # Top bundle should be (bread, milk) with weight 10
        top_bundle = result[0]
        assert top_bundle[2] == 10

    def test_get_top_bundles_limit_exceeds(self):
        """Test requesting more bundles than exist."""
        graph = Graph()
        graph.add_edge("a", "b", weight=5)

        result = get_top_bundles(graph, n=10)

        assert len(result) == 1

    def test_bundles_are_pairs(self):
        """Test that bundles are returned as (item1, item2, weight) tuples."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=10)

        result = get_top_bundles(graph, n=1)

        assert len(result[0]) == 3
        item1, item2, weight = result[0]
        assert isinstance(item1, str)
        assert isinstance(item2, str)
        assert isinstance(weight, int)


class TestAssociationQueryIntegration:
    """Integration tests for association queries."""

    def test_end_to_end_query(self):
        """Test complete workflow: build graph and query associations."""
        graph = Graph()
        # Simulate transaction data
        graph.add_edge("bread", "milk", weight=100)
        graph.add_edge("bread", "butter", weight=75)
        graph.add_edge("bread", "eggs", weight=50)
        graph.add_edge("milk", "eggs", weight=60)
        graph.add_edge("butter", "eggs", weight=40)

        # Query: What's bought with bread?
        bread_items = find_items_bought_with(graph, "bread", limit=3)

        assert len(bread_items) == 3
        assert bread_items[0][0] == "milk"  # Highest weight

        # Query: Top 2 bundles
        top_bundles = get_top_bundles(graph, n=2)

        assert len(top_bundles) == 2
        # (bread, milk) should be top bundle
        assert top_bundles[0][2] == 100

    def test_real_scenario_milk_associations(self):
        """Test realistic scenario: what do customers buy with milk?"""
        graph = Graph()
        graph.add_edge("milk", "bread", weight=80)
        graph.add_edge("milk", "eggs", weight=60)
        graph.add_edge("milk", "cereal", weight=50)
        graph.add_edge("milk", "butter", weight=30)

        # Top 3 items bought with milk
        result = get_top_associations(graph, "milk", n=3)

        assert len(result) == 3
        assert result[0] == ("bread", 80)
        assert result[1] == ("eggs", 60)
        assert result[2] == ("cereal", 50)

    def test_filter_low_frequency_associations(self):
        """Test filtering out low-frequency associations."""
        graph = Graph()
        graph.add_edge("bread", "milk", weight=100)
        graph.add_edge("bread", "rare_item", weight=2)

        # Only show items bought together at least 10 times
        result = find_items_bought_with(graph, "bread", min_frequency=10)

        assert len(result) == 1
        assert result[0][0] == "milk"
