"""Registry of available chart types and builders."""

from typing import Dict, Callable, List, Any
import logging

logger = logging.getLogger(__name__)

# Will be populated by chart builder modules
CHART_BUILDERS: Dict[str, Callable] = {}

# Chart metadata
CHART_METADATA = {
    "bar": {
        "name": "Bar Chart",
        "description": "Compare values across categories",
        "requires": ["x", "y"],
        "optional": ["color", "sort"],
    },
    "grouped_bar": {
        "name": "Grouped Bar",
        "description": "Compare multiple series by category",
        "requires": ["x", "y_columns"],
        "optional": ["color", "sort"],
    },
    "stacked_bar": {
        "name": "Stacked Bar",
        "description": "Show composition and totals",
        "requires": ["x", "y_columns"],
        "optional": ["sort", "normalize"],
    },
    "stacked_bar_100": {
        "name": "100% Stacked Bar",
        "description": "Show percentage composition",
        "requires": ["x", "y_columns"],
        "optional": ["sort"],
    },
    "line": {
        "name": "Line Chart",
        "description": "Show trends over time or values",
        "requires": ["x", "y"],
        "optional": ["color", "markers"],
    },
    "area": {
        "name": "Area Chart",
        "description": "Show cumulative trends",
        "requires": ["x", "y"],
        "optional": ["color", "stacked"],
    },
    "scatter": {
        "name": "Scatter Plot",
        "description": "Show relationships between variables",
        "requires": ["x", "y"],
        "optional": ["size", "color", "hover_text"],
    },
    "bubble": {
        "name": "Bubble Chart",
        "description": "Multi-dimensional comparison",
        "requires": ["x", "y", "size"],
        "optional": ["color", "hover_text"],
    },
    "box": {
        "name": "Box Plot",
        "description": "Show distribution and outliers",
        "requires": ["x", "y"],
        "optional": ["color"],
    },
    "violin": {
        "name": "Violin Plot",
        "description": "Show probability density",
        "requires": ["x", "y"],
        "optional": ["color", "points"],
    },
    "histogram": {
        "name": "Histogram",
        "description": "Show frequency distribution",
        "requires": ["x"],
        "optional": ["nbins", "color"],
    },
    "heatmap": {
        "name": "Heatmap",
        "description": "Show matrix of values with color",
        "requires": ["x", "y", "values"],
        "optional": ["colorscale", "annotations"],
    },
    "heatmap_annotated": {
        "name": "Annotated Heatmap",
        "description": "Heatmap with cell text",
        "requires": ["x", "y", "values", "text"],
        "optional": ["colorscale"],
    },
    "radar": {
        "name": "Radar/Spider Chart",
        "description": "Multi-dimensional profile",
        "requires": ["categories", "values"],
        "optional": ["fill"],
    },
    "treemap": {
        "name": "Treemap",
        "description": "Show hierarchical composition",
        "requires": ["labels", "values"],
        "optional": ["parents", "color"],
    },
    "sunburst": {
        "name": "Sunburst Chart",
        "description": "Hierarchical pie chart",
        "requires": ["labels", "values"],
        "optional": ["parents", "color"],
    },
    "sankey": {
        "name": "Sankey Diagram",
        "description": "Show flow and relationships",
        "requires": ["source", "target", "value"],
        "optional": ["color"],
    },
    "flow_diagram": {
        "name": "Flow/Pipeline Diagram",
        "description": "Show process steps",
        "requires": ["nodes", "edges"],
        "optional": ["layout"],
    },
    "network_graph": {
        "name": "Network Graph",
        "description": "Show network connections",
        "requires": ["edges"],
        "optional": ["nodes", "layout"],
    },
    "runtime_breakdown": {
        "name": "Runtime Breakdown",
        "description": "Execution time distribution",
        "requires": ["stages", "times"],
        "optional": ["preset"],
    },
    "preset_comparison": {
        "name": "Preset Comparison",
        "description": "Compare multiple presets",
        "requires": ["presets", "metrics"],
        "optional": ["aggregation"],
    },
}


def register_builder(chart_type: str, builder_func: Callable):
    """Register a chart builder function."""
    CHART_BUILDERS[chart_type] = builder_func
    logger.info(f"Registered chart builder: {chart_type}")


def get_builder(chart_type: str) -> Callable:
    """Get a chart builder function."""
    if chart_type not in CHART_BUILDERS:
        raise ValueError(f"Unknown chart type: {chart_type}")
    return CHART_BUILDERS[chart_type]


def get_available_charts() -> List[str]:
    """Get list of available chart types."""
    return sorted(CHART_BUILDERS.keys())


def get_chart_metadata(chart_type: str) -> Dict[str, Any]:
    """Get metadata for a chart type."""
    return CHART_METADATA.get(chart_type, {})


def build_chart(chart_type: str, **kwargs):
    """Build a chart of specified type."""
    builder = get_builder(chart_type)
    return builder(**kwargs)
