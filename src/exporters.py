"""Export functions for charts and data."""

import logging
from pathlib import Path
from typing import List, Dict, Any
import json
import pandas as pd

logger = logging.getLogger(__name__)


def ensure_output_structure():
    """Ensure output directory structure exists."""
    dirs = [
        "output/png",
        "output/svg",
        "output/pdf",
        "output/html",
        "output/configs",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def export_plotly_chart(fig, output_path: str, formats: List[str]) -> Dict[str, str]:
    """
    Export Plotly figure to multiple formats.
    
    Returns dict of {format: filepath}
    """
    ensure_output_structure()
    results = {}
    
    for fmt in formats:
        try:
            if fmt.lower() == "html":
                filepath = output_path.replace(".{}", ".html")
                fig.write_html(filepath)
                results[fmt] = filepath
                logger.info(f"Exported HTML: {filepath}")
                
            elif fmt.lower() == "png":
                filepath = output_path.replace(".{}", ".png")
                fig.write_image(filepath, width=1200, height=800, scale=3)
                results[fmt] = filepath
                logger.info(f"Exported PNG: {filepath}")
                
            elif fmt.lower() == "svg":
                filepath = output_path.replace(".{}", ".svg")
                fig.write_image(filepath, format="svg", width=1200, height=800)
                results[fmt] = filepath
                logger.info(f"Exported SVG: {filepath}")
                
            elif fmt.lower() == "pdf":
                filepath = output_path.replace(".{}", ".pdf")
                fig.write_image(filepath, format="pdf", width=1200, height=800)
                results[fmt] = filepath
                logger.info(f"Exported PDF: {filepath}")
                
        except Exception as e:
            logger.error(f"Failed to export {fmt}: {e}")
    
    return results


def save_chart_config(config: Dict[str, Any], name: str) -> str:
    """Save chart configuration as JSON."""
    ensure_output_structure()
    filepath = f"output/configs/{name}.json"
    with open(filepath, "w") as f:
        json.dump(config, f, indent=2)
    logger.info(f"Saved configuration: {filepath}")
    return filepath


def export_data_table(df: pd.DataFrame, name: str, formats: List[str] = None) -> Dict[str, str]:
    """Export data table to various formats."""
    if formats is None:
        formats = ["csv", "xlsx"]
    
    ensure_output_structure()
    results = {}
    
    for fmt in formats:
        try:
            if fmt.lower() == "csv":
                filepath = f"output/{fmt}/{name}.csv"
                Path(filepath).parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(filepath, index=False)
                results[fmt] = filepath
                logger.info(f"Exported CSV: {filepath}")
                
            elif fmt.lower() == "xlsx":
                filepath = f"output/{fmt}/{name}.xlsx"
                Path(filepath).parent.mkdir(parents=True, exist_ok=True)
                df.to_excel(filepath, index=False)
                results[fmt] = filepath
                logger.info(f"Exported XLSX: {filepath}")
                
        except Exception as e:
            logger.error(f"Failed to export {fmt}: {e}")
    
    return results
