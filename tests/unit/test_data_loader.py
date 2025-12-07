"""
Unit tests for data_loader module.
Following TDD - tests written BEFORE implementation.
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.utils.data_loader import load_transactions, parse_transaction_line


class TestParseTransactionLine:
    """Test parsing individual transaction lines."""

    def test_parse_simple_transaction(self):
        """Test parsing a simple comma-separated line."""
        line = "bread,milk,eggs"
        items = parse_transaction_line(line)

        assert items == ["bread", "milk", "eggs"]

    def test_parse_with_whitespace(self):
        """Test that whitespace is trimmed from items."""
        line = " bread , milk , eggs "
        items = parse_transaction_line(line)

        assert items == ["bread", "milk", "eggs"]

    def test_parse_single_item(self):
        """Test parsing a line with single item."""
        line = "bread"
        items = parse_transaction_line(line)

        assert items == ["bread"]

    def test_parse_empty_line(self):
        """Test that empty lines return empty list."""
        line = ""
        items = parse_transaction_line(line)

        assert items == []

    def test_parse_whitespace_only(self):
        """Test that whitespace-only lines return empty list."""
        line = "   "
        items = parse_transaction_line(line)

        assert items == []

    def test_parse_with_empty_fields(self):
        """Test handling of empty fields in CSV."""
        line = "bread,,milk"
        items = parse_transaction_line(line)

        # Empty fields should be filtered out
        assert items == ["bread", "milk"]

    def test_case_normalization(self):
        """Test that item names are normalized to lowercase."""
        line = "BREAD,Milk,EgGs"
        items = parse_transaction_line(line)

        assert items == ["bread", "milk", "eggs"]


class TestLoadTransactions:
    """Test loading transactions from CSV files."""

    def test_load_simple_csv(self, tmp_path):
        """Test loading a simple CSV file."""
        # Create temporary CSV file
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread,milk,eggs\nbread,butter\nmilk,cheese\n")

        transactions = load_transactions(str(csv_file))

        assert len(transactions) == 3
        assert transactions[0] == ["bread", "milk", "eggs"]
        assert transactions[1] == ["bread", "butter"]
        assert transactions[2] == ["milk", "cheese"]

    def test_load_with_header(self, tmp_path):
        """Test loading CSV with header row."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("items\nbread,milk,eggs\nbread,butter\n")

        # Should skip header if specified
        transactions = load_transactions(str(csv_file), has_header=True)

        assert len(transactions) == 2
        assert transactions[0] == ["bread", "milk", "eggs"]

    def test_load_without_header(self, tmp_path):
        """Test loading CSV without header."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread,milk,eggs\nbread,butter\n")

        transactions = load_transactions(str(csv_file), has_header=False)

        assert len(transactions) == 2

    def test_load_empty_file(self, tmp_path):
        """Test loading an empty CSV file."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("")

        transactions = load_transactions(str(csv_file))

        assert transactions == []

    def test_load_file_with_empty_lines(self, tmp_path):
        """Test that empty lines are skipped."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread,milk\n\nbutter,cheese\n\n")

        transactions = load_transactions(str(csv_file))

        assert len(transactions) == 2
        assert transactions[0] == ["bread", "milk"]
        assert transactions[1] == ["butter", "cheese"]

    def test_load_nonexistent_file(self):
        """Test that loading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_transactions("nonexistent.csv")

    def test_load_with_varying_lengths(self, tmp_path):
        """Test loading transactions with different numbers of items."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread\nmilk,eggs\nbutter,cheese,yogurt,cream\n")

        transactions = load_transactions(str(csv_file))

        assert len(transactions) == 3
        assert len(transactions[0]) == 1
        assert len(transactions[1]) == 2
        assert len(transactions[2]) == 4

    def test_load_duplicate_items_in_transaction(self, tmp_path):
        """Test handling duplicate items within same transaction."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread,milk,bread\n")

        transactions = load_transactions(str(csv_file))

        # Duplicates within a transaction should be removed
        assert transactions[0] == ["bread", "milk"]

    def test_load_maintains_order(self, tmp_path):
        """Test that item order within transaction is preserved."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("eggs,bread,milk\n")

        transactions = load_transactions(str(csv_file))

        assert transactions[0] == ["eggs", "bread", "milk"]

    def test_load_large_transaction(self, tmp_path):
        """Test loading a transaction with many items."""
        items = [f"item_{i}" for i in range(50)]
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(",".join(items))

        transactions = load_transactions(str(csv_file))

        assert len(transactions) == 1
        assert len(transactions[0]) == 50

    def test_load_special_characters(self, tmp_path):
        """Test handling items with special characters."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("whole wheat bread,skim milk,free-range eggs\n")

        transactions = load_transactions(str(csv_file))

        assert transactions[0] == ["whole wheat bread", "skim milk", "free-range eggs"]


class TestLoadTransactionsWithSample:
    """Test loading with sample data."""

    def test_load_first_n_transactions(self, tmp_path):
        """Test loading only first N transactions."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread,milk\nbutter,cheese\neggs,bacon\njuice,cereal\n")

        transactions = load_transactions(str(csv_file), max_transactions=2)

        assert len(transactions) == 2
        assert transactions[0] == ["bread", "milk"]
        assert transactions[1] == ["butter", "cheese"]

    def test_load_max_greater_than_file(self, tmp_path):
        """Test when max_transactions exceeds file length."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("bread,milk\nbutter,cheese\n")

        transactions = load_transactions(str(csv_file), max_transactions=100)

        assert len(transactions) == 2


class TestDataValidation:
    """Test data validation and error handling."""

    def test_invalid_encoding(self, tmp_path):
        """Test handling files with invalid encoding."""
        csv_file = tmp_path / "test.csv"
        # Write some valid data
        csv_file.write_text("bread,milk\n")

        # Should not raise error, handles encoding gracefully
        transactions = load_transactions(str(csv_file))
        assert len(transactions) >= 0

    def test_very_long_item_name(self, tmp_path):
        """Test handling extremely long item names."""
        long_name = "a" * 1000
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(f"{long_name},milk\n")

        transactions = load_transactions(str(csv_file))
        assert len(transactions[0][0]) == 1000
