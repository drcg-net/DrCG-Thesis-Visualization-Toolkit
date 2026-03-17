"""Chart builders using Plotly."""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_layout_config():
    """Get common layout configuration for thesis mode."""
    return {
        "template": "plotly_white",
        "font": {"family": "Times New Roman, serif", "size": 12},
        "margin": {"l": 80, "r": 40, "t": 60, "b": 60},
        "plot_bgcolor": "rgba(255,255,255,1)",
        "paper_bgcolor": "rgba(255,255,255,1)",
        "showlegend": True,
        "hovermode": "closest",
    }


def build_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Bar Chart",
    x_label: str = None,
    y_label: str = None,
    color: Optional[str] = None,
    sort_by: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build a bar chart."""
    df_plot = df.copy()
    
    if sort_by:
        df_plot = df_plot.sort_values(by=sort_by, ascending=False)
    
    fig = px.bar(
        df_plot,
        x=x,
        y=y,
        color=color,
        title=title,
        labels={x: x_label or x, y: y_label or y},
    )
    
    fig.update_layout(get_layout_config())
    return fig


def build_grouped_bar(
    df: pd.DataFrame,
    x: str,
    y_columns: List[str],
    title: str = "Grouped Bar",
    x_label: str = None,
    y_label: str = None,
    **kwargs
) -> go.Figure:
    """Build a grouped bar chart."""
    fig = go.Figure()
    
    for y_col in y_columns:
        fig.add_trace(
            go.Bar(x=df[x], y=df[y_col], name=y_col)
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label or x,
        yaxis_title=y_label or "Value",
        barmode="group",
        **get_layout_config(),
    )
    return fig


def build_stacked_bar(
    df: pd.DataFrame,
    x: str,
    y_columns: List[str],
    title: str = "Stacked Bar",
    x_label: str = None,
    y_label: str = None,
    **kwargs
) -> go.Figure:
    """Build a stacked bar chart."""
    fig = go.Figure()
    
    for y_col in y_columns:
        fig.add_trace(
            go.Bar(x=df[x], y=df[y_col], name=y_col)
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label or x,
        yaxis_title=y_label or "Value",
        barmode="stack",
        **get_layout_config(),
    )
    return fig


def build_stacked_bar_100(
    df: pd.DataFrame,
    x: str,
    y_columns: List[str],
    title: str = "100% Stacked Bar",
    x_label: str = None,
    y_label: str = None,
    **kwargs
) -> go.Figure:
    """Build a 100% stacked bar chart."""
    fig = go.Figure()
    
    for y_col in y_columns:
        fig.add_trace(
            go.Bar(x=df[x], y=df[y_col], name=y_col)
        )
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label or x,
        yaxis_title=y_label or "Percentage (%)",
        barmode="relative",
        **get_layout_config(),
    )
    
    fig.update_yaxes(tickformat=".0%")
    return fig


def build_line(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Line Chart",
    x_label: str = None,
    y_label: str = None,
    color: Optional[str] = None,
    markers: bool = True,
    **kwargs
) -> go.Figure:
    """Build a line chart."""
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        markers=markers,
        labels={x: x_label or x, y: y_label or y},
    )
    fig.update_layout(get_layout_config())
    return fig


def build_area(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Area Chart",
    x_label: str = None,
    y_label: str = None,
    color: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build an area chart."""
    fig = px.area(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        labels={x: x_label or x, y: y_label or y},
    )
    fig.update_layout(get_layout_config())
    return fig


def build_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Scatter Plot",
    x_label: str = None,
    y_label: str = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    hover_text: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build a scatter plot."""
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_data=[hover_text] if hover_text else None,
        title=title,
        labels={x: x_label or x, y: y_label or y},
    )
    fig.update_layout(get_layout_config())
    return fig


def build_bubble(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    title: str = "Bubble Chart",
    x_label: str = None,
    y_label: str = None,
    color: Optional[str] = None,
    hover_text: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build a bubble chart."""
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_data=[hover_text] if hover_text else None,
        title=title,
        labels={x: x_label or x, y: y_label or y},
    )
    fig.update_traces(marker=dict(sizemode="diameter"))
    fig.update_layout(get_layout_config())
    return fig


