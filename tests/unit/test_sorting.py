"""
Unit tests for custom sorting algorithms (TDD).
"""

import pytest
from src.algorithms.sorting import (
    merge_sort,
    sort_pairs_by_frequency,
    sort_associations_by_weight,
)


class TestMergeSort:
    """Tests for merge_sort function."""

    def test_empty_list(self):
        """Sorting empty list returns empty list."""
        assert merge_sort([]) == []

    def test_single_element(self):
        """Sorting single element returns same element."""
        assert merge_sort([5]) == [5]

    def test_two_elements_sorted(self):
        """Already sorted two elements stay sorted."""
        assert merge_sort([1, 2]) == [1, 2]

    def test_two_elements_unsorted(self):
        """Unsorted two elements get sorted."""
        assert merge_sort([2, 1]) == [1, 2]

    def test_multiple_elements(self):
        """Multiple elements get sorted correctly."""
        assert merge_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_reverse_order(self):
        """Reverse flag sorts descending."""
        assert merge_sort([1, 3, 2], reverse=True) == [3, 2, 1]

    def test_with_key_function(self):
        """Key function extracts comparison value."""
        items = [("a", 3), ("b", 1), ("c", 2)]
        result = merge_sort(items, key=lambda x: x[1])
        assert result == [("b", 1), ("c", 2), ("a", 3)]

    def test_key_with_reverse(self):
        """Key function combined with reverse."""
        items = [("a", 3), ("b", 1), ("c", 2)]
        result = merge_sort(items, key=lambda x: x[1], reverse=True)
        assert result == [("a", 3), ("c", 2), ("b", 1)]

    def test_does_not_modify_original(self):
        """Original list is not modified."""
        original = [3, 1, 2]
        merge_sort(original)
        assert original == [3, 1, 2]

    def test_strings(self):
        """Sorting strings alphabetically."""
        assert merge_sort(["banana", "apple", "cherry"]) == [
            "apple",
            "banana",
            "cherry",
        ]

    def test_duplicates(self):
        """Handles duplicate values correctly."""
        assert merge_sort([3, 1, 3, 2, 1]) == [1, 1, 2, 3, 3]

    def test_negative_numbers(self):
        """Handles negative numbers."""
        assert merge_sort([3, -1, 0, -5, 2]) == [-5, -1, 0, 2, 3]


class TestSortPairsByFrequency:
    """Tests for sort_pairs_by_frequency function."""

    def test_empty_list(self):
        """Empty list returns empty."""
        assert sort_pairs_by_frequency([]) == []

    def test_single_pair(self):
        """Single pair returned as-is."""
        pairs = [("milk", "bread", 5)]
        assert sort_pairs_by_frequency(pairs) == [("milk", "bread", 5)]

    def test_sorts_descending_by_default(self):
        """Pairs sorted by frequency descending."""
        pairs = [("a", "b", 10), ("c", "d", 50), ("e", "f", 25)]
        result = sort_pairs_by_frequency(pairs)
        assert result == [("c", "d", 50), ("e", "f", 25), ("a", "b", 10)]

    def test_ascending_order(self):
        """Can sort ascending with reverse=False."""
        pairs = [("a", "b", 10), ("c", "d", 50), ("e", "f", 25)]
        result = sort_pairs_by_frequency(pairs, reverse=False)
        assert result == [("a", "b", 10), ("e", "f", 25), ("c", "d", 50)]


class TestSortAssociationsByWeight:
    """Tests for sort_associations_by_weight function."""

    def test_empty_list(self):
        """Empty list returns empty."""
        assert sort_associations_by_weight([]) == []

    def test_single_association(self):
        """Single association returned as-is."""
        assocs = [("milk", 5)]
        assert sort_associations_by_weight(assocs) == [("milk", 5)]

    def test_sorts_descending_by_default(self):
        """Associations sorted by weight descending."""
        assocs = [("milk", 10), ("bread", 50), ("eggs", 25)]
        result = sort_associations_by_weight(assocs)
        assert result == [("bread", 50), ("eggs", 25), ("milk", 10)]

    def test_ascending_order(self):
        """Can sort ascending with reverse=False."""
        assocs = [("milk", 10), ("bread", 50), ("eggs", 25)]
        result = sort_associations_by_weight(assocs, reverse=False)
        assert result == [("milk", 10), ("eggs", 25), ("bread", 50)]
