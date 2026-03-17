# 📊 DrCG Thesis Visualization Toolkit (Thesis Chart Generator)

A focused chart-generation toolkit for PhD thesis research.

This app provides an easy way to upload tables (CSV/Excel), automatically suggest relevant chart types, and output publication-ready figures (PNG/SVG/PDF/HTML).

Built with Streamlit and Plotly.

## Features

✨ **Data Import**
- CSV, Excel (XLSX/XLSM), XLS, XLSB, ODS formats
- Multi-sheet support with sheet selection
- Automatic data type detection (numeric/categorical)

📈 **20+ Chart Types**
- **Standard**: Bar, Grouped Bar, Stacked Bar, 100% Stacked Bar
- **Trends**: Line, Area
- **Relationships**: Scatter, Bubble
- **Distribution**: Box Plot, Violin Plot, Histogram
- **Hierarchical**: Treemap, Sunburst, Sankey
- **Network**: Graph, Flow Diagram, Network Graph
- **Specialized**: Radar, Heatmap, Runtime Breakdown, Preset Comparison
- **Spatial**: Space Syntax Diagrams, Circulation Diagrams, Adjacency Matrices

🎨 **Customization**
- Custom titles, labels, colors
- Column mapping (X/Y axes, size, color, grouping)
- Publication mode with thesis defaults
- Grayscale/readable modes

📥 **Export Formats**
- PNG (print-quality, up to 300 DPI)
- SVG (vector, scalable)
- PDF (publication-ready)
- Interactive HTML (web-shareable)

📚 **Bibliometric Analysis**
- Co-authorship networks
- Keyword co-occurrence analysis
- Source frequency tables
- Citation trends
- VOSviewer data export

💾 **Configuration & Batch**
- Save chart configurations as JSON
- Reproduce charts with saved configs
- Batch generation of multiple charts
- Sample presets for common use cases

## Installation

### Prerequisites

- **Python 3.11+** (check with `python --version`)
- **Windows 10+**, macOS, or Linux
- **Graphviz** (for flow diagrams) - see below

### Step 1: Extract and Navigate

```powershell
cd e:\DrCG_Floor_Generator\thesis_viz_app
```

### Step 2: Install Graphviz (Windows)

If you don't have Graphviz installed:

**Option A: Chocolatey (recommended)**
```powershell
choco install graphviz
```

**Option B: Manual Download**
Download from https://graphviz.org/download/ and run the installer.

**Option C: Direct Install Command**
```powershell
winget install Graphviz.Graphviz
```

Verify installation:
```powershell
dot -V
```

### Step 3: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you see an error about execution policy, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry the activation command.

### Step 4: Install Python Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- streamlit - Web application framework
- pandas, numpy - Data handling
- plotly - Interactive visualizations
- kaleido - Chart export to static formats
- openpyxl, pyxlsb, odfpy - Excel/ODS file support
- networkx, graphviz - Network visualization
- bibtexparser - Bibliographic data parsing
- And more (see requirements.txt)

### Step 5: Verify Installation

```powershell
python -c "import streamlit; import plotly; import pandas; print('✅ All dependencies installed!')"
```

## 🚀 Deploying (GitHub + Streamlit)

To make this tool available to others, publish the repository on GitHub and then deploy it using **Streamlit Community Cloud**.

### 1) Push to GitHub
1. Create a new GitHub repo (public or private)
2. Add all files and commit:
   ```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

### 2) Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Log in and connect your GitHub account
3. Select your repository and choose the branch `main`
4. Set the **main file** to `app.py`
5. Click **Deploy**

✅ Your app will be live at `https://<your-username>.streamlit.app` (or similar).

> Note: If you use Graphviz-dependent charts (flow diagrams, network graphs), make sure the deployment environment can install Graphviz (Streamlit Cloud supports this via the `packages.txt` file).

## 🧑‍💻 Credits

Developed by **DrCG.Net** / **Mohammad Amanzadegan**

If you reuse or adapt this tool, please keep attribution.

> ✅ **Important:** The MIT license requires that this copyright notice and the license text
> remain intact in any copies, modified versions, or distributions of this project.

## Quick Start

### Launch the App

```powershell
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`

### First Steps

1. **Home Page** - Review features and samples
2. **Data Uploader** - Import your CSV/Excel files
3. **Chart Builder** - Select chart type and customize
4. **Export** - Save as PNG/SVG/PDF/HTML
5. **Batch Generator** - Create multiple charts with JSON config

### Using Sample Data

Sample CSV files are in the `samples/` folder:
- `preset_comparison.csv` - Architecture preset metrics
- `experiment_runs.csv` - Multi-run experiment results
- `runtime_breakdown.csv` - Execution timing by stage
- `batch_config.csv` - Batch configuration example