def build_box(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Box Plot",
    x_label: str = None,
    y_label: str = None,
    color: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build a box plot."""
    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        labels={x: x_label or x, y: y_label or y},
    )
    fig.update_layout(get_layout_config())
    return fig


def build_violin(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "Violin Plot",
    x_label: str = None,
    y_label: str = None,
    color: Optional[str] = None,
    points: bool = False,
    **kwargs
) -> go.Figure:
    """Build a violin plot."""
    fig = px.violin(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        box=True,
        points="outliers" if points else False,
        labels={x: x_label or x, y: y_label or y},
    )
    fig.update_layout(get_layout_config())
    return fig


def build_histogram(
    df: pd.DataFrame,
    x: str,
    title: str = "Histogram",
    x_label: str = None,
    y_label: str = "Count",
    nbins: int = 20,
    color: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build a histogram."""
    fig = px.histogram(
        df,
        x=x,
        nbins=nbins,
        color=color,
        title=title,
        labels={x: x_label or x, "count": y_label},
    )
    fig.update_layout(get_layout_config())
    return fig


def build_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    values: str,
    title: str = "Heatmap",
    colorscale: str = "RdBu",
    annotations: bool = False,
    **kwargs
) -> go.Figure:
    """Build a heatmap."""
    pivot_df = df.pivot_table(index=y, columns=x, values=values, aggfunc="mean")
    
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale=colorscale,
            text=pivot_df.values if annotations else None,
            texttemplate="%{text:.2f}" if annotations else None,
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        **get_layout_config(),
    )
    return fig


def build_heatmap_annotated(
    df: pd.DataFrame,
    x: str,
    y: str,
    values: str,
    text: str = None,
    title: str = "Annotated Heatmap",
    colorscale: str = "RdBu",
    **kwargs
) -> go.Figure:
    """Build an annotated heatmap."""
    pivot_df = df.pivot_table(index=y, columns=x, values=values, aggfunc="mean")
    
    if text and text in df.columns:
        text_df = df.pivot_table(index=y, columns=x, values=text, aggfunc="first")
        text_values = text_df.values
    else:
        text_values = pivot_df.values
    
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale=colorscale,
            text=text_values,
            texttemplate="%{text:.2f}",
            textfont={"size": 10},
        )
    )
    
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        **get_layout_config(),
    )
    return fig


def build_radar(
    df: pd.DataFrame,
    categories: List[str] = None,
    values: List[str] = None,
    title: str = "Radar Chart",
    fill: bool = True,
    **kwargs
) -> go.Figure:
    """Build a radar (spider) chart."""
    if categories is None or values is None:
        raise ValueError("categories and values required for radar chart")
    
    # Use first row if values is a column name
    if isinstance(values, str) and values in df.columns:
        values = df[values].iloc[0]
    elif isinstance(values, list):
        values = [df[c].mean() for c in values]
    
    fig = go.Figure(
        data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself" if fill else None,
            name="Profile",
        )
    )
    
    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True, range=[0, max(values) * 1.1])),
        **get_layout_config(),
    )
    return fig


def build_treemap(
    df: pd.DataFrame,
    labels: str,
    values: str,
    parents: Optional[str] = None,
    color: Optional[str] = None,
    title: str = "Treemap",
    **kwargs
) -> go.Figure:
    """Build a treemap."""
    fig = px.treemap(
        df,
        labels=labels,
        values=values,
        parents=parents,
        color=color,
        title=title,
    )
    fig.update_layout(get_layout_config())
    return fig


def build_sunburst(
    df: pd.DataFrame,
    labels: str,
    values: str,
    parents: Optional[str] = None,
    color: Optional[str] = None,
    title: str = "Sunburst Chart",
    **kwargs
) -> go.Figure:
    """Build a sunburst chart."""
    fig = px.sunburst(
        df,
        labels=labels,
        values=values,
        parents=parents,
        color=color,
        title=title,
    )
    fig.update_layout(get_layout_config())
    return fig


