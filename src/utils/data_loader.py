"""
Data loading utilities for market basket transactions.
Loads and parses CSV transaction data.
"""

from typing import List
import os


def parse_transaction_line(line: str) -> List[str]:
    """
    Parse a single transaction line from CSV.

    Args:
        line: Comma-separated line of items

    Returns:
        List of item names (trimmed, lowercase, duplicates removed)
    """
    # Handle empty or whitespace-only lines
    if not line or not line.strip():
        return []

    # Split by comma
    items = line.split(",")

    # Process items: strip whitespace, lowercase, filter empty
    processed_items = []
    for item in items:
        item = item.strip()  # Remove whitespace
        if item:  # Filter empty strings
            item = item.lower()  # Normalize to lowercase
            processed_items.append(item)

    # Remove duplicates while preserving order
    seen = set()
    unique_items = []
    for item in processed_items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items


def load_transactions(
    filepath: str, has_header: bool = False, max_transactions: int = None
) -> List[List[str]]:
    """
    Load transactions from CSV file.

    Args:
        filepath: Path to CSV file
        has_header: Whether first line is a header to skip
        max_transactions: Maximum number of transactions to load (None = all)

    Returns:
        List of transactions, where each transaction is a list of items

    Raises:
        FileNotFoundError: If file does not exist
    """
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    transactions = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # Skip header if specified
            if has_header:
                next(f, None)

            # Read transactions
            for line in f:
                # Parse the line
                items = parse_transaction_line(line)

                # Only add non-empty transactions
                if items:
                    transactions.append(items)

                # Check if we've reached max_transactions
                if (
                    max_transactions is not None
                    and len(transactions) >= max_transactions
                ):
                    break

    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(filepath, "r", encoding="latin-1") as f:
            if has_header:
                next(f, None)

            for line in f:
                items = parse_transaction_line(line)
                if items:
                    transactions.append(items)

                if (
                    max_transactions is not None
                    and len(transactions) >= max_transactions
                ):
                    break

    return transactions
