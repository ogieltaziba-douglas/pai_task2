"""
Graph builder algorithm for market basket analysis.
Processes transaction data into graph structure.
"""

from typing import List
from src.data_structures.graph import Graph


def build_graph_from_transactions(transactions: List[List[str]]) -> Graph:
    """
    Build a graph from transaction data.

    Creates nodes for items and edges for co-purchased items.
    Edge weights represent co-occurrence frequency.

    Args:
        transactions: List of transactions, each is a list of item names

    Returns:
        Graph with items as nodes and co-purchase relationships as edges

    Time Complexity: O(n * m^2) where n = number of transactions,
                     m = average items per transaction
    Space Complexity: O(V + E) where V = unique items, E = unique pairs
    """
    graph = Graph()

    # Process each transaction
    for transaction in transactions:
        # Filter out empty or whitespace-only items, and normalize case
        items = []
        for item in transaction:
            if item and item.strip():
                items.append(item.strip().lower())  # Normalize to lowercase

        # Remove duplicates within transaction
        unique_items = []
        seen = set()
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)

        # Add all nodes (items)
        for item in unique_items:
            graph.add_node(item)

        # Create edges for all pairs of items in the transaction
        # This is the co-purchase relationship
        for i in range(len(unique_items)):
            for j in range(i + 1, len(unique_items)):
                item1 = unique_items[i]
                item2 = unique_items[j]

                # Add edge with weight 1 (will accumulate if already exists)
                graph.add_edge(item1, item2, weight=1)

    return graph
