"""Data loading from various file formats."""

import pandas as pd
import logging
from typing import List, Optional, Tuple, Union, BinaryIO
from pathlib import Path
import io

logger = logging.getLogger(__name__)


def _get_file_path_or_bytes(file_input: Union[str, BinaryIO]) -> Union[str, BinaryIO]:
    """Handle both file paths and file-like objects."""
    if isinstance(file_input, str):
        return file_input
    # Streamlit UploadedFile has a .name attribute
    if hasattr(file_input, 'read'):
        return file_input
    return str(file_input)


def load_csv(filepath: Union[str, BinaryIO]) -> pd.DataFrame:
    """Load CSV file from path or file object."""
    try:
        filepath = _get_file_path_or_bytes(filepath)
        df = pd.read_csv(filepath)
        name = getattr(filepath, 'name', str(filepath))
        logger.info(f"Loaded CSV: {name} ({len(df)} rows)")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise


def load_excel(filepath: Union[str, BinaryIO], sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Load Excel file (XLSX, XLSM, XLS) from path or file object.
    
    If sheet_name is None, loads the first sheet.
    """
    try:
        filepath = _get_file_path_or_bytes(filepath)
        # Note: If sheet_name=None and there are multiple sheets, 
        # pandas returns a dict. We explicitly load sheet 0 (first sheet) to avoid this.
        if sheet_name is None:
            # For multi-sheet files, load the first sheet
            df = pd.read_excel(filepath, sheet_name=0)
        else:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        name = getattr(filepath, 'name', str(filepath))
        logger.info(f"Loaded Excel: {name} ({len(df)} rows)")
        return df
    except Exception as e:
        logger.error(f"Error loading Excel: {e}")
        raise


def load_xlsb(filepath: Union[str, BinaryIO], sheet_name: Optional[str] = None) -> pd.DataFrame:
    """Load binary Excel file (XLSB) from path or file object."""
    try:
        from pyxlsb import open_workbook
        # If it's a file object, read it to bytes first
        if hasattr(filepath, 'read'):
            file_bytes = filepath.read()
            filepath = io.BytesIO(file_bytes)
        with open_workbook(filepath) as wb:
            ws = wb.sheets[sheet_name or 0]
            data = []
            for row in ws.rows:
                data.append([c.v for c in row])
            df = pd.DataFrame(data[1:], columns=data[0])
        name = getattr(filepath, 'name', 'XLSB file')
        logger.info(f"Loaded XLSB: {name} ({len(df)} rows)")
        return df
    except Exception as e:
        logger.error(f"Error loading XLSB: {e}")
        raise


def load_ods(filepath: Union[str, BinaryIO], sheet_name: Optional[int] = None) -> pd.DataFrame:
    """Load ODS (OpenDocument Spreadsheet) from path or file object.
    
    If sheet_name is None, loads the first sheet.
    """
    try:
        filepath = _get_file_path_or_bytes(filepath)
        # For ODS files, default to first sheet if not specified
        if sheet_name is None:
            sheet_name = 0
        df = pd.read_excel(filepath, sheet_name=sheet_name, engine="odf")
        name = getattr(filepath, 'name', str(filepath))
        logger.info(f"Loaded ODS: {name} ({len(df)} rows)")
        return df
    except Exception as e:
        logger.error(f"Error loading ODS: {e}")
        raise


def get_sheet_names(filepath: Union[str, BinaryIO]) -> List[str]:
    """Get list of sheet names from Excel or ODS file."""
    try:
        # Get filename to determine type
        if hasattr(filepath, 'name'):
            filename = filepath.name.lower()
        else:
            filename = str(filepath).lower()
        
        if filename.endswith(".xlsb"):
            from pyxlsb import open_workbook
            # For XLSB, need to reset if file object was already read
            if hasattr(filepath, 'seek'):
                filepath.seek(0)
            with open_workbook(filepath) as wb:
                return [ws.name for ws in wb.sheets]
        elif filename.endswith((".ods", ".odt")):
            if hasattr(filepath, 'seek'):
                filepath.seek(0)
            xls = pd.ExcelFile(filepath, engine="odf")
            return xls.sheet_names
        else:
            if hasattr(filepath, 'seek'):
                filepath.seek(0)
            xls = pd.ExcelFile(filepath)
            return xls.sheet_names
    except Exception as e:
        logger.warning(f"Error getting sheet names: {e}")
        return []


def load_data(filepath: Union[str, BinaryIO], sheet_name: Optional[str] = None) -> Tuple[pd.DataFrame, List[str]]:
    """
    Intelligently load data from various formats.
    
    Accepts:
    - File paths (str)
    - Streamlit UploadedFile objects
    - File-like objects (with .read() and .name attributes)
    
    Returns:
        Tuple of (DataFrame, list of sheet names)
    """
    # Get filename to determine type
    if hasattr(filepath, 'name'):
        filename = filepath.name.lower()
    else:
        filename = str(filepath).lower()
    
    # Reset file pointer if it's a file object
    if hasattr(filepath, 'seek'):
        try:
            filepath.seek(0)
        except:
            pass
    
    try:
        if filename.endswith(".csv"):
            df = load_csv(filepath)
            return df, []
        elif filename.endswith(".xlsb"):
            if hasattr(filepath, 'seek'):
                filepath.seek(0)
            df = load_xlsb(filepath, sheet_name)
            sheets = get_sheet_names(filepath)
            return df, sheets
        elif filename.endswith((".ods", ".odt")):
            if hasattr(filepath, 'seek'):
                filepath.seek(0)
            df = load_ods(filepath, sheet_name)
            sheets = get_sheet_names(filepath)
            return df, sheets
        elif filename.endswith((".xlsx", ".xlsm", ".xls")):
            if hasattr(filepath, 'seek'):
                filepath.seek(0)
            df = load_excel(filepath, sheet_name)
            sheets = get_sheet_names(filepath)
            return df, sheets
        else:
            # Try to detect by content if extension unknown
            logger.warning(f"Unknown extension for {filename}, attempting CSV load")
            df = load_csv(filepath)
            return df, []
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise ValueError(f"Could not load file: {e}") from e
