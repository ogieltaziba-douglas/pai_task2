"""
Demo script to load and analyze the FULL supermarket dataset.
This version loads ALL transactions for complete analysis.
"""

import sys
import time
from pathlib import Path

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
    """Load supermarket dataset (one item per line format)."""
    print(f" Loading data from: {filepath}")

    import csv
    from collections import defaultdict

    transactions_dict = defaultdict(list)

    start_time = time.time()

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            member = row["Member_number"]
            date = row["Date"]
            item = row["itemDescription"].strip().lower()

            if item:
                transaction_key = f"{member}_{date}"
                transactions_dict[transaction_key].append(item)

    transactions = list(transactions_dict.values())
    transactions = [[*dict.fromkeys(txn)] for txn in transactions]

    if max_transactions:
        transactions = transactions[:max_transactions]

    load_time = time.time() - start_time

    print(f" Loaded {len(transactions)} transactions in {load_time:.2f}s")

    return transactions


def main():
    print("=" * 70)
    print("  MARKET BASKET ANALYSIS - FULL Dataset")
    print("=" * 70)

    dataset_path = "data/raw/Supermarket_dataset_PAI.csv"

    # Load ALL transactions
    print("\n Loading ALL Transactions...")
    transactions = load_supermarket_data(dataset_path)

    print(f"\n   Total transactions: {len(transactions)}")
    print(f"   Sample: {transactions[0][:3]}...")

    # Build graph
    print("\n Building Complete Item Network...")
    start_time = time.time()
    graph = build_graph_from_transactions(transactions)
    build_time = time.time() - start_time
    print(f" Graph built in {build_time:.2f}s")

    # Statistics
    print(f"\n Complete Graph Statistics:")
    print(f"   Unique items: {graph.node_count()}")
    print(f"   Item pairs (edges): {graph.edge_count()}")

    # Top bundles
    print(f"\n Top 20 Product Bundles:")
    top_bundles = get_top_bundles(graph, n=20)
    for i, (item1, item2, freq) in enumerate(top_bundles, 1):
        print(f"   {i:2d}. {item1:30s} + {item2:30s}: {freq:4d}x")

    print("\n" + "=" * 70)
    print(" Full Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
