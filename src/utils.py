"""Utility functions for the thesis visualization app."""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def ensure_output_dirs():
    """Ensure all output directories exist."""
    dirs = [
        "output/png",
        "output/svg",
        "output/pdf",
        "output/html",
        "output/configs",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def detect_column_type(series: pd.Series) -> str:
    """Detect if a column is numeric or categorical."""
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    else:
        return "categorical"


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Get list of numeric columns."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Get list of categorical columns."""
    return df.select_dtypes(include=["object"]).columns.tolist()


def normalize_data(series: pd.Series, method: str = "minmax") -> pd.Series:
    """Normalize a series using specified method."""
    if method == "minmax":
        return (series - series.min()) / (series.max() - series.min())
    elif method == "zscore":
        return (series - series.mean()) / series.std()
    elif method == "log":
        return np.log1p(series)
    else:
        return series


def suggest_chart_type(df: pd.DataFrame, x_col: str, y_col: str) -> List[str]:
    """Suggest recommended chart types based on data characteristics."""
    suggestions = []
    
    x_type = detect_column_type(df[x_col])
    y_type = detect_column_type(df[y_col])
    
    if x_type == "categorical" and y_type == "numeric":
        suggestions.extend(["bar", "grouped_bar", "box", "violin"])
    elif x_type == "numeric" and y_type == "numeric":
        suggestions.extend(["scatter", "bubble", "heatmap", "line"])
    elif x_type == "datetime" and y_type == "numeric":
        suggestions.extend(["line", "area", "scatter"])
    
    return suggestions


def save_config(config: Dict[str, Any], filepath: str):
    """Save chart configuration as JSON."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(config, f, indent=2)
    logger.info(f"Config saved to {filepath}")


def load_config(filepath: str) -> Dict[str, Any]:
    """Load chart configuration from JSON."""
    with open(filepath, "r") as f:
        return json.load(f)


def export_to_format(fig, filepath: str, format_type: str = "png", dpi: int = 300):
    """Export Plotly figure to specified format."""
    try:
        if format_type == "html":
            fig.write_html(filepath)
        elif format_type == "png":
            fig.write_image(filepath, width=1200, height=800, scale=dpi/100)
        elif format_type == "svg":
            fig.write_image(filepath, format="svg", width=1200, height=800)
        elif format_type == "pdf":
            fig.write_image(filepath, format="pdf", width=1200, height=800)
        logger.info(f"Exported to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return False


def create_output_filename(base_name: str, extension: str) -> str:
    """Create unique output filename with timestamp."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"output/{extension.lstrip('.')}s/{base_name}_{timestamp}.{extension.lstrip('.')}"


def load_sample_data(filename: str) -> Optional[pd.DataFrame]:
    """Load sample data from samples folder."""
    path = Path("samples") / filename
    if path.exists():
        return pd.read_csv(path)
    return None


def get_column_stats(series: pd.Series) -> Dict[str, Any]:
    """Get summary statistics for a column."""
    if pd.api.types.is_numeric_dtype(series):
        return {
            "type": "numeric",
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "q25": float(series.quantile(0.25)),
            "q75": float(series.quantile(0.75)),
        }
    else:
        return {
            "type": "categorical",
            "unique_values": int(series.nunique()),
            "top_values": series.value_counts().head(10).to_dict(),
        }


def clean_sheet_data(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Clean messy Excel sheet data.
    Handles merged cells, header rows, NaN values, etc.
    """
    if df.empty:
        return None
    
    # Drop completely empty rows/columns
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')
    
    if df.empty:
        return None
    
    # If first column looks like a header (contains mostly strings), try to use it
    first_col_name = df.columns[0]
    first_col_vals = df[first_col_name].astype(str).str.strip()
    
    # Find the actual header row (looking for row with keywords like "Stage", "Type", "Run")
    header_keywords = ['stage', 'type', 'run', 'seed', 'fi', 'cs', 'uf', 'oi', 'odp', 'runtime', 'hard', 'preset']
    
    header_row_idx = None
    for idx, row in df.iterrows():
        row_str = ' '.join(map(str, row.values)).lower()
        if sum(keyword in row_str for keyword in header_keywords) >= 3:
            header_row_idx = idx
            break
    
    # Use found header or keep existing
    if header_row_idx is not None and header_row_idx > 0:
        df = df.iloc[header_row_idx:].reset_index(drop=True)
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
    
    # Clean column names
    df.columns = df.columns.astype(str).str.strip().str.lower()
    df.columns = df.columns.str.replace(r'\s+', '_', regex=True)
    
    # Convert numeric columns
    numeric_cols = []
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].notna().sum() > 0:  # If at least one valid numeric value
                numeric_cols.append(col)
        except:
            pass
    
    # Drop rows where all numeric columns are NaN
    if numeric_cols:
        df = df.dropna(subset=numeric_cols, how='all')
    
    # Drop rows that are all NaN
    df = df.dropna(how='all')
    
    return df if not df.empty else None


def get_suggested_charts(df: pd.DataFrame) -> List[str]:
    """
    Suggest chart types based on available data.
    """
    if df.empty:
        return []
    
    numeric_cols = get_numeric_columns(df)
    cat_cols = get_categorical_columns(df)
    
    suggestions = []
    
    # Multi-metric analysis
    if len(numeric_cols) >= 2:
        suggestions.append("box")  # For outlier detection across metrics
        suggestions.append("violin")  # Distribution of metrics
        suggestions.append("scatter_matrix")  # Relationships between metrics
    
    # Time-series like data (if has a stage or run column)
    if any(col in [c.lower() for c in df.columns] for col in ['stage', 'run', 'seed']):
        suggestions.append("line")
        suggestions.append("bar")
    
    # Comparison data (categorical + numeric)
    if len(cat_cols) > 0 and len(numeric_cols) > 0:
        suggestions.append("bar")
        suggestions.append("grouped_bar")
        suggestions.append("box")  # For comparison across groups
    
    # Correlation analysis
    if len(numeric_cols) >= 3:
        suggestions.append("heatmap")  # Correlation heatmap
        suggestions.append("scatter")
    
    # Always include these for thesis-quality outputs
    if len(numeric_cols) >= 1:
        suggestions.append("histogram")
        suggestions.append("radar")  # Nice for thesis figures
    
    return list(dict.fromkeys(suggestions))  # Remove duplicates, preserve order


def prepare_multi_sheet_data(excel_path: str, sheet_names: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Load and clean data from multiple sheets in an Excel file.
    Returns a dictionary: {sheet_name: cleaned_dataframe}
    """
    result = {}
    
    try:
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                cleaned = clean_sheet_data(df)
                if cleaned is not None and not cleaned.empty:
                    result[sheet_name] = cleaned
            except Exception as e:
                logger.warning(f"Could not clean sheet '{sheet_name}': {e}")
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
    
    return result
