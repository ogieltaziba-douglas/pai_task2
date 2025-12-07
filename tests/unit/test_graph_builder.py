"""
Unit tests for graph_builder module.
Following TDD - tests written BEFORE implementation.
"""

import pytest
from src.algorithms.graph_builder import build_graph_from_transactions
from src.data_structures.graph import Graph


class TestBuildGraphFromTransactions:
    """Test building graph from transaction data."""

    def test_build_from_empty_transactions(self):
        """Test building graph from empty transaction list."""
        transactions = []
        graph = build_graph_from_transactions(transactions)

        assert graph.node_count() == 0
        assert graph.edge_count() == 0
        assert graph.is_empty()

    def test_build_from_single_transaction(self):
        """Test building graph from one transaction."""
        transactions = [["bread", "milk", "eggs"]]
        graph = build_graph_from_transactions(transactions)

        # 3 items
        assert graph.node_count() == 3

        # 3 pairs: (bread,milk), (bread,eggs), (milk,eggs)
        assert graph.edge_count() == 3

        # All items should be connected
        assert graph.has_edge("bread", "milk")
        assert graph.has_edge("bread", "eggs")
        assert graph.has_edge("milk", "eggs")

    def test_build_edge_weights_default(self):
        """Test that initial edge weights are 1."""
        transactions = [["bread", "milk"]]
        graph = build_graph_from_transactions(transactions)

        assert graph.get_edge_weight("bread", "milk") == 1

    def test_build_weight_accumulation(self):
        """Test that repeated co-purchases increase weight."""
        transactions = [["bread", "milk"], ["bread", "milk"], ["bread", "milk"]]
        graph = build_graph_from_transactions(transactions)

        # Weight should accumulate
        assert graph.get_edge_weight("bread", "milk") == 3

    def test_build_multiple_transactions(self):
        """Test building graph from multiple transactions."""
        transactions = [["bread", "milk"], ["bread", "butter"], ["milk", "cheese"]]
        graph = build_graph_from_transactions(transactions)

        # Should have 4 unique items
        assert graph.node_count() == 4

        # Should have 3 edges
        assert graph.edge_count() == 3

        # Check specific edges
        assert graph.has_edge("bread", "milk")
        assert graph.has_edge("bread", "butter")
        assert graph.has_edge("milk", "cheese")

    def test_build_partial_overlap(self):
        """Test transactions with partial item overlap."""
        transactions = [["bread", "milk", "eggs"], ["bread", "butter", "cheese"]]
        graph = build_graph_from_transactions(transactions)

        # 5 unique items: bread, milk, eggs, butter, cheese
        assert graph.node_count() == 5

        # bread appears in both, so it connects to 4 items
        assert graph.degree("bread") == 4

        # milk and eggs only in first transaction
        assert graph.degree("milk") == 2  # bread, eggs
        assert graph.degree("eggs") == 2  # bread, milk

    def test_build_single_item_transaction(self):
        """Test that single-item transactions add nodes but no edges."""
        transactions = [["bread"], ["milk"]]
        graph = build_graph_from_transactions(transactions)

        # Two isolated nodes
        assert graph.node_count() == 2
        assert graph.edge_count() == 0

        # Nodes exist but not connected
        assert graph.has_node("bread")
        assert graph.has_node("milk")
        assert not graph.has_edge("bread", "milk")

    def test_build_mixed_transaction_sizes(self):
        """Test mix of different transaction sizes."""
        transactions = [["bread"], ["milk", "eggs"], ["butter", "cheese", "yogurt"]]
        graph = build_graph_from_transactions(transactions)

        # bread is isolated
        assert graph.degree("bread") == 0

        # milk-eggs pair
        assert graph.degree("milk") == 1
        assert graph.degree("eggs") == 1

        # butter-cheese-yogurt triangle
        assert graph.degree("butter") == 2
        assert graph.degree("cheese") == 2
        assert graph.degree("yogurt") == 2

    def test_build_all_items_together(self):
        """Test when all transactions contain the same items."""
        transactions = [["bread", "milk"], ["bread", "milk"], ["bread", "milk"]]
        graph = build_graph_from_transactions(transactions)

        assert graph.node_count() == 2
        assert graph.edge_count() == 1
        assert graph.get_edge_weight("bread", "milk") == 3

    def test_build_using_sample_fixture(self, sample_transactions):
        """Test using the sample_transactions fixture from conftest."""
        graph = build_graph_from_transactions(sample_transactions)

        # sample_transactions has: bread, milk, eggs, butter, cheese
        assert graph.node_count() == 5
        assert graph.edge_count() > 0

        # bread appears multiple times
        assert graph.degree("bread") > 1

    def test_build_preserves_graph_properties(self):
        """Test that built graph maintains valid graph properties."""
        transactions = [["a", "b", "c"], ["b", "c", "d"]]
        graph = build_graph_from_transactions(transactions)

        # Graph should be undirected (symmetric edges)
        for node in graph.get_all_nodes():
            for neighbor, weight in graph.get_neighbors(node).items():
                assert graph.get_edge_weight(neighbor, node) == weight

    def test_build_large_transaction(self):
        """Test building graph from a large transaction."""
        # Transaction with 10 items creates 45 edges (n choose 2)
        items = [f"item_{i}" for i in range(10)]
        transactions = [items]
        graph = build_graph_from_transactions(transactions)

        assert graph.node_count() == 10
        # 10 choose 2 = 45
        assert graph.edge_count() == 45

    def test_build_many_transactions(self):
        """Test building graph from many transactions."""
        transactions = [["bread", "milk"] for _ in range(100)]
        graph = build_graph_from_transactions(transactions)

        assert graph.node_count() == 2
        assert graph.edge_count() == 1
        assert graph.get_edge_weight("bread", "milk") == 100


