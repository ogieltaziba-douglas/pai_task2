"""
Data loading utilities for market basket transactions.
Loads and parses CSV transaction data.
"""

from typing import List


def parse_transaction_line(line: str) -> List[str]:
    """
    Parse a single transaction line from CSV.

    Args:
        line: Comma-separated line of items

    Returns:
        List of item names (trimmed, lowercase, duplicates removed)
    """
    pass


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
    pass
