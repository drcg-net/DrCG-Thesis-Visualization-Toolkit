"""
DrCG Thesis Visualization Toolkit (Thesis Chart Generator)

A lightweight tool for PhD thesis chart generation.
Upload tables (CSV/Excel/ODS), generate publication-ready charts, and export figures.
"""

import streamlit as st
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import json
from typing import Optional, List
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import loaders, exporters, utils, chart_registry, bibliometric, graph_diagrams, chart_metadata
from src.chart_builders import plotly_charts

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure output directories
utils.ensure_output_dirs()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="DrCG Thesis Visualization Toolkit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        /* Hide deploy button in header */
        button[data-testid="stToolbarButton"] { display: none !important; }
        [data-testid="stToolbarButton"] { display: none !important; }
        .st-emotion-cache-z5fcl4 { display: none !important; }
        
        /* Hide all action buttons in toolbar */
        [data-testid="stAppToolbar"] button:first-child { display: none !important; }
        
        /* Styling */
        .thesis-header { font-size: 24px; font-weight: bold; margin-bottom: 20px; }
        .chart-container { border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.markdown("""
<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
    <span style='font-size: 40px;'>📊</span>
    <div>
        <h2 style='margin: 0; font-size: 20px;'>Thesis Viz Toolkit</h2>
        <small style='color: #888;'>Publication-Ready Charts</small>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "📋 Select Tool",
    [
        "🏠 Home",
        "📥 Data Uploader",
        "🎨 Chart Builder",
        "🚀 Quick Analysis",
        "📊 Multi-Sheet Analysis",
        "📚 Bibliometric Analysis",
        "🔗 Graph & Diagrams",
        "🔄 Batch Generator",
        "✨ Examples & Presets",
    ],
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "sheet_names" not in st.session_state:
    st.session_state.sheet_names = []

if "uploaded_file_buffer" not in st.session_state:
    st.session_state.uploaded_file_buffer = None

if "chart_config" not in st.session_state:
    st.session_state.chart_config = {}

if "generate_all_category" not in st.session_state:
    st.session_state.generate_all_category = None

# ============================================================================
# HOME PAGE
# ============================================================================

if page == "Home" or page == "🏠 Home":
    st.markdown("<h1 style='color: #1f77b4;'>📊 DrCG Thesis Visualization Toolkit</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### A Thesis Chart Generator for Researchers
    
    This app helps you quickly turn tabular data (CSV/Excel/ODS) into publication-ready charts.
    It is designed for PhD thesis research, academic reports, and scientific visualization.
    
    **Key Capabilities:**
    - 📥 Flexible data import (CSV, Excel, ODS, multi-sheet)
    - 📈 20+ chart types (bar, line, scatter, box, violin, radar, heatmap, and more)
    - 🎛️ Auto chart suggestions and quick analysis
    - 📦 Export to PNG, SVG, PDF, and interactive HTML
    - 🔁 Save/load chart configs and batch-generate multiple figures
    
    **Quick Start:**
    1. Go to **Data Uploader** and import your data
    2. Use **Chart Builder** to pick a chart and configure axes
    3. Export your figure (PNG/SVG/PDF/HTML)
    4. Use **Batch Generator** to create multiple charts automatically
    
    **Need inspiration?** Use **Examples & Presets** to see ready-made charts.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Supported formats", "CSV / Excel / ODS")
    with col2:
        st.metric("Chart types", "20+")
    with col3:
        st.metric("Export formats", "PNG / SVG / PDF / HTML")
    
    st.markdown("---")
    st.markdown("**Developed by:** DrCG.Net / Mohammad Amanzadegan")


# ============================================================================
# DATA UPLOADER
# ============================================================================

elif page == "Data Uploader" or page == "📥 Data Uploader":
    st.header("📥 Data Uploader")
    
    # Upload section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload data file (CSV, Excel, ODS, etc.)",
            type=["csv", "xlsx", "xlsm", "xls", "xlsb", "ods", "odt"],
        )
    
    with col2:
        use_sample = st.checkbox("Use Sample Data")
    
    if use_sample:
        sample_files = list(Path("samples").glob("*.csv"))
        if sample_files:
            sample_file = st.selectbox("Select sample", sample_files)
            try:
                st.session_state.df = pd.read_csv(sample_file)
                st.session_state.sheet_names = []
                st.success(f"Loaded sample: {sample_file.name}")
            except Exception as e:
                st.error(f"Error loading sample: {e}")
    
    elif uploaded_file:
        try:
            # Cache file content to BytesIO to allow multiple reads
            # (Streamlit UploadedFile cannot be re-read reliably after first read)
            import io
            file_bytes = uploaded_file.read()
            file_buffer = io.BytesIO(file_bytes)
            file_buffer.name = uploaded_file.name
            
            st.session_state.uploaded_file_buffer = file_buffer
            st.session_state.df, st.session_state.sheet_names = loaders.load_data(file_buffer)
            st.success(f"✅ Loaded {len(st.session_state.df)} rows")
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            logger.exception("File loading error")
    
    # Sheet selection for multi-sheet files
    if st.session_state.sheet_names and st.session_state.get('uploaded_file_buffer'):
        st.subheader("Sheet Selection")
        selected_sheet = st.selectbox("Select sheet", st.session_state.sheet_names)
        if st.button("Load Sheet"):
            try:
                # Reset file pointer before reading again
                file_buffer = st.session_state.uploaded_file_buffer
                file_buffer.seek(0)
                st.session_state.df, _ = loaders.load_data(file_buffer, selected_sheet)
                st.success(f"✅ Loaded sheet: {selected_sheet}")
            except Exception as e:
                st.error(f"Error loading sheet: {e}")
    
    # Data preview
    if st.session_state.df is not None:
        st.subheader("Data Preview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(st.session_state.df))
        with col2:
            st.metric("Columns", len(st.session_state.df.columns))
        with col3:
            numeric_cols = len(utils.get_numeric_columns(st.session_state.df))
            st.metric("Numeric Columns", numeric_cols)
        
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
        
        # Column statistics
        st.subheader("Column Statistics")
        
        col_to_analyze = st.selectbox("Analyze column:", st.session_state.df.columns)
        
        if col_to_analyze:
            stats = utils.get_column_stats(st.session_state.df[col_to_analyze])
            
            if stats["type"] == "numeric":
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Mean", f"{stats['mean']:.2f}")
                with col2:
                    st.metric("Median", f"{stats['median']:.2f}")
                with col3:
                    st.metric("Std Dev", f"{stats['std']:.2f}")
                with col4:
                    st.metric("Min", f"{stats['min']:.2f}")
                with col5:
                    st.metric("Max", f"{stats['max']:.2f}")
            else:
                st.write(f"**Unique Values:** {stats['unique_values']}")
                st.write("**Top Values:**")
                for val, count in stats['top_values'].items():
                    st.write(f"- {val}: {count}")


# ============================================================================
# CHART BUILDER
# ============================================================================

elif page == "Chart Builder" or page == "🎨 Chart Builder":
    st.header("📈 Chart Builder")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
    else:
        # Chart configuration panel
        st.subheader("1. Choose Chart Type")
        
        # Category selection
        category = st.radio("📁 Category", list(chart_metadata.CHART_CATEGORIES.keys()), horizontal=True)
        charts_in_category = chart_metadata.CHART_CATEGORIES[category]
        
        # Show all charts in category with icons
        st.write("**Available charts in this category:**")
        cols = st.columns(min(4, len(charts_in_category)))
        for idx, chart in enumerate(charts_in_category):
            icon, name = chart_metadata.get_chart_icon_and_name(chart)
            desc = chart_metadata.get_chart_description(chart)
            with cols[idx % len(cols)]:
                st.markdown(f"""
                <div style='text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>
                <div style='font-size: 24px;'>{icon}</div>
                <b>{name}</b>
                <br><small>{desc}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # Single chart selection
        chart_options = [f"{chart_metadata.get_chart_icon_and_name(c)[0]} {chart_metadata.get_chart_icon_and_name(c)[1]}" for c in charts_in_category]
        selected_option = st.selectbox("or Select One Chart", chart_options)
        chart_type = charts_in_category[chart_options.index(selected_option)]
        
        # Get recommendations
        numeric_cols = utils.get_numeric_columns(st.session_state.df)
        cat_cols = utils.get_categorical_columns(st.session_state.df)
        all_cols = st.session_state.df.columns.tolist()
        
        st.info(f"📊 Auto-detected: {len(numeric_cols)} numeric, {len(cat_cols)} categorical columns")
        
        # Configuration based on chart type
        st.subheader("2. Configure Data Mapping")
        
        config = {"chart_type": chart_type}
        
        try:
            if chart_type in ["bar", "grouped_bar", "stacked_bar", "stacked_bar_100"]:
                config["x"] = st.selectbox("X-axis (Category)", cat_cols + numeric_cols)
                
                if chart_type == "bar":
                    config["y"] = st.selectbox("Y-axis (Values)", numeric_cols)
                else:
                    config["y_columns"] = st.multiselect("Y-axis (Values)", numeric_cols)
                
                config["sort_by"] = st.selectbox("Sort by", [None] + numeric_cols)
            
            elif chart_type in ["line", "area", "scatter", "bubble"]:
                config["x"] = st.selectbox("X-axis", all_cols)
                config["y"] = st.selectbox("Y-axis", numeric_cols)
                
                if chart_type == "bubble":
                    config["size"] = st.selectbox("Bubble Size", numeric_cols)
                
                if chart_type in ["scatter", "bubble"]:
                    config["color"] = st.selectbox("Color by (optional)", [None] + all_cols)
            
            elif chart_type in ["box", "violin"]:
                config["x"] = st.selectbox("X-axis (Category)", cat_cols)
                config["y"] = st.selectbox("Y-axis (Values)", numeric_cols)
                config["color"] = st.selectbox("Color by", [None] + cat_cols)
            
            elif chart_type == "histogram":
                config["x"] = st.selectbox("Variable", numeric_cols)
                config["nbins"] = st.slider("Number of Bins", 5, 50, 20)
            
            elif chart_type in ["heatmap", "heatmap_annotated"]:
                config["x"] = st.selectbox("X-axis", cat_cols + numeric_cols)
                config["y"] = st.selectbox("Y-axis", cat_cols + numeric_cols)
                config["values"] = st.selectbox("Values", numeric_cols)
                config["colorscale"] = st.selectbox(
                    "Color Scale",
                    ["RdBu", "Viridis", "Blues", "Reds", "Greens", "Greys"],
                )
            
            elif chart_type == "radar":
                config["categories"] = st.multiselect("Categories", all_cols)
                config["values"] = st.selectbox("Values", numeric_cols)
            
            elif chart_type in ["treemap", "sunburst"]:
                config["labels"] = st.selectbox("Labels", all_cols)
                config["values"] = st.selectbox("Values", numeric_cols)
                if st.checkbox("Has hierarchy"):
                    config["parents"] = st.selectbox("Parents", [None] + all_cols)
            
            elif chart_type == "sankey":
                config["source"] = st.selectbox("Source", all_cols)
                config["target"] = st.selectbox("Target", all_cols)
                config["value"] = st.selectbox("Value", numeric_cols)
            
            elif chart_type in ["flow_diagram", "network_graph"]:
                config["source"] = st.selectbox("From/Source Column", all_cols)
                config["target"] = st.selectbox("To/Target Column", all_cols)
            
            # Common parameters
            st.divider()
            st.subheader("3. Styling & Export")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                config["title"] = st.text_input("Title", "My Chart", key="title_input")
            with col2:
                config["x_label"] = st.text_input("X Label", "", key="x_label_input")
            with col3:
                config["y_label"] = st.text_input("Y Label", "", key="y_label_input")
            
            # Advanced options in expander
            with st.expander("⚙️ Advanced Options"):
                publication_mode = st.checkbox("📖 Publication Mode (Thesis)", value=True)
                dpi = st.select_slider("Resolution (DPI)", [100, 150, 200, 300], value=300 if publication_mode else 100)
                export_formats = st.multiselect("Export Formats", ["HTML", "PNG", "SVG", "PDF"], default=["PNG"])
                
                st.divider()
                st.subheader("🔄 Generate All Charts")
                generate_all = st.checkbox("Generate all charts in this category automatically", value=False)
                if generate_all:
                    st.info(f"📊 Will generate {len(charts_in_category)} charts from '{category}' category")
            
            # Set defaults if not in advanced
            if "dpi" not in config:
                dpi = 300
                export_formats = ["png"]
            
            # Generate buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("🎨 Generate Chart", use_container_width=True):
                    st.session_state.chart_config = config
                    st.session_state.chart_config["dpi"] = dpi
                    st.session_state.chart_config["export_formats"] = [f.lower() for f in export_formats]
                    st.rerun()
            
            with col2:
                if st.button("💾 Save Config", use_container_width=True):
                    config_name = st.text_input("Config name", "my_chart_config")
                    if config_name:
                        filepath = exporters.save_chart_config(st.session_state.chart_config, config_name)
                        st.success(f"✅ Saved: {filepath}")
            
            with col3:
                if generate_all and st.button("🎨 Generate All", use_container_width=True):
                    st.session_state.generate_all_category = category
                    st.session_state.chart_config["dpi"] = dpi
                    st.session_state.chart_config["export_formats"] = [f.lower() for f in export_formats]
                    st.rerun()
        
        except Exception as e:
            st.error(f"Configuration error: {e}")
            logger.exception("Configuration error")
        
        # Handle generate all category
        if st.session_state.generate_all_category:
            try:
                st.divider()
                st.subheader(f"🎨 Generating All Charts - {st.session_state.generate_all_category}")
                
                category_charts = chart_metadata.CHART_CATEGORIES[st.session_state.generate_all_category]
                dpi = st.session_state.chart_config.get("dpi", 300)
                export_formats = st.session_state.chart_config.get("export_formats", ["png"])
                
                builder_map = {
                    "bar": plotly_charts.build_bar,
                    "grouped_bar": plotly_charts.build_grouped_bar,
                    "stacked_bar": plotly_charts.build_stacked_bar,
                    "stacked_bar_100": plotly_charts.build_stacked_bar_100,
                    "line": plotly_charts.build_line,
                    "area": plotly_charts.build_area,
                    "scatter": plotly_charts.build_scatter,
                    "bubble": plotly_charts.build_bubble,
                    "box": plotly_charts.build_box,
                    "violin": plotly_charts.build_violin,
                    "histogram": plotly_charts.build_histogram,
                    "heatmap": plotly_charts.build_heatmap,
                    "radar": plotly_charts.build_radar,
                    "treemap": plotly_charts.build_treemap,
                    "sunburst": plotly_charts.build_sunburst,
                    "sankey": plotly_charts.build_sankey,
                }
                
                generated_count = 0
                for chart_type in category_charts:
                    if chart_type not in ["flow_diagram", "network_graph", "heatmap_annotated", "runtime_breakdown", "preset_comparison"]:
                        if chart_type in builder_map:
                            try:
                                icon, name = chart_metadata.get_chart_icon_and_name(chart_type)
                                st.subheader(f"{icon} {name}")
                                
                                # Auto-detect best column mapping
                                numeric_cols = utils.get_numeric_columns(st.session_state.df)
                                cat_cols = utils.get_categorical_columns(st.session_state.df)
                                
                                if chart_type in ["bar"]:
                                    if cat_cols and numeric_cols:
                                        fig = builder_map[chart_type](
                                            st.session_state.df,
                                            x=cat_cols[0],
                                            y=numeric_cols[0],
                                            title=f"{name} - {cat_cols[0]} vs {numeric_cols[0]}"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                        generated_count += 1
                                
                                elif chart_type in ["line", "scatter"]:
                                    if len(numeric_cols) >= 2:
                                        fig = builder_map[chart_type](
                                            st.session_state.df,
                                            x=numeric_cols[0],
                                            y=numeric_cols[1],
                                            title=f"{name} - {numeric_cols[0]} vs {numeric_cols[1]}"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                        generated_count += 1
                                
                                elif chart_type in ["box", "violin"]:
                                    if cat_cols and numeric_cols:
                                        fig = builder_map[chart_type](
                                            st.session_state.df,
                                            x=cat_cols[0],
                                            y=numeric_cols[0],
                                            title=f"{name} - {numeric_cols[0]} by {cat_cols[0]}"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                        generated_count += 1
                                
                                elif chart_type in ["grouped_bar", "stacked_bar"]:
                                    if cat_cols and len(numeric_cols) >= 2:
                                        fig = builder_map[chart_type](
                                            st.session_state.df,
                                            x=cat_cols[0],
                                            y_columns=numeric_cols[:2],
                                            title=f"{name} - Multiple Metrics"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                        generated_count += 1
                                
                                elif chart_type == "histogram":
                                    if numeric_cols:
                                        fig = builder_map[chart_type](
                                            st.session_state.df,
                                            x=numeric_cols[0],
                                            nbins=20,
                                            title=f"{name} - {numeric_cols[0]} Distribution"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                                        generated_count += 1
                                
                            except Exception as e:
                                st.warning(f"Could not generate {chart_type}: {str(e)[:100]}")
                
                st.success(f"✅ Generated {generated_count} charts from {st.session_state.generate_all_category} category")
                
                if st.button("🔁 Clear Results"):
                    st.session_state.generate_all_category = None
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error generating all charts: {e}")
                logger.exception("Generate all error")
        
        # Chart generation and display
        elif st.session_state.chart_config:
            try:
                chart_type = st.session_state.chart_config.get("chart_type")
                
                # Get builder function
                builder_map = {
                    "bar": plotly_charts.build_bar,
                    "grouped_bar": plotly_charts.build_grouped_bar,
                    "stacked_bar": plotly_charts.build_stacked_bar,
                    "stacked_bar_100": plotly_charts.build_stacked_bar_100,
                    "line": plotly_charts.build_line,
                    "area": plotly_charts.build_area,
                    "scatter": plotly_charts.build_scatter,
                    "bubble": plotly_charts.build_bubble,
                    "box": plotly_charts.build_box,
                    "violin": plotly_charts.build_violin,
                    "histogram": plotly_charts.build_histogram,
                    "heatmap": plotly_charts.build_heatmap,
                    "heatmap_annotated": plotly_charts.build_heatmap_annotated,
                    "radar": plotly_charts.build_radar,
                    "treemap": plotly_charts.build_treemap,
                    "sunburst": plotly_charts.build_sunburst,
                    "sankey": plotly_charts.build_sankey,
                    "flow_diagram": plotly_charts.build_flow_diagram,
                    "network_graph": plotly_charts.build_network_graph,
                    "runtime_breakdown": plotly_charts.build_runtime_breakdown,
                    "preset_comparison": plotly_charts.build_preset_comparison,
                }
                
                if chart_type in builder_map:
                    builder = builder_map[chart_type]
                    
                    # Special handling for flow/network diagrams
                    if chart_type == "flow_diagram":
                        nodes = st.session_state.df[st.session_state.chart_config.get("source", st.session_state.df.columns[0])].unique().tolist()
                        nodes += st.session_state.df[st.session_state.chart_config.get("target", st.session_state.df.columns[1])].unique().tolist()
                        nodes = list(set(nodes))
                        edges = list(zip(
                            st.session_state.df[st.session_state.chart_config.get("source")],
                            st.session_state.df[st.session_state.chart_config.get("target")]
                        ))
                        fig = builder(nodes=nodes, edges=edges, title=st.session_state.chart_config.get("title", "Flow Diagram"))
                    else:
                        fig = builder(st.session_state.df, **{k: v for k, v in st.session_state.chart_config.items() if k not in ["dpi", "export_formats"]})
                    
                    # Display chart
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export options
                    st.subheader("Export Chart")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        chart_name = st.text_input("Chart name for export", "thesis_chart")
                    
                    with col2:
                        if st.button("📥 Export to Files"):
                            export_formats = st.session_state.chart_config.get("export_formats", ["png", "svg"])
                            results = exporters.export_plotly_chart(
                                fig,
                                f"output/{chart_name}.{{}}",
                                export_formats,
                            )
                            
                            st.success("✅ Export complete!")
                            for fmt, path in results.items():
                                st.write(f"- {fmt.upper()}: `{path}`")
            
            except Exception as e:
                st.error(f"❌ Error generating chart: {e}")
                logger.exception("Chart generation error")


# ============================================================================
# QUICK ANALYSIS - AUTO-GENERATE ALL CHARTS
# ============================================================================

elif page == "🚀 Quick Analysis":
    st.header("🚀 Quick Analysis - Auto-Generate All Charts")
    st.markdown("""
    Upload an Excel file or CSV, and this tool will:
    1. 📖 Read all sheets
    2. 🧹 Clean and auto-detect the data
    3. 📊 Suggest optimal chart types
    4. ⚡ Generate all charts automatically
    """)
    
    # Upload section
    uploaded_file = st.file_uploader(
        "Upload data file (CSV, Excel with multiple sheets)",
        type=["csv", "xlsx", "xlsm", "xls", "xlsb", "ods"],
        key="quick_analysis_uploader"
    )
    
    if uploaded_file:
        import io
        
        # Cache file for multi-read
        file_bytes = uploaded_file.read()
        file_buffer = io.BytesIO(file_bytes)
        file_buffer.name = uploaded_file.name
        
        st.info(f"📄 File loaded: {uploaded_file.name}")
        
        # Get sheet names
        sheet_names = loaders.get_sheet_names(file_buffer)
        file_buffer.seek(0)
        
        if sheet_names:
            st.subheader("📑 Available Sheets")
            st.write(f"Found **{len(sheet_names)}** sheet(s): {', '.join(sheet_names)}")
            
            # Select sheets to analyze
            selected_sheets = st.multiselect(
                "Select sheets to analyze",
                sheet_names,
                default=sheet_names[:3] if len(sheet_names) > 3 else sheet_names
            )
            
            if selected_sheets and st.button("🎯 Generate All Charts", key="quick_gen_all"):
                with st.spinner("⏳ Analyzing data and generating charts..."):
                    all_charts_generated = 0
                    all_charts_failed = 0
                    
                    for sheet_name in selected_sheets:
                        file_buffer.seek(0)
                        try:
                            df = pd.read_excel(file_buffer, sheet_name=sheet_name)
                            cleaned_df = utils.clean_sheet_data(df)
                            
                            if cleaned_df is None or cleaned_df.empty:
                                st.warning(f"⚠️ Sheet '{sheet_name}': No usable data found")
                                continue
                            
                            st.subheader(f"📊 Sheet: {sheet_name}")
                            
                            # Show data preview
                            with st.expander(f"Data Preview - {sheet_name}"):
                                st.dataframe(cleaned_df.head(10), use_container_width=True)
                                st.caption(f"{len(cleaned_df)} rows × {len(cleaned_df.columns)} columns")
                            
                            # Get suggested charts
                            suggested_charts = utils.get_suggested_charts(cleaned_df)
                            
                            if not suggested_charts:
                                st.info(f"ℹ️ No suitable chart types found for '{sheet_name}'")
                                continue
                            
                            st.write(f"**Suggested chart types:** {', '.join(suggested_charts)}")
                            
                            # Generate charts
                            numeric_cols = utils.get_numeric_columns(cleaned_df)
                            cat_cols = utils.get_categorical_columns(cleaned_df)
                            
                            chart_cols = st.columns(2)
                            col_idx = 0
                            
                            for chart_type in suggested_charts:
                                try:
                                    col = chart_cols[col_idx % 2]
                                    col_idx += 1
                                    
                                    with col:
                                        # Apply appropriate chart based on data
                                        if chart_type == "scatter_matrix" and len(numeric_cols) >= 2:
                                            fig = plotly_charts.scatter_matrix(
                                                cleaned_df[numeric_cols[:4]],  # Limit to 4 columns for readability
                                                numeric_cols[:4]
                                            )
                                        elif chart_type == "grouped_bar" and len(cat_cols) > 0 and len(numeric_cols) > 0:
                                            fig = plotly_charts.grouped_bar_chart(
                                                cleaned_df,
                                                cat_cols[0],
                                                numeric_cols[:2]
                                            )
                                        elif chart_type == "heatmap" and len(numeric_cols) >= 3:
                                            fig = plotly_charts.correlation_heatmap(cleaned_df[numeric_cols], numeric_cols)
                                        elif chart_type == "bar":
                                            col1 = numeric_cols[0] if numeric_cols else None
                                            col2 = cat_cols[0] if cat_cols else None
                                            if col1:
                                                fig = plotly_charts.bar_chart(cleaned_df, col2, col1)
                                            else:
                                                fig = None
                                        elif chart_type == "line":
                                            col1 = numeric_cols[0] if numeric_cols else None
                                            if col1:
                                                fig = plotly_charts.line_chart(cleaned_df, None, col1)
                                            else:
                                                fig = None
                                        elif chart_type == "scatter":
                                            if len(numeric_cols) >= 2:
                                                fig = plotly_charts.scatter_plot(cleaned_df, numeric_cols[0], numeric_cols[1])
                                            else:
                                                fig = None
                                        elif chart_type == "box":
                                            if len(numeric_cols) >= 1:
                                                fig = plotly_charts.box_plot(cleaned_df[numeric_cols])
                                            else:
                                                fig = None
                                        elif chart_type == "violin":
                                            if len(numeric_cols) >= 1:
                                                fig = plotly_charts.violin_plot(cleaned_df[numeric_cols])
                                            else:
                                                fig = None
                                        elif chart_type == "histogram":
                                            if len(numeric_cols) >= 1:
                                                fig = plotly_charts.histogram(cleaned_df, numeric_cols[0])
                                            else:
                                                fig = None
                                        elif chart_type == "radar":
                                            if len(numeric_cols) >= 3:
                                                # Normalize for radar chart
                                                df_radar = cleaned_df[numeric_cols].iloc[:1].copy()
                                                fig = plotly_charts.radar_chart(
                                                    df_radar,
                                                    numeric_cols[:5],  # Limit to 5 for readability
                                                    f"Radar-{sheet_name}"
                                                )
                                            else:
                                                fig = None
                                        else:
                                            fig = None
                                        
                                        if fig:
                                            st.plotly_chart(fig, use_container_width=True)
                                            all_charts_generated += 1
                                        else:
                                            all_charts_failed += 1
                                
                                except Exception as e:
                                    st.error(f"Error generating {chart_type}: {str(e)}")
                                    all_charts_failed += 1
                                    logger.exception(f"Chart generation error for {chart_type}")
                        
                        except Exception as e:
                            st.error(f"Error processing sheet '{sheet_name}': {str(e)}")
                            logger.exception(f"Sheet processing error")
                    
                    # Summary
                    st.success(f"✅ Generated **{all_charts_generated}** charts!")
                    if all_charts_failed > 0:
                        st.warning(f"⚠️ Failed to generate {all_charts_failed} charts")
        else:
            # For CSV files without sheets
            try:
                file_buffer.seek(0)
                df = pd.read_csv(file_buffer)
                cleaned_df = utils.clean_sheet_data(df)
                
                if cleaned_df is not None and not cleaned_df.empty:
                    st.subheader("📊 Auto-Analysis Results")
                    st.dataframe(cleaned_df.head(10), use_container_width=True)
                    
                    suggested_charts = utils.get_suggested_charts(cleaned_df)
                    st.write(f"**Suggested charts:** {', '.join(suggested_charts)}")
            except Exception as e:
                st.error(f"Could not read file: {str(e)}")


# ============================================================================
# MULTI-SHEET ANALYSIS - COMPARE SHEETS
# ============================================================================

elif page == "📊 Multi-Sheet Analysis":
    st.header("📊 Multi-Sheet Analysis - Compare & Combine Data")
    st.markdown("""
    Compare metrics across different sheets in your Excel file:
    - 📊 Side-by-side comparison
    - 📈 Trend analysis across stages
    - 🎯 Combined metrics visualization
    """)
    
    # Upload section
    uploaded_file = st.file_uploader(
        "Upload Excel file with multiple sheets",
        type=["xlsx", "xlsm", "xls", "xlsb"],
        key="multi_sheet_uploader"
    )
    
    if uploaded_file:
        import io
        
        # Cache file for multi-read
        file_bytes = uploaded_file.read()
        file_buffer = io.BytesIO(file_bytes)
        file_buffer.name = uploaded_file.name
        
        st.info(f"📄 File loaded: {uploaded_file.name}")
        
        # Get sheet names
        sheet_names = loaders.get_sheet_names(file_buffer)
        
        if sheet_names and len(sheet_names) > 1:
            st.subheader("📑 Compare Sheets")
            
            col1, col2 = st.columns(2)
            with col1:
                sheet1 = st.selectbox("First sheet", sheet_names, key="sheet1")
            with col2:
                sheet2 = st.selectbox("Second sheet", sheet_names, index=1 if len(sheet_names) > 1 else 0, key="sheet2")
            
            if st.button("📊 Compare Sheets"):
                file_buffer.seek(0)
                
                try:
                    # Load both sheets
                    df1 = pd.read_excel(file_buffer, sheet_name=sheet1)
                    df1_clean = utils.clean_sheet_data(df1)
                    
                    file_buffer.seek(0)
                    df2 = pd.read_excel(file_buffer, sheet_name=sheet2)
                    df2_clean = utils.clean_sheet_data(df2)
                    
                    if df1_clean is None or df1_clean.empty or df2_clean is None or df2_clean.empty:
                        st.error("Could not clean one or both sheets")
                    else:
                        st.subheader(f"Comparison: {sheet1} vs {sheet2}")
                        
                        # Get numeric columns from both
                        numeric1 = utils.get_numeric_columns(df1_clean)
                        numeric2 = utils.get_numeric_columns(df2_clean)
                        common_metrics = list(set(numeric1) & set(numeric2))
                        
                        if not common_metrics:
                            st.warning("No common numeric metrics found")
                        else:
                            st.write(f"**Common metrics:** {', '.join(common_metrics[:5])}")
                            
                            # Let user select metric to compare
                            metric = st.selectbox("Select metric to compare", common_metrics)
                            
                            if metric:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.subheader(sheet1)
                                    try:
                                        fig1 = plotly_charts.histogram(df1_clean, metric)
                                        st.plotly_chart(fig1, use_container_width=True)
                                    except:
                                        st.dataframe(df1_clean[[metric]].describe())
                                
                                with col2:
                                    st.subheader(sheet2)
                                    try:
                                        fig2 = plotly_charts.histogram(df2_clean, metric)
                                        st.plotly_chart(fig2, use_container_width=True)
                                    except:
                                        st.dataframe(df2_clean[[metric]].describe())
                                
                                # Combined statistics
                                st.subheader("📊 Statistics Comparison")
                                stats1 = utils.get_column_stats(df1_clean[metric])
                                stats2 = utils.get_column_stats(df2_clean[metric])
                                
                                comparison_data = {
                                    'Metric': sheet1,
                                    sheet1: [stats1.get('mean', 'N/A'), stats1.get('std', 'N/A'), stats1.get('min', 'N/A'), stats1.get('max', 'N/A')],
                                    sheet2: [stats2.get('mean', 'N/A'), stats2.get('std', 'N/A'), stats2.get('min', 'N/A'), stats2.get('max', 'N/A')],
                                }
                                
                                comp_df = pd.DataFrame({
                                    'Statistic': ['Mean', 'Std Dev', 'Min', 'Max'],
                                    sheet1: comparison_data[sheet1],
                                    sheet2: comparison_data[sheet2],
                                })
                                st.dataframe(comp_df, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    logger.exception("Multi-sheet comparison error")
        
        else:
            st.warning("File needs at least 2 sheets for comparison")


# ============================================================================
# BIBLIOMETRIC ANALYSIS
# ============================================================================

elif page == "Bibliometric Analysis" or page == "📚 Bibliometric Analysis":
    st.header("📚 Bibliometric Analysis")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
    else:
        st.subheader("Analysis Options")
        
        analysis_type = st.radio(
            "Select Analysis",
            ["Summary Statistics", "Co-authorship Network", "Keyword Co-occurrence", "Source Frequency", "Citation Trends"],
        )
        
        if analysis_type == "Summary Statistics":
            st.subheader("Bibliometric Summary")
            
            # Assume specific column names
            author_col = st.selectbox("Author column", ["authors"] + st.session_state.df.columns.tolist(), index=0 if "authors" in st.session_state.df.columns else 0)
            keyword_col = st.selectbox("Keyword column", ["keywords"] + st.session_state.df.columns.tolist(), index=0 if "keywords" in st.session_state.df.columns else 0)
            source_col = st.selectbox("Source column", ["source"] + st.session_state.df.columns.tolist(), index=0 if "source" in st.session_state.df.columns else 0)
            
            if author_col and keyword_col and source_col:
                try:
                    summary = bibliometric.extract_bibliometric_summary(st.session_state.df)
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Total Publications", summary.get("total_publications", 0))
                    with col2:
                        st.metric("Years", summary.get("publication_years", "N/A"))
                    with col3:
                        st.metric("Avg Citations", f"{summary.get('average_citations', 0):.1f}")
                    with col4:
                        st.metric("Unique Authors", summary.get("unique_authors", 0))
                    with col5:
                        st.metric("Unique Sources", summary.get("unique_sources", 0))
                
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif analysis_type == "Co-authorship Network":
            st.subheader("Co-authorship Network")
            
            author_col = st.selectbox("Author column", st.session_state.df.columns)
            separator = st.selectbox("Separator", [";", ",", "|"])
            
            if st.button("🔗 Build Network"):
                try:
                    G, stats = bibliometric.create_coauthorship_network(st.session_state.df, author_col)
                    
                    st.success(f"✅ Network created: {len(G.nodes())} authors, {len(G.edges())} collaborations")
                    
                    # Visualize as network graph
                    edges = list(G.edges())
                    nodes = list(G.nodes())
                    
                    fig = plotly_charts.build_network_graph(edges, nodes, title="Co-authorship Network")
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif analysis_type == "Keyword Co-occurrence":
            st.subheader("Keyword Co-occurrence Network")
            
            keyword_col = st.selectbox("Keyword column", st.session_state.df.columns)
            min_count = st.slider("Minimum co-occurrence count", 1, 10, 2)
            
            if st.button("🔗 Build Keyword Network"):
                try:
                    G, stats = bibliometric.create_keyword_network(st.session_state.df, keyword_col)
                    
                    st.success(f"✅ Network created: {len(G.nodes())} keywords, {len(G.edges())} co-occurrences")
                    
                    edges = list(G.edges())
                    nodes = list(G.nodes())
                    
                    fig = plotly_charts.build_network_graph(edges, nodes, title="Keyword Co-occurrence Network")
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif analysis_type == "Source Frequency":
            st.subheader("Publication by Source")
            
            source_col = st.selectbox("Source column", st.session_state.df.columns)
            
            if st.button("📊 Analyze"):
                try:
                    freq_df = bibliometric.create_source_frequency_table(st.session_state.df, source_col)
                    
                    fig = plotly_charts.build_bar(
                        freq_df,
                        x="source",
                        y="count",
                        title="Publication Frequency by Source",
                        y_label="Count",
                        sort_by="count",
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(freq_df, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif analysis_type == "Citation Trends":
            st.subheader("Citation Trends Over Time")
            
            year_col = st.selectbox("Year column", st.session_state.df.columns)
            citation_col = st.selectbox("Citation count column", st.session_state.df.columns)
            
            if st.button("📈 Plot"):
                try:
                    trends_df = bibliometric.create_citations_over_time(st.session_state.df, year_col, citation_col)
                    
                    fig = plotly_charts.build_line(
                        trends_df,
                        x=year_col,
                        y=citation_col,
                        title="Citations Over Time",
                        y_label="Citation Count",
                        markers=True,
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error: {e}")


# ============================================================================
# GRAPH & DIAGRAMS
# ============================================================================

elif page == "Graph & Diagrams" or page == "🔗 Graph & Diagrams":
    st.header("🔗 Graph & Diagrams")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
    else:
        diagram_type = st.radio(
            "Diagram Type",
            ["Space Syntax Diagram", "Circulation Diagram", "Adjacency Matrix", "Graph Visualization"],
        )
        
        source_col = st.selectbox("From/Source Column", st.session_state.df.columns)
        target_col = st.selectbox("To/Target Column", st.session_state.df.columns)
        
        if diagram_type == "Space Syntax Diagram":
            st.subheader("Space Syntax Accessibility Graph")
            
            layout = st.selectbox("Layout", ["spring", "circular", "hierarchical"])
            
            if st.button("🎨 Generate Diagram"):
                try:
                    fig = graph_diagrams.create_space_syntax_diagram(
                        st.session_state.df,
                        layout=layout,
                        title="Space Syntax Accessibility Graph",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show metrics
                    G = graph_diagrams.parse_adjacency_matrix(st.session_state.df, source_col, target_col)
                    metrics = graph_diagrams.calculate_graph_metrics(G)
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("Nodes", metrics["nodes"])
                    with col2:
                        st.metric("Edges", metrics["edges"])
                    with col3:
                        st.metric("Density", f"{metrics['density']:.3f}")
                    with col4:
                        st.metric("Avg Degree", f"{metrics['average_degree']:.1f}")
                    with col5:
                        st.metric("Clustering", f"{metrics['average_clustering']:.3f}")
                
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif diagram_type == "Circulation Diagram":
            st.subheader("Circulation Paths")
            
            if st.button("🎨 Generate Diagram"):
                try:
                    fig = graph_diagrams.create_circulation_diagram(
                        st.session_state.df,
                        title="Circulation Diagram",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif diagram_type == "Adjacency Matrix":
            st.subheader("Adjacency Matrix Heatmap")
            
            weight_col = st.selectbox("Weight Column (optional)", [None] + st.session_state.df.columns.tolist())
            
            if st.button("🎨 Generate Heatmap"):
                try:
                    fig = graph_diagrams.create_adjacency_matrix_heatmap(
                        st.session_state.df,
                        node1_col=source_col,
                        node2_col=target_col,
                        weight_col=weight_col,
                        title="Adjacency Matrix",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif diagram_type == "Graph Visualization":
            st.subheader("Network Graph")
            
            layout = st.selectbox("Layout", ["spring", "circular"])
            
            if st.button("🎨 Visualize Network"):
                try:
                    edges = list(zip(
                        st.session_state.df[source_col],
                        st.session_state.df[target_col]
                    ))
                    nodes = list(set(st.session_state.df[source_col].tolist() + st.session_state.df[target_col].tolist()))
                    
                    fig = plotly_charts.build_network_graph(edges, nodes, layout=layout, title="Network Graph")
                    st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"Error: {e}")


# ============================================================================
# BATCH GENERATOR
# ============================================================================

elif page == "Batch Generator" or page == "🔄 Batch Generator":
    st.header("🔄 Batch Chart Generator")
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload data first")
    else:
        st.subheader("Generate Multiple Charts at Once")
        
        # Configuration template
        batch_config_template = {
            "charts": [
                {
                    "name": "chart_1",
                    "type": "bar",
                    "x": st.session_state.df.columns[0],
                    "y": st.session_state.df.columns[1] if len(st.session_state.df.columns) > 1 else st.session_state.df.columns[0],
                    "title": "Chart 1",
                },
            ]
        }
        
        config_json = st.text_area(
            "Batch Configuration (JSON)",
            value=json.dumps(batch_config_template, indent=2),
            height=300,
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Generate All Charts"):
                try:
                    config = json.loads(config_json)
                    
                    charts_generated = 0
                    for chart_def in config.get("charts", []):
                        chart_name = chart_def.get("name", "chart")
                        chart_type = chart_def.get("type", "bar")
                        
                        # Build chart
                        builder_map = {
                            "bar": plotly_charts.build_bar,
                            "line": plotly_charts.build_line,
                            "scatter": plotly_charts.build_scatter,
                            "box": plotly_charts.build_box,
                        }
                        
                        if chart_type in builder_map:
                            builder = builder_map[chart_type]
                            fig = builder(st.session_state.df, **{k: v for k, v in chart_def.items() if k not in ["name", "type"]})
                            
                            # Export
                            exporters.export_plotly_chart(fig, f"output/{chart_name}.{{}}", ["png", "html"])
                            charts_generated += 1
                    
                    st.success(f"✅ Generated {charts_generated} charts!")
                
                except json.JSONDecodeError:
                    st.error("Invalid JSON configuration")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            st.info("💡 Edit the JSON above to change chart definitions, then click Generate")


# ============================================================================
# EXAMPLES & PRESETS
# ============================================================================

elif page == "Examples & Presets" or page == "✨ Examples & Presets":
    st.header("📚 Examples & Presets")
    
    st.write("Click the button below to generate all sample examples automatically.")
    
    if st.button("🎨 Generate All Built-in Examples", use_container_width=True, key="generate_all_examples"):
        st.subheader("✅ Generating Examples...")
        
        examples_data = [
            {
                "name": "📊 Preset Performance Comparison",
                "file": "preset_comparison.csv",
                "chart": "grouped_bar",
                "config": {"x": "preset_name", "y_columns": ["wall_efficiency", "daylight_ratio", "energy_score"]}
            },
            {
                "name": "⏱️ Runtime by Generation Stage",
                "file": "runtime_breakdown.csv",
                "chart": "bar",
                "config": {"x": "stage", "y": "runtime_ms", "color": "preset", "x_label": "Stage", "y_label": "Time (ms)"}
            },
            {
                "name": "🔗 Wall Efficiency vs Daylight Access",
                "file": "preset_comparison.csv",
                "chart": "scatter",
                "config": {"x": "wall_efficiency", "y": "daylight_ratio", "color": "energy_score", "size": "coverage_percent"}
            },
        ]
        
        builder_map = {
            "bar": plotly_charts.build_bar,
            "grouped_bar": plotly_charts.build_grouped_bar,
            "scatter": plotly_charts.build_scatter,
            "bubble": plotly_charts.build_bubble,
            "box": plotly_charts.build_box,
            "violin": plotly_charts.build_violin,
            "line": plotly_charts.build_line,
            "area": plotly_charts.build_area,
        }
        
        success_count = 0
        for example in examples_data:
            try:
                st.subheader(example["name"])
                df = utils.load_sample_data(example["file"])
                if df is not None:
                    chart_type = example["chart"]
                    builder = builder_map.get(chart_type)
                    if builder:
                        fig = builder(df, **example["config"])
                        st.plotly_chart(fig, use_container_width=True)
                        success_count += 1
                else:
                    st.warning(f"Could not load {example['file']}")
            except Exception as e:
                st.warning(f"Could not generate {example['name']}: {str(e)[:100]}")
        
        if success_count > 0:
            st.success(f"✅ Generated {success_count} examples successfully!")
    
    # Distribution Analysis - Two charts in columns
    if st.button("📦 Generate Distribution Examples", use_container_width=True, key="gen_dist"):
        st.subheader("📦 Distribution Analysis Examples")
        df = utils.load_sample_data("experiment_runs.csv")
        if df is not None:
            col1, col2 = st.columns(2)
            try:
                with col1:
                    st.subheader("📦 Box Plot")
                    fig1 = plotly_charts.build_box(df, x="preset", y="avg_room_area", title="Room Area Distribution")
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    st.subheader("🎻 Violin Plot")
                    fig2 = plotly_charts.build_violin(df, x="preset", y="wall_efficiency", title="Wall Efficiency Distribution")
                    st.plotly_chart(fig2, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Could not load experiment_runs.csv")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox("Font Style", ["Times New Roman", "Arial", "Helvetica"])
    with col2:
        st.selectbox("Color Mode", ["Full Color", "Grayscale", "Black & White"])
    with col3:
        st.selectbox("Export DPI", [100, 150, 200, 300])
    
    st.info("💡 These settings will be applied to all future exports until changed")


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**📊 Thesis Viz Toolkit**")
    st.markdown("Publication-ready visualizations")
    st.markdown("""<small>v1.0 - 2026</small>""", unsafe_allow_html=True)

with footer_col2:
    st.markdown("**📁 Output Location**")
    st.markdown("`output/` directory")
    st.markdown("**Formats:** PNG • SVG • PDF • HTML")

with footer_col3:
    st.markdown("**👨‍💻 Developer**")
    st.markdown("Mohammad Amanzadegan")
    st.markdown("[DrCG.Net](https://drcg.net)")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 12px;'>"
    "<p><strong>DrCG</strong> Built with ❤️ for thesis visualization | "
    "<a href='https://github.com/drcg-net/DrCG-Thesis-Visualization-Toolkit' target='_blank'>GitHub</a> | "
    "<a href='https://streamlit.io' target='_blank'>Streamlit</a> | "
    "<a href='https://www.Amanzadegan.com' target='_blank'>Amanzadegan</a> | "
    "<a href='https://drcg.net' target='_blank'>DrCG.Net</a></p>"
    "</div>",
    unsafe_allow_html=True
)
