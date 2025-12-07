"""
Demo script to load and analyze the real supermarket dataset.
Demonstrates the complete market basket analysis workflow.

IMPORTANT: This script ONLY READS the original dataset. It never modifies it.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.data_loader import load_transactions
from algorithms.graph_builder import build_graph_from_transactions
from analysis.frequent_items import (
    find_items_bought_with,
    get_top_bundles,
    get_frequent_pairs,
)
from algorithms.search import bfs, dfs


def load_supermarket_data(filepath: str, max_transactions: int = None):
    """
    Load the supermarket dataset.

    Note: The dataset has one item per line, so we need special handling.
    Format: Member_number,Date,itemDescription

    Args:
        filepath: Path to the CSV file
        max_transactions: Limit number of transactions (for testing)

    Returns:
        List of transactions
    """
    print(f" Loading data from: {filepath}")
    print("   (This only READS the file, never modifies it)")

    import csv
    from collections import defaultdict

    # Group items by (member_number, date) to form transactions
    transactions_dict = defaultdict(list)

    start_time = time.time()

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            member = row["Member_number"]
            date = row["Date"]
            item = row["itemDescription"].strip().lower()

            if item:  # Only add non-empty items
                transaction_key = f"{member}_{date}"
                transactions_dict[transaction_key].append(item)

    # Convert to list of transactions
    transactions = list(transactions_dict.values())

    # Remove duplicates within each transaction
    transactions = [[*dict.fromkeys(txn)] for txn in transactions]

    # Apply limit if specified
    if max_transactions:
        transactions = transactions[:max_transactions]

    load_time = time.time() - start_time

    print(f" Loaded {len(transactions)} transactions in {load_time:.2f}s")
    print(f"   Original file has {len(transactions_dict)} unique shopping sessions")

    return transactions


def analyze_graph(graph):
    """Display basic graph statistics."""
    print(f"\n Graph Statistics:")
    print(f"   Nodes (unique items): {graph.node_count()}")
    print(f"   Edges (item pairs): {graph.edge_count()}")
    print(
        f"   Average items per transaction: ~{graph.edge_count() * 2 / max(graph.node_count(), 1):.1f}"
    )


def demo_queries(graph):
    """Demonstrate various query capabilities."""
    print(f"\n Running Demo Queries...")

    # Get all items first
    all_items = graph.get_all_nodes()
    if not all_items:
        print("  No items in graph!")
        return

    print(f"\n1️  Top 10 Product Bundles:")
    top_bundles = get_top_bundles(graph, n=10)
    for i, (item1, item2, freq) in enumerate(top_bundles[:10], 1):
        print(f"   {i}. {item1} + {item2}: {freq} times")

    # Pick a common item for association query
    if top_bundles:
        common_item = top_bundles[0][0]  # Most common item

        print(f"\n2️  Items frequently bought with '{common_item}':")
        associations = find_items_bought_with(graph, common_item, limit=5)
        for item, freq in associations:
            print(f"   - {item}: {freq} times")

        print(f"\n3️  BFS: Items within 2 degrees of '{common_item}':")
        nearby = bfs(graph, common_item, max_depth=2)
        print(f"   Found {len(nearby)} connected items")
        print(f"   Depth 0: {sum(1 for d in nearby.values() if d == 0)} items")
        print(f"   Depth 1: {sum(1 for d in nearby.values() if d == 1)} items")
        print(f"   Depth 2: {sum(1 for d in nearby.values() if d == 2)} items")


def main():
    """Main demo workflow."""
    print("=" * 60)
    print("  MARKET BASKET ANALYSIS - Real Dataset Demo")
    print("=" * 60)

    # Dataset path
    dataset_path = "data/raw/Supermarket_dataset_PAI.csv"

    # Step 1: Load data (read-only!)
    print("\n Step 1: Load Transaction Data")
    transactions = load_supermarket_data(dataset_path, max_transactions=1000)

    if not transactions:
        print(" No transactions loaded!")
        return

    print(
        f"\n   Sample transaction: {transactions[0][:5]} {'...' if len(transactions[0]) > 5 else ''}"
    )

    # Step 2: Build graph
    print("\n Step 2: Build Item Network Graph")
    start_time = time.time()
    graph = build_graph_from_transactions(transactions)
    build_time = time.time() - start_time
    print(f" Graph built in {build_time:.2f}s")

    # Step 3: Analyze
    print("\n Step 3: Analyze Market Basket Data")
    analyze_graph(graph)
    demo_queries(graph)

    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
