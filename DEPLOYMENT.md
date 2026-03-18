# 🚀 Deployment Guide - DrCG Thesis Visualization Toolkit

## Repository Information

- **Repository:** `drcg-net/DrCG-Thesis-Visualization-Toolkit`
- **GitHub:** https://github.com/drcg-net/DrCG-Thesis-Visualization-Toolkit
- **Website:** www.Amanzadegan.com
- **Organization:** DrCG.Net

---

## Deploy to Streamlit Cloud

### Steps:

1. **Visit Streamlit Cloud**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)

2. **Sign Up / Log In**
   - Create an account or log in with GitHub

3. **Connect GitHub Repository**
   - Click "New app"
   - Select "From GitHub"
   - Choose: `drcg-net/DrCG-Thesis-Visualization-Toolkit`

4. **Configure Deployment**
   - **Branch:** `main` (or your desired branch)
   - **Main file path:** `app.py`
   - **Python version:** 3.10+

5. **Click Deploy**
   - Streamlit will automatically install dependencies from `requirements.txt`
   - App will be live in a few minutes!

---

## Local Development

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/drcg-net/DrCG-Thesis-Visualization-Toolkit.git
cd DrCG-Thesis-Visualization-Toolkit

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
docker build -t thesis-viz-toolkit .
docker run -p 8501:8501 thesis-viz-toolkit
```

---

## Environment Variables

Create a `.env` file (for local development only):

```
# Optional: Add your configuration here
# Keep this file out of version control
```

---

## Supported Platforms

- ✅ **Streamlit Cloud** (recommended)
- ✅ **Heroku**
- ✅ **AWS**
- ✅ **Docker**
- ✅ **Google Cloud**
- ✅ **Local/On-Premise**

---

## Support & Contact

- **Developer:** Mohammad Amanzadegan
- **Website:** www.Amanzadegan.com
- **Organization:** DrCG.Net
- **GitHub Issues:** https://github.com/drcg-net/DrCG-Thesis-Visualization-Toolkit/issues

---

## License

MIT License - See [LICENSE](./LICENSE) for details.

**Copyright © 2026 DrCG.Net / Mohammad Amanzadegan**

For more information, visit: www.Amanzadegan.com