def build_sankey(
    df: pd.DataFrame,
    source: str,
    target: str,
    value: str,
    title: str = "Sankey Diagram",
    color: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """Build a Sankey diagram."""
    fig = px.sankey(
        df,
        source=source,
        target=target,
        value=value,
        color=color,
        title=title,
    )
    fig.update_layout(get_layout_config())
    return fig


def build_flow_diagram(
    nodes: List[str],
    edges: List[tuple],
    title: str = "Flow Diagram",
    **kwargs
) -> go.Figure:
    """Build a simplified flow/pipeline diagram using Plotly."""
    # Create a network-style visualization
    import networkx as nx
    
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="#888"),
        hoverinfo="none",
        showlegend=False,
    )
    
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=nodes,
        textposition="top center",
        hoverinfo="text",
        marker=dict(size=20, color="#0072B2"),
        showlegend=False,
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig = go.Figure(data=[edge_trace, node_trace])
    layout_config = get_layout_config()
    # Remove keys that we're setting directly to avoid duplicates
    for key in ['plot_bgcolor', 'showlegend', 'hovermode', 'margin']:
        layout_config.pop(key, None)
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(240,240,240,0.5)",
        **layout_config,
    )
    return fig


def build_network_graph(
    edges: List[tuple],
    nodes: Optional[List[str]] = None,
    title: str = "Network Graph",
    layout: str = "spring",
    **kwargs
) -> go.Figure:
    """Build a network graph."""
    import networkx as nx
    
    G = nx.Graph()
    
    if nodes:
        G.add_nodes_from(nodes)
    
    G.add_edges_from(edges)
    
    if layout == "spring":
        pos = nx.spring_layout(G, k=2, iterations=50)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="#888"),
        hoverinfo="none",
        showlegend=False,
    )
    
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = list(G.nodes())
    node_size = [max(10, min(30, len(list(G.neighbors(node))) * 3)) for node in G.nodes()]
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hoverinfo="text",
        marker=dict(size=node_size, color="#0072B2"),
        showlegend=False,
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    layout_config = get_layout_config()
    # Remove keys that we're setting directly to avoid duplicates
    for key in ['plot_bgcolor', 'showlegend', 'hovermode', 'margin']:
        layout_config.pop(key, None)
    fig.update_layout(
        title=title,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(240,240,240,0.5)",
        **layout_config,
    )
    return fig


def build_runtime_breakdown(
    df: pd.DataFrame,
    stages: str,
    times: str,
    preset: Optional[str] = None,
    title: str = "Runtime Breakdown",
    **kwargs
) -> go.Figure:
    """Build a runtime breakdown visualization."""
    if preset:
        df_plot = df[df["preset"] == preset].copy()
    else:
        df_plot = df.copy()
    
    return build_stacked_bar(
        df_plot,
        x="preset" if preset else stages,
        y_columns=df_plot[stages].unique().tolist() if preset else [times],
        title=title,
        y_label="Time (ms)",
    )


def build_preset_comparison(
    df: pd.DataFrame,
    presets: str = None,
    metrics: List[str] = None,
    aggregation: str = "mean",
    title: str = "Preset Comparison",
    **kwargs
) -> go.Figure:
    """Build a preset comparison chart."""
    if metrics is None:
        metrics = df.select_dtypes(include=[np.number]).columns.tolist()[:3]
    
    fig = make_subplots(
        rows=1,
        cols=len(metrics),
        subplot_titles=metrics,
        specs=[[{"type": "bar"} for _ in metrics]],
    )
    
    for idx, metric in enumerate(metrics, 1):
        if presets:
            grouped = df.groupby(presets)[metric].agg(aggregation)
        else:
            grouped = df[metric].agg(aggregation)
        
        fig.add_trace(
            go.Bar(x=grouped.index, y=grouped.values, name=metric),
            row=1,
            col=idx,
        )
    
    fig.update_layout(title=title, **get_layout_config())
    return fig
