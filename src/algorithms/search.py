"""
Search algorithms for graph traversal.
Implements BFS and DFS for finding item associations.
"""
from typing import Dict, List, Set
from collections import deque
from src.data_structures.graph import Graph


def bfs(graph: Graph, start: str, max_depth: int = None) -> Dict[str, int]:
    """
    Breadth-First Search traversal from a starting node.
    
    Explores nodes level by level, visiting all neighbors at depth N
    before moving to depth N+1.
    
    Args:
        graph: Graph to search
        start: Starting node
        max_depth: Maximum depth to explore (None = unlimited)
        
    Returns:
        Dictionary mapping node names to their depth from start
        
    Raises:
        KeyError: If start node not found in graph
        
    Time Complexity: O(V + E) where V = nodes, E = edges
    Space Complexity: O(V) for visited tracking
    """
    # Check if start node exists
    if not graph.has_node(start):
        raise KeyError(f"Node '{start}' not found in graph")
    
    # Initialize
    visited = {start: 0}  # Maps node to depth
    queue = deque([(start, 0)])  # Queue of (node, depth) tuples
    
    while queue:
        current, depth = queue.popleft()
        
        # Check max_depth limit
        if max_depth is not None and depth >= max_depth:
            continue
        
        # Explore neighbors
        neighbors = graph.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in visited:
                visited[neighbor] = depth + 1
                queue.append((neighbor, depth + 1))
    
    return visited


def dfs(graph: Graph, start: str, max_depth: int = None) -> List[str]:
    """
    Depth-First Search traversal from a starting node.
    
    Explores as far as possible along each branch before backtracking.
    
    Args:
        graph: Graph to search
        start: Starting node
        max_depth: Maximum depth to explore (None = unlimited)
        
    Returns:
        List of nodes in the order they were visited
        
    Raises:
        KeyError: If start node not found in graph
        
    Time Complexity: O(V + E) where V = nodes, E = edges
    Space Complexity: O(V) for visited tracking
    """
    # Check if start node exists
    if not graph.has_node(start):
        raise KeyError(f"Node '{start}' not found in graph")
    
    visited = []
    visited_set = set()
    
    def _dfs_recursive(node: str, depth: int):
        """Helper function for recursive DFS."""
        # Mark as visited
        visited.append(node)
        visited_set.add(node)
        
        # Check max_depth limit
        if max_depth is not None and depth >= max_depth:
            return
        
        # Explore neighbors
        neighbors = graph.get_neighbors(node)
        for neighbor in neighbors:
            if neighbor not in visited_set:
                _dfs_recursive(neighbor, depth + 1)
    
    # Start DFS from start node
    _dfs_recursive(start, 0)
    
    return visited
