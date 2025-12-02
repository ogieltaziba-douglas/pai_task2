"""
Graph data structure for Market Basket Analysis.
Represents items as nodes and co-purchase relationships as weighted edges.
"""
from typing import Dict, List, Tuple


class Graph:
    """
    Undirected weighted graph for representing item co-purchase relationships.
    
    Nodes represent grocery items.
    Edges represent co-purchase relationships.
    Edge weights represent frequency of co-occurrence.
    
    Time Complexity:
        - add_node: O(1)
        - add_edge: O(1)
        - has_node: O(1)
        - has_edge: O(1)
        - get_neighbors: O(1)
        - get_edge_weight: O(1)
    
    Space Complexity: O(V + E) where V is nodes and E is edges
    """
    
    def __init__(self):
        """
        Initialize an empty graph.
        
        Uses adjacency list representation: {item: {neighbor: weight, ...}}
        """
        self._adjacency_list: Dict[str, Dict[str, int]] = {}
    
    def add_node(self, item: str) -> None:
        """
        Add a node to the graph.
        
        Args:
            item: The item name to add as a node
            
        Note:
            If node already exists, this is a no-op.
        """
        if item not in self._adjacency_list:
            self._adjacency_list[item] = {}
    
    def add_edge(self, item1: str, item2: str, weight: int = 1) -> None:
        """
        Add an edge between two items with given weight.
        
        If edge already exists, the weight is added to the existing weight.
        This is an undirected graph, so edge is added in both directions.
        
        Args:
            item1: First item name
            item2: Second item name
            weight: Edge weight (default: 1)
            
        Raises:
            ValueError: If item names are empty, identical (self-loop), 
                       or weight is non-positive
        """
        # Validation
        if not item1 or not item2:
            raise ValueError("Item names cannot be empty")
        
        if item1 == item2:
            raise ValueError("Self-loops are not allowed")
        
        if weight <= 0:
            raise ValueError("Weight must be positive")
        
        # Add nodes if they don't exist
        self.add_node(item1)
        self.add_node(item2)
        
        # Add edge in both directions (undirected graph)
        # If edge exists, add to existing weight
        if item2 in self._adjacency_list[item1]:
            self._adjacency_list[item1][item2] += weight
            self._adjacency_list[item2][item1] += weight
        else:
            self._adjacency_list[item1][item2] = weight
            self._adjacency_list[item2][item1] = weight
    
    def has_node(self, item: str) -> bool:
        """
        Check if a node exists in the graph.
        
        Args:
            item: Item name to check
            
        Returns:
            True if node exists, False otherwise
        """
        return item in self._adjacency_list
    
    def has_edge(self, item1: str, item2: str) -> bool:
        """
        Check if an edge exists between two items.
        
        Args:
            item1: First item name
            item2: Second item name
            
        Returns:
            True if edge exists, False otherwise
        """
        if item1 not in self._adjacency_list:
            return False
        return item2 in self._adjacency_list[item1]
    
    def get_neighbors(self, item: str) -> Dict[str, int]:
        """
        Get all neighbors of an item with their edge weights.
        
        Args:
            item: Item name
            
        Returns:
            Dictionary mapping neighbor items to edge weights
            
        Raises:
            KeyError: If item not found in graph
        """
        if item not in self._adjacency_list:
            raise KeyError(f"Item '{item}' not found in graph")
        
        # Return a copy to prevent external modification
        return self._adjacency_list[item].copy()
    
    def get_edge_weight(self, item1: str, item2: str) -> int:
        """
        Get the weight of an edge between two items.
        
        Args:
            item1: First item name
            item2: Second item name
            
        Returns:
            Edge weight, or 0 if edge doesn't exist
        """
        if not self.has_edge(item1, item2):
            return 0
        return self._adjacency_list[item1][item2]
    
    def get_all_nodes(self) -> List[str]:
        """
        Get all nodes in the graph.
        
        Returns:
            List of all item names in the graph
        """
        return list(self._adjacency_list.keys())
    
    def get_all_edges(self) -> List[Tuple[str, str, int]]:
        """
        Get all edges in the graph as list of tuples.
        
        Returns:
            List of tuples (item1, item2, weight) representing edges.
            Each edge appears once (not duplicated for undirected).
        """
        edges = []
        seen = set()
        
        for item1, neighbors in self._adjacency_list.items():
            for item2, weight in neighbors.items():
                # Create a canonical edge representation to avoid duplicates
                edge = tuple(sorted([item1, item2]))
                if edge not in seen:
                    seen.add(edge)
                    edges.append((item1, item2, weight))
        
        return edges
    
    def remove_node(self, item: str) -> None:
        """
        Remove a node and all its edges from the graph.
        
        Args:
            item: Item name to remove
            
        Note:
            If item doesn't exist, this is a no-op.
        """
        if item not in self._adjacency_list:
            return
        
        # Remove all edges to this node from other nodes
        neighbors = list(self._adjacency_list[item].keys())
        for neighbor in neighbors:
            if neighbor in self._adjacency_list:
                self._adjacency_list[neighbor].pop(item, None)
        
        # Remove the node itself
        del self._adjacency_list[item]
    
    def remove_edge(self, item1: str, item2: str) -> None:
        """
        Remove an edge between two items.
        
        Args:
            item1: First item name
            item2: Second item name
            
        Note:
            If edge doesn't exist, this is a no-op.
        """
        if self.has_edge(item1, item2):
            del self._adjacency_list[item1][item2]
            del self._adjacency_list[item2][item1]
    
    def node_count(self) -> int:
        """
        Get the number of nodes in the graph.
        
        Returns:
            Number of nodes
        """
        return len(self._adjacency_list)
    
    def edge_count(self) -> int:
        """
        Get the number of edges in the graph.
        
        Returns:
            Number of unique edges (counting each undirected edge once)
        """
        total = sum(len(neighbors) for neighbors in self._adjacency_list.values())
        # Divide by 2 since each edge is stored twice (undirected)
        return total // 2
    
    def degree(self, item: str) -> int:
        """
        Get the degree (number of neighbors) of a node.
        
        Args:
            item: Item name
            
        Returns:
            Number of neighbors (degree)
            
        Raises:
            KeyError: If item not found in graph
        """
        if item not in self._adjacency_list:
            raise KeyError(f"Item '{item}' not found in graph")
        
        return len(self._adjacency_list[item])
    
    def is_empty(self) -> bool:
        """
        Check if the graph is empty (no nodes).
        
        Returns:
            True if graph has no nodes, False otherwise
        """
        return len(self._adjacency_list) == 0
    
    def __str__(self) -> str:
        """
        String representation of the graph.
        
        Returns:
            Human-readable string showing nodes and edges
        """
        if self.is_empty():
            return "Graph(empty)"
        
        lines = [f"Graph with {self.node_count()} nodes and {self.edge_count()} edges:"]
        for item, neighbors in sorted(self._adjacency_list.items()):
            if neighbors:
                neighbor_str = ", ".join(f"{n}({w})" for n, w in sorted(neighbors.items()))
                lines.append(f"  {item}: {neighbor_str}")
            else:
                lines.append(f"  {item}: (isolated)")
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """
        Repr representation of the graph.
        
        Returns:
            String representation for debugging
        """
        return f"Graph({self.node_count()} nodes, {self.edge_count()} edges)"
