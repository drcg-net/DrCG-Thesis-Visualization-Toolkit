"""Graph and diagram generation for space syntax and adjacency visualizations."""

import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from typing import Dict, List, Optional, Tuple
import logging
import json

logger = logging.getLogger(__name__)


def parse_adjacency_matrix(df: pd.DataFrame, source_col: str = None, target_col: str = None, weight_col: str = None) -> nx.Graph:
    """Parse adjacency data and create NetworkX graph."""
    if source_col is None:
        source_col = df.columns[0]
    if target_col is None:
        target_col = df.columns[1]
    if weight_col is None and len(df.columns) > 2:
        weight_col = df.columns[2]
    
    G = nx.Graph()
    
    for _, row in df.iterrows():
        src = row[source_col]
        tgt = row[target_col]
        weight = row[weight_col] if weight_col and weight_col in df.columns else 1.0
        
        G.add_edge(src, tgt, weight=float(weight))
    
    logger.info(f"Created graph with {len(G.nodes())} nodes and {len(G.edges())} edges")
    return G


def create_space_syntax_diagram(
    df: pd.DataFrame,
    layout: str = "spring",
    title: str = "Space Syntax Accessibility Graph",
) -> go.Figure:
    """
    Create a space syntax-style accessibility diagram.
    
    Shows connectivity and hierarchical relationships between spaces.
    """
    G = parse_adjacency_matrix(df)
    
    if layout == "spring":
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "hierarchical":
        pos = nx.spring_layout(G, k=3)
    else:
        pos = nx.spring_layout(G)
    
    # Calculate node sizes based on degree centrality
    degrees = dict(G.degree())
    max_degree = max(degrees.values()) if degrees else 1
    node_sizes = [10 + 30 * (degrees[node] / max_degree) for node in G.nodes()]
    
    # Calculate edge widths based on weight
    edge_widths = []
    for u, v in G.edges():
        weight = G[u][v].get("weight", 1.0)
        edge_widths.append(weight * 2)
    
    edge_x = []
    edge_y = []
    edge_width_list = []
    
    for i, edge in enumerate(G.edges()):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_width_list.extend([edge_widths[i], edge_widths[i], None])
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="rgba(0,0,0,0.4)"),
        hoverinfo="none",
        showlegend=False,
    )
    
    # Node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = list(G.nodes())
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        textfont=dict(size=10),
        hoverinfo="text",
        marker=dict(
            size=node_sizes,
            color=[degrees.get(node, 1) for node in G.nodes()],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Connectivity"),
        ),
        showlegend=False,
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(255,255,255,1)",
    )
    
    return fig


def create_circulation_diagram(
    df: pd.DataFrame,
    primary_path_col: str = None,
    secondary_path_col: str = None,
    title: str = "Circulation Diagram",
) -> go.Figure:
    """
    Create a circulation path diagram showing primary and secondary routes.
    """
    G = parse_adjacency_matrix(df)
    pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
    
    # Draw edges
    edge_x = []
    edge_y = []
    edge_color = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_color.extend(["rgba(100,100,150,0.5)", "rgba(100,100,150,0.5)", None])
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="rgba(0, 100, 200, 0.6)"),
        hoverinfo="none",
        showlegend=False,
    )
    
    # Node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(G.nodes()),
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            size=25,
            color="#4472C4",
            line=dict(color="#2F5496", width=2),
        ),
        showlegend=False,
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(240,240,240,1)",
        paper_bgcolor="rgba(255,255,255,1)",
        font=dict(family="Times New Roman, serif", size=11),
    )
    
    return fig


def calculate_graph_metrics(G: nx.Graph) -> Dict:
    """Calculate network metrics for the graph."""
    return {
        "nodes": len(G.nodes()),
        "edges": len(G.edges()),
        "density": nx.density(G),
        "average_degree": 2 * len(G.edges()) / len(G.nodes()) if len(G.nodes()) > 0 else 0,
        "average_clustering": nx.average_clustering(G),
        "diameter": nx.diameter(G) if nx.is_connected(G) else -1,
        "connected_components": nx.number_connected_components(G),
    }


def create_adjacency_matrix_heatmap(
    df: pd.DataFrame,
    node1_col: str = None,
    node2_col: str = None,
    weight_col: str = None,
    title: str = "Adjacency Matrix",
) -> go.Figure:
    """Create a heatmap visualization of adjacency relationships."""
    G = parse_adjacency_matrix(df, node1_col, node2_col, weight_col)
    
    # Create adjacency matrix
    nodes = sorted(list(G.nodes()))
    adj_matrix = nx.to_pandas_adjacency(G, nodelist=nodes, weight=weight_col)
    
    fig = go.Figure(
        data=go.Heatmap(
            z=adj_matrix.values,
            x=adj_matrix.columns,
            y=adj_matrix.index,
            colorscale="Blues",
            text=adj_matrix.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 10},
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title="Space/Node",
        yaxis_title="Space/Node",
        font=dict(family="Times New Roman, serif", size=11),
    )
    
    return fig


def export_graph_format(G: nx.Graph, format_type: str = "graphml") -> str:
    """Export graph in various formats."""
    if format_type == "graphml":
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".graphml") as f:
            nx.write_graphml(G, f)
            return f.name
    elif format_type == "gexf":
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".gexf") as f:
            nx.write_gexf(G, f)
            return f.name
    elif format_type == "json":
        data = nx.node_link_data(G)
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            json.dump(data, f, indent=2)
            return f.name
    else:
        raise ValueError(f"Unsupported format: {format_type}")