Click "Use Sample Data" in the uploader to load them instantly.

## Usage Examples

### Example 1: Basic Bar Chart

1. Go to **Data Uploader**
2. Click "Use Sample Data" → Select `preset_comparison.csv`
3. Go to **Chart Builder**
4. Select Chart Type: `bar`
5. X-axis: `preset_name`
6. Y-axis: `coverage_percent`
7. Enter Title: "Site Coverage by Preset"
8. Click "Generate Chart"
9. Click "Export to Files" → Choose PNG/SVG

### Example 2: Comparison Dashboard

1. Upload `experiment_runs.csv`
2. Go to **Chart Builder**
3. Create stacked bar chart:
   - Chart Type: `stacked_bar`
   - X-axis: `preset`
   - Y columns: `avg_room_area`, `wall_efficiency`, `daylight_access`
4. Save configuration as JSON for later

### Example 3: Network Visualization

1. Upload a table with columns: `from_space`, `to_space`, `adjacency_score`
2. Go to **Graph & Diagrams**
3. Select "Space Syntax Diagram"
4. Map columns accordingly
5. Choose layout (spring/circular)
6. Generate and export

### Example 4: Batch Generation

1. Upload your data
2. Go to **Batch Generator**
3. Edit JSON config with multiple chart definitions
4. Click "Generate All Charts"
5. All charts export to `output/` folder

## File Structure

```
thesis_viz_app/
├── app.py                          # Main Streamlit app
├── requirements.txt                 # Python dependencies
├── .env.example                     # Configuration template
├── README.md                        # This file
│
├── src/
│   ├── __init__.py
│   ├── loaders.py                  # Data loading (CSV/Excel/ODS)
│   ├── exporters.py                # Export to PNG/SVG/PDF/HTML
│   ├── utils.py                    # Utilities (normalization, stats)
│   ├── chart_registry.py           # Chart type registry
│   ├── bibliometric.py             # Bibliometric analysis
│   ├── graph_diagrams.py           # Network/space syntax diagrams
│   │
│   └── chart_builders/
│       ├── __init__.py
│       └── plotly_charts.py        # All chart builders
│
├── config/
│   └── chart_presets.json          # Predefined chart presets
│
├── samples/
│   ├── preset_comparison.csv       # Sample data
│   ├── experiment_runs.csv
│   ├── runtime_breakdown.csv
│   └── batch_config.csv
│
└── output/
    ├── png/                        # PNG exports
    ├── svg/                        # SVG exports
    ├── pdf/                        # PDF exports
    ├── html/                       # Interactive HTML
    └── configs/                    # Saved chart configs
```

## Supported Data Formats

- **CSV** (.csv)
- **Excel** (.xlsx, .xlsm, .xls)
- **Binary Excel** (.xlsb)
- **OpenDocument Spreadsheet** (.ods)
- **OpenDocument Text** (.odt) - with table extraction

## Export Features

### PNG
- Publication-quality at 300 DPI
- Perfect for papers and theses
- Fixed size (1200×800 px, configurable)

### SVG
- Vector format (infinitely scalable)
- Editable in Illustrator, Inkscape
- Best for final refinement

### PDF
- Print-ready format
- Embeds fonts
- Page-sized output

### Interactive HTML
- Hover information
- Zoom and pan
- Shareable via web

## Advanced Features

### Custom Themes

Edit `config/chart_presets.json` to customize:
- Font family and size
- Line widths and marker sizes
- Color schemes
- Margin sizes
- DPI defaults

### Batch Configuration Format

```json
{
  "charts": [
    {
      "name": "chart_1",
      "type": "bar",
      "x": "column_name",
      "y": "metric_name",
      "title": "My Chart",
      "color": "preset"
    },
    {
      "name": "chart_2",
      "type": "scatter",
      "x": "x_metric",
      "y": "y_metric",
      "size": "area_metric"
    }
  ]
}
```

### Space Syntax Analysis

For architectural spatial analysis:
1. Prepare data: `[from_space, to_space, connection_strength]`
2. Upload to app
3. Go to **Graph & Diagrams**
4. Select "Space Syntax Diagram"
5. View connectivity metrics (degree, centrality, clustering)
6. Export as network visualization

### Bibliometric Analysis

Requires columns:
- `authors` (semicolon-separated)
- `keywords` (semicolon-separated)
- `source` (journal/conference)
- `citations` (optional)
- `year` (optional)

Features:
- Co-authorship networks
- Keyword co-occurrence
- Publication frequency
- Citation trends
- VOSviewer compatibility

