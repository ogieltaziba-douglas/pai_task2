"""
Frequent items analysis for market basket queries.
Functions to find item associations and frequent itemsets.
"""

from typing import List, Tuple
from data_structures.graph import Graph
from algorithms.search import bfs
from algorithms.sorting import merge_sort


def find_items_bought_with(
    graph: Graph, item: str, min_frequency: int = 1, limit: int = None
) -> List[Tuple[str, int]]:
    """
    Find items frequently bought together with the specified item.

    Args:
        graph: Graph containing item relationships
        item: Target item to find associations for
        min_frequency: Minimum co-occurrence frequency
        limit: Maximum number of items to return

    Returns:
        List of (item_name, frequency) tuples, sorted by frequency descending

    Raises:
        KeyError: If item not found in graph
    """
    # Check if item exists
    if not graph.has_node(item):
        raise KeyError(f"Item '{item}' not found in graph")

    # Get all neighbors with their weights
    neighbors = graph.get_neighbors(item)

    # Filter by minimum frequency
    filtered = [
        (neighbor, weight)
        for neighbor, weight in neighbors.items()
        if weight >= min_frequency
    ]

    # Sort by weight (frequency) in descending order using custom merge sort
    sorted_items = merge_sort(filtered, key=lambda x: x[1], reverse=True)

    # Apply limit if specified
    if limit is not None:
        sorted_items = sorted_items[:limit]

    return sorted_items


def get_top_associations(
    graph: Graph, item: str, n: int = 5, max_depth: int = 1
) -> List[Tuple[str, int]]:
    """
    Get top N items associated with the target item.

    Args:
        graph: Graph containing item relationships
        item: Target item
        n: Number of top associations to return
        max_depth: Search depth (1 = direct neighbors only)

    Returns:
        List of (item_name, weight) tuples for top N associations

    Raises:
        KeyError: If item not found in graph
    """
    # Use BFS to find items within max_depth
    reachable = bfs(graph, item, max_depth=max_depth)

    # Collect associations with weights
    associations = []
    for node in reachable:
        if node != item:  # Exclude the item itself
            # Get weight from graph
            weight = graph.get_edge_weight(item, node)
            if weight > 0:  # Direct neighbor
                associations.append((node, weight))
            # For indirect connections (depth > 1), we'd need path finding
            # For now, only include direct neighbors with edges

    # Sort by weight descending using custom merge sort
    associations = merge_sort(associations, key=lambda x: x[1], reverse=True)

    # Return top N
    return associations[:n]


def get_frequent_pairs(
    graph: Graph, min_frequency: int = 1
) -> List[Tuple[str, str, int]]:
    """
    Get all frequent item pairs from the graph.

    Args:
        graph: Graph containing item relationships
        min_frequency: Minimum co-occurrence frequency

    Returns:
        List of (item1, item2, frequency) tuples sorted by frequency descending
    """
    # Get all edges from the graph
    edges = graph.get_all_edges()

    # Filter by minimum frequency
    filtered = [
        (item1, item2, weight)
        for item1, item2, weight in edges
        if weight >= min_frequency
    ]

    # Sort by frequency (weight) in descending order using custom merge sort
    sorted_pairs = merge_sort(filtered, key=lambda x: x[2], reverse=True)

    return sorted_pairs


def get_top_bundles(graph: Graph, n: int = 10) -> List[Tuple[str, str, int]]:
    """
    Get top N most common product bundles (item pairs).

    Args:
        graph: Graph containing item relationships
        n: Number of top bundles to return

    Returns:
        List of (item1, item2, frequency) tuples for top N bundles
    """
    # Get all pairs sorted by frequency
    all_pairs = get_frequent_pairs(graph, min_frequency=1)

    # Return top N
    return all_pairs[:n]