class TestGraphBuilderEdgeCases:
    """Test edge cases and error handling."""

    def test_build_with_duplicate_items_in_transaction(self):
        """Test handling duplicate items within a transaction."""
        # This should be handled by data_loader, but test anyway
        transactions = [["bread", "milk", "bread"]]
        graph = build_graph_from_transactions(transactions)

        # Should not create self-loop or count duplicate
        assert graph.node_count() == 2
        assert graph.edge_count() == 1

    def test_build_empty_items_filtered(self):
        """Test that empty strings are filtered out."""
        transactions = [["bread", "", "milk"]]
        graph = build_graph_from_transactions(transactions)

        assert graph.node_count() == 2
        assert not graph.has_node("")

    def test_build_whitespace_items_filtered(self):
        """Test that whitespace-only items are filtered."""
        transactions = [["bread", "   ", "milk"]]
        graph = build_graph_from_transactions(transactions)

        assert graph.node_count() == 2

    def test_build_case_consistency(self):
        """Test that item names are case-consistent."""
        transactions = [["Bread", "Milk"], ["bread", "milk"]]
        graph = build_graph_from_transactions(transactions)

        # Should treat as same items (lowercase normalized)
        # This assumes data_loader normalizes to lowercase
        assert graph.node_count() == 2


class TestGraphBuilderComplexity:
    """Test algorithm complexity characteristics."""

    def test_incremental_build(self):
        """Test that we can build graph incrementally."""
        # Build initial graph
        transactions1 = [["bread", "milk"]]
        graph = build_graph_from_transactions(transactions1)

        initial_weight = graph.get_edge_weight("bread", "milk")
        assert initial_weight == 1

        # Note: This test assumes we might want incremental updates later
        # For now, we rebuild from scratch

    def test_order_independence(self):
        """Test that transaction order doesn't affect final graph."""
        transactions_v1 = [["bread", "milk"], ["eggs", "cheese"]]
        transactions_v2 = [["eggs", "cheese"], ["bread", "milk"]]

        graph1 = build_graph_from_transactions(transactions_v1)
        graph2 = build_graph_from_transactions(transactions_v2)

        # Graphs should be equivalent
        assert graph1.node_count() == graph2.node_count()
        assert graph1.edge_count() == graph2.edge_count()
        assert graph1.get_edge_weight("bread", "milk") == graph2.get_edge_weight(
            "bread", "milk"
        )


class TestGraphBuilderIntegration:
    """Integration tests combining multiple components."""

    def test_build_then_query(self):
        """Test building graph and then querying it."""
        transactions = [
            ["bread", "milk", "eggs"],
            ["bread", "milk", "butter"],
            ["milk", "eggs", "cheese"],
        ]
        graph = build_graph_from_transactions(transactions)

        # milk appears in all 3 transactions
        milk_neighbors = graph.get_neighbors("milk")

        # milk should connect to: bread (2x), eggs (2x), butter (1x), cheese (1x)
        assert len(milk_neighbors) == 4
        assert milk_neighbors["bread"] == 2
        assert milk_neighbors["eggs"] == 2
        assert milk_neighbors["butter"] == 1
        assert milk_neighbors["cheese"] == 1

    def test_build_and_verify_all_pairs(self):
        """Test that all item pairs in a transaction are connected."""
        transactions = [["a", "b", "c", "d"]]
        graph = build_graph_from_transactions(transactions)

        items = ["a", "b", "c", "d"]

        # Every pair should be connected
        for i, item1 in enumerate(items):
            for item2 in items[i + 1 :]:
                assert graph.has_edge(item1, item2)
