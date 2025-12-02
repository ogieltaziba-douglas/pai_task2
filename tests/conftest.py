"""
Pytest Configuration and Shared Fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture
def sample_transactions():
    """
    Sample transaction data for testing.
    Returns a list of transactions where each transaction is a list of items.
    """
    return [
        ["bread", "milk", "eggs"],
        ["bread", "butter"],
        ["milk", "butter", "cheese"],
        ["bread", "milk", "butter"],
        ["eggs", "cheese"],
    ]


@pytest.fixture
def empty_transactions():
    """Empty transaction list for edge case testing."""
    return []


@pytest.fixture
def single_item_transactions():
    """Transactions with single items only."""
    return [["bread"], ["milk"], ["eggs"]]


@pytest.fixture
def large_transaction():
    """A single large transaction with many items."""
    return [["item_" + str(i) for i in range(100)]]
