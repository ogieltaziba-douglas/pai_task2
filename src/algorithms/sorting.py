"""
Custom sorting algorithms for market basket analysis.
Implements merge sort to replace built-in sorted() function.
"""

from typing import List, Tuple, Callable, Any


def merge_sort(
    items: List[Any], key: Callable = None, reverse: bool = False
) -> List[Any]:
    """
    Sort a list using merge sort algorithm.

    Args:
        items: List of items to sort
        key: Optional function to extract comparison key from each item
        reverse: If True, sort in descending order

    Returns:
        New sorted list (does not modify original)

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Handle empty or single-item lists
    if len(items) <= 1:
        return list(items)

    # Create a copy to avoid modifying original
    arr = list(items)

    # Use identity function if no key provided
    if key is None:
        key = lambda x: x

    def _merge(left: List[Any], right: List[Any]) -> List[Any]:
        """Merge two sorted lists into one sorted list."""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            left_key = key(left[i])
            right_key = key(right[j])

            if reverse:
                # Descending order
                if left_key >= right_key:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            else:
                # Ascending order
                if left_key <= right_key:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

        # Append remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _merge_sort(arr: List[Any]) -> List[Any]:
        """Recursive merge sort implementation."""
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])

        return _merge(left, right)

    return _merge_sort(arr)


def sort_pairs_by_frequency(
    pairs: List[Tuple[str, str, int]], reverse: bool = True
) -> List[Tuple[str, str, int]]:
    """
    Sort item pairs by their frequency (weight).

    Args:
        pairs: List of (item1, item2, frequency) tuples
        reverse: If True (default), sort descending (highest first)

    Returns:
        Sorted list of pairs
    """
    return merge_sort(pairs, key=lambda x: x[2], reverse=reverse)


def sort_associations_by_weight(
    associations: List[Tuple[str, int]], reverse: bool = True
) -> List[Tuple[str, int]]:
    """
    Sort item associations by their weight.

    Args:
        associations: List of (item, weight) tuples
        reverse: If True (default), sort descending (highest first)

    Returns:
        Sorted list of associations
    """
    return merge_sort(associations, key=lambda x: x[1], reverse=reverse)
