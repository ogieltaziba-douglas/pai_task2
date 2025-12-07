"""
Market Basket Analysis - PyVis Network Visualization
Enhanced version with PyVis for interactive network graphs
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import os
import sys
from pathlib import Path
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from algorithms.graph_builder import build_graph_from_transactions
from analysis.frequent_items import (
    find_items_bought_with,
    get_top_bundles,
    get_frequent_pairs,
)

try:
    from pyvis.network import Network

    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False


# Page configuration
st.set_page_config(page_title="Market Basket Analysis", layout="wide")


@st.cache_data
def load_supermarket_data(max_transactions=None):
    """Load and cache the supermarket dataset."""
    import csv
    from collections import defaultdict

    filepath = "data/raw/Supermarket_dataset_PAI.csv"

    if not os.path.exists(filepath):
        st.error(f"Dataset not found at {filepath}")
        return None

    transactions_dict = defaultdict(list)

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

    return transactions


@st.cache_data
def build_graph_cached(transactions):
    """Build and cache the graph."""
    return build_graph_from_transactions(transactions)


def create_pyvis_network(graph, max_edges=50, physics_enabled=True):
    """Create interactive network using PyVis with improved edge visibility."""
    if not PYVIS_AVAILABLE:
        return None

    # Get top edges
    all_edges = get_frequent_pairs(graph, min_frequency=1)
    sorted_edges = sorted(all_edges, key=lambda x: x[2], reverse=True)[:max_edges]

    if not sorted_edges:
        return None

    # Create network
    net = Network(
        height="700px",
        width="100%",
        bgcolor="#1a1a2e",
        font_color="white",
    )

    # Add nodes and edges
    added_nodes = set()
    max_weight = sorted_edges[0][2] if sorted_edges else 1

    # Color palette for nodes
    node_colors = [
        "#4fc3f7",
        "#81c784",
        "#ffb74d",
        "#f06292",
        "#ba68c8",
        "#4dd0e1",
        "#aed581",
        "#ff8a65",
    ]

    for idx, (item1, item2, weight) in enumerate(sorted_edges):
        # Add nodes with colors
        if item1 not in added_nodes:
            degree = graph.degree(item1)
            color = node_colors[hash(item1) % len(node_colors)]
            net.add_node(
                item1,
                label=item1[:20],
                title=f"{item1}\nConnections: {degree}",
                size=12 + degree * 0.3,
                color=color,
                borderWidth=2,
                borderWidthSelected=4,
            )
            added_nodes.add(item1)

        if item2 not in added_nodes:
            degree = graph.degree(item2)
            color = node_colors[hash(item2) % len(node_colors)]
            net.add_node(
                item2,
                label=item2[:20],
                title=f"{item2}\nConnections: {degree}",
                size=12 + degree * 0.3,
                color=color,
                borderWidth=2,
                borderWidthSelected=4,
            )
            added_nodes.add(item2)

        # Add edge with smooth curves
        edge_width = 0.5 + (weight / max_weight) * 2
        net.add_edge(
            item1,
            item2,
            value=weight,
            title=f"{item1} + {item2}\nBought together: {weight} times",
            width=edge_width,
            smooth={"type": "curvedCW", "roundness": 0.2},
        )

    # Configure options with hover highlighting
    options = (
        """
    {
      "nodes": {
        "font": {"size": 12, "face": "arial"},
        "shadow": true
      },
      "edges": {
        "color": {
          "inherit": false,
          "color": "#848484",
          "highlight": "#00ff00",
          "hover": "#ffff00"
        },
        "smooth": {
          "type": "curvedCW",
          "roundness": 0.15
        },
        "hoverWidth": 3,
        "selectionWidth": 4
      },
      "interaction": {
        "hover": true,
        "hoverConnectedEdges": true,
        "selectConnectedEdges": true,
        "tooltipDelay": 100,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false
      },
      "physics": {
        "enabled": """
        + str(physics_enabled).lower()
        + """,
        "barnesHut": {
          "gravitationalConstant": -40000,
          "centralGravity": 0.15,
          "springLength": 250,
          "springConstant": 0.04,
          "damping": 0.2,
          "avoidOverlap": 0.5
        },
        "minVelocity": 0.75,
        "stabilization": {
          "enabled": true,
          "iterations": 150
        }
      }
    }
    """
    )
    net.set_options(options)

    return net


def main():
    """Main application."""

    # Title
    st.title("Market Basket Analysis")
    st.markdown("Analyze customer purchasing patterns and visualize item associations")

    # Sidebar
    st.sidebar.header("Settings")
    max_transactions = st.sidebar.slider(
        "Number of transactions", min_value=100, max_value=15000, value=5000, step=500
    )

    # Load data
    with st.spinner("Loading data..."):
        transactions = load_supermarket_data(max_transactions)

        if transactions is None:
            st.stop()

        graph = build_graph_cached(transactions)

    st.sidebar.success(f"{len(transactions)} transactions")
    st.sidebar.info(f"{graph.node_count()} unique items")
    st.sidebar.info(f"{graph.edge_count():,} item pairs")

    # Check PyVis availability
    if not PYVIS_AVAILABLE:
        st.warning("PyVis not installed. Run: `pip install pyvis`")
        st.info("Showing limited features without network visualization.")

    # Tabs - Analysis, Top Bundles, then Network
    if PYVIS_AVAILABLE:
        tab1, tab2, tab3 = st.tabs(["Analysis", "Top Bundles", "Network Visualization"])
    else:
        tab1, tab2 = st.tabs(["Analysis", "Top Bundles"])

    # TAB 1: Analysis
    with tab1:
        st.header("Item Association Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Find Associations")
            item_list = sorted(graph.get_all_nodes())
            selected_item = st.selectbox(
                "Select an item:",
                item_list,
                index=item_list.index("whole milk") if "whole milk" in item_list else 0,
            )
            top_n_assoc = st.slider("Number of associations:", 1, 20, 5)

            if selected_item:
                associations = find_items_bought_with(
                    graph, selected_item, limit=top_n_assoc
                )

                st.write(f"**Top {top_n_assoc} items bought with '{selected_item}':**")

                if associations:
                    for item, weight in associations:
                        st.write(f"- **{item}** (Frequency: {weight})")
                else:
                    st.info("No associations found")

        with col2:
            st.subheader("Visualize Associations")

            if selected_item:
                associations = find_items_bought_with(graph, selected_item, limit=15)

                if associations:
                    df = pd.DataFrame(associations, columns=["Item", "Frequency"])

                    fig = px.bar(
                        df,
                        x="Frequency",
                        y="Item",
                        orientation="h",
                        color="Frequency",
                        color_continuous_scale="oranges",
                    )
                    fig.update_layout(
                        height=400,
                        yaxis={"categoryorder": "total ascending"},
                        title=f"Items bought with '{selected_item}'",
                    )
                    st.plotly_chart(fig, use_container_width=True)

    # TAB 3: Network Visualization (PyVis)
    if PYVIS_AVAILABLE:
        with tab3:
            st.header("Interactive Item Network")
            st.markdown(
                "**Explore relationships between items in an interactive graph**"
            )

            col1, col2 = st.columns([3, 1])

            with col2:
                max_edges = st.slider(
                    "Max edges to show:",
                    min_value=10,
                    max_value=200,
                    value=50,
                    step=10,
                    help="Controls how many relationships to display",
                )
                physics = st.checkbox("Enable Physics Layout", value=True)

                st.info(
                    "Tips:\n- Drag nodes to rearrange\n- Scroll to zoom\n- Click nodes for info"
                )

            with col1:
                with st.spinner("Generating interactive network..."):
                    net = create_pyvis_network(
                        graph, max_edges=max_edges, physics_enabled=physics
                    )

                    if net:
                        # Save to temp file and display
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".html", mode="w"
                        ) as tmp:
                            net.save_graph(tmp.name)
                            with open(tmp.name, "r") as f:
                                html_content = f.read()
                            components.html(html_content, height=700, scrolling=False)

                            # Clean up
                            os.unlink(tmp.name)
                    else:
                        st.warning("Not enough data to generate network.")

    # TAB 2: Top Bundles
    with tab2:
        st.header("Top Product Bundles")

        # Get all bundles first to determine max values
        all_bundles = get_top_bundles(graph, n=500)
        max_bundle_count = len(all_bundles)
        max_frequency = all_bundles[0][2] if all_bundles else 1

        num_bundles = st.slider(
            "Number of bundles to show:",
            min_value=5,
            max_value=min(max_bundle_count, 100),
            value=min(20, max_bundle_count),
            step=5,
        )
        min_freq = st.slider(
            "Minimum frequency:",
            min_value=1,
            max_value=max(max_frequency // 2, 10),
            value=5,
            step=1,
        )

        top_bundles = get_top_bundles(graph, n=num_bundles)
        filtered = [(i1, i2, w) for i1, i2, w in top_bundles if w >= min_freq]

        if filtered:
            df = pd.DataFrame(filtered, columns=["Item 1", "Item 2", "Frequency"])
            df["Bundle"] = df["Item 1"] + " + " + df["Item 2"]

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = px.bar(
                    df,
                    x="Frequency",
                    y="Bundle",
                    orientation="h",
                    title=f"Top {len(filtered)} Product Bundles",
                    color="Frequency",
                    color_continuous_scale="viridis",
                )
                fig.update_layout(
                    height=max(400, len(filtered) * 20),
                    yaxis={"categoryorder": "total ascending"},
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.dataframe(
                    df[["Item 1", "Item 2", "Frequency"]],
                    height=max(400, len(filtered) * 20),
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.warning("No bundles found with specified frequency.")


if __name__ == "__main__":
    main()
