"""Chart metadata and icons."""

CHART_ICONS = {
    # Comparison
    "bar": {"icon": "📊", "name": "Bar Chart", "description": "Simple category comparison"},
    "grouped_bar": {"icon": "📊📊", "name": "Grouped Bar", "description": "Multiple categories side-by-side"},
    "stacked_bar": {"icon": "📚", "name": "Stacked Bar", "description": "Cumulative categories"},
    "stacked_bar_100": {"icon": "📈", "name": "100% Stacked", "description": "Normalized percentages"},
    
    # Trends
    "line": {"icon": "📈", "name": "Line Chart", "description": "Trends over time"},
    "area": {"icon": "📉", "name": "Area Chart", "description": "Filled trend visualization"},
    
    # Relationship
    "scatter": {"icon": "•••", "name": "Scatter Plot", "description": "Two-variable relationship"},
    "bubble": {"icon": "◯◯◯", "name": "Bubble Chart", "description": "Three-variable relationship"},
    "heatmap": {"icon": "🔥", "name": "Heatmap", "description": "2D color-coded matrix"},
    
    # Distribution
    "box": {"icon": "📦", "name": "Box Plot", "description": "Distribution quartiles"},
    "violin": {"icon": "🎻", "name": "Violin Plot", "description": "Distribution density"},
    "histogram": {"icon": "📊", "name": "Histogram", "description": "Frequency distribution"},
    
    # Hierarchy
    "treemap": {"icon": "🗂️", "name": "Treemap", "description": "Hierarchical rectangles"},
    "sunburst": {"icon": "☀️", "name": "Sunburst", "description": "Radial hierarchy"},
    
    # Flow
    "sankey": {"icon": "🔀", "name": "Sankey", "description": "Flow diagram"},
    "flow_diagram": {"icon": "⏱️", "name": "Flow Pipeline", "description": "Process steps"},
    
    # Network
    "network_graph": {"icon": "🕸️", "name": "Network Graph", "description": "Nodes and connections"},
    "radar": {"icon": "⭐", "name": "Radar Chart", "description": "Multi-dimensional profile"},
    
    # Advanced
    "heatmap_annotated": {"icon": "🔥📝", "name": "Annotated Heatmap", "description": "Heatmap with values"},
    "preset_comparison": {"icon": "⚔️", "name": "Preset Compare", "description": "Design alternatives"},
    "runtime_breakdown": {"icon": "⏱️", "name": "Runtime Stack", "description": "Execution stages"},
}

CHART_CATEGORIES = {
    "Comparison": ["bar", "grouped_bar", "stacked_bar", "stacked_bar_100"],
    "Trends": ["line", "area"],
    "Relationship": ["scatter", "bubble", "heatmap"],
    "Distribution": ["box", "violin", "histogram"],
    "Hierarchy": ["treemap", "sunburst"],
    "Flow": ["sankey", "flow_diagram"],
    "Network": ["network_graph", "radar"],
    "Advanced": ["heatmap_annotated", "preset_comparison", "runtime_breakdown"],
}


def get_chart_icon_and_name(chart_type: str) -> tuple:
    """Get icon and display name for a chart type."""
    meta = CHART_ICONS.get(chart_type, {})
    return meta.get("icon", "📊"), meta.get("name", chart_type)


def get_chart_description(chart_type: str) -> str:
    """Get description for a chart type."""
    return CHART_ICONS.get(chart_type, {}).get("description", "")


def format_chart_option(chart_type: str) -> str:
    """Format chart option with icon and name for dropdown."""
    icon, name = get_chart_icon_and_name(chart_type)
    return f"{icon} {name}"