## Troubleshooting

### Issue: "Graphviz not found"
**Solution**: Install Graphviz:
```powershell
# Windows
winget install Graphviz.Graphviz

# Or use Chocolatey
choco install graphviz
```

Then restart the app.

### Issue: "Permission denied" when activating venv
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "No module named 'kaleido'"
**Solution**: Kaleido requires extra system libraries. Reinstall with:
```powershell
pip install --force-reinstall --no-cache-dir kaleido
```

### Issue: "UnicodeEncodeError" with Persian text
**Solution**: Ensure files are UTF-8 encoded. In Streamlit, Persian text is natively supported.

### Issue: App says "Connection refused"
**Solution**: Check if port 8501 is in use:
```powershell
netstat -ano | findstr :8501
```

To use a different port:
```powershell
streamlit run app.py --server.port 8502
```

## Performance Tips

- **Large datasets**: Consider filtering columns before upload
- **Many charts**: Use batch generator for efficiency
- **High-DPI export**: Takes longer; use 150-200 DPI for draft mode
- **Network graphs**: Keep < 100 nodes for interactive performance

## Architecture & Design

### Technology Stack
- **Frontend**: Streamlit (rapid prototyping)
- **Visualization**: Plotly (interactive + static export)
- **Data**: Pandas/NumPy
- **Networks**: NetworkX
- **Export**: Kaleido (Plotly), native formats

### Modular Design
- Loaders handle file format detection
- Chart builders are type-specific functions
- Exporters handle multi-format output
- Utilities provide reusable functions

### Extension Points

Add new chart types:
1. Create builder function in `src/chart_builders/plotly_charts.py`
2. Register in `src/chart_registry.py`
3. Add UI form in `app.py`

Add new file format:
1. Create loader in `src/loaders.py`
2. Update file uploader types in `app.py`

## Configuration

### Environment Variables (.env)

Create `.env` file from `.env.example`:

```
VOSVVIEWER_PATH=C:\Program Files\VOSviewer\VOSviewer.exe
OUTPUT_DIR=output
DPI_PRINT=300
STREAMLIT_SERVER_PORT=8501
```

### Streamlit Config

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "serif"

[client]
toolbarMode = "minimal"
```

## Common Workflows

### PhD Thesis Visualization Pipeline

1. **Data Collection**: Experiment runs, metrics
2. **Upload**: CSV/Excel with results
3. **Exploration**: Preview, statistics
4. **Chart Creation**: Select chart types
5. **Customization**: Labels, colors, styles
6. **Export**: PNG/SVG at 300 DPI
7. **Archiving**: Save JSON configs

### Comparative Analysis

1. Upload multi-preset comparison data
2. Create bar charts for each metric
3. Use grouped/stacked variants for relationships
4. Batch export all charts
5. Create composite figures with saved SVGs

### Network Analysis

1. Prepare edge list (source, target, weight)
2. Upload to app
3. Visualize as network, space syntax, or circulation diagram
4. Calculate metrics (centrality, clustering)
5. Export network data (GraphML/GEXF) for further analysis

## Citation & Attribution

If you use this toolkit for research, cite as:

```bibtex
@software{thesis_viz_toolkit,
  title={Thesis Visualization Toolkit},
  author={Mohammad Amanzadegan},
  year={2026},
  url={https://github.com/your-repo/thesis-viz},
  note={PhD Thesis Support Tool}
}
```

## License

MIT License - See LICENSE file for details

## Support & Issues

For bugs, feature requests, or questions:
1. Check this README for common issues
2. Review sample data for format examples
3. Inspect browser console for errors (F12)
4. Check terminal output for debug info

## Changelog

### v1.0.0 (Initial Release)
- ✅ 20+ chart types
- ✅ Multi-format export (PNG/SVG/PDF/HTML)
- ✅ Data file support (CSV/Excel/ODS)
- ✅ Bibliometric analysis
- ✅ Network visualization
- ✅ Batch chart generation
- ✅ Configuration saving/loading

## Future Enhancements

- 🔄 Real-time chart updates
- 🎨 More theme options
- 📱 Mobile-responsive UI
- 🤖 AI-powered chart suggestions
- 🔗 Multi-file joins
- 📊 Statistical analysis tools
- 🌍 Multilingual support

## Quick Reference

### Launch
```powershell
cd thesis_viz_app
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

### Access
```
http://localhost:8501
```

### Output Location
```
thesis_viz_app/output/
```

### Deactivate Virtual Environment
```powershell
deactivate
```

---

**Built with ❤️ for academic research**

Last Updated: March 17, 2026
