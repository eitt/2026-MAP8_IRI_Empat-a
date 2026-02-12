# Streamlit Cloud Deployment Guide

This document explains how to deploy the MAP-8 IRI Streamlit app as a stable, publicly accessible website.

## 🚀 Quick Start: Deploy to Streamlit Cloud

Streamlit Cloud is the official platform for hosting Streamlit apps. It's **free**, requires **minimal configuration**, and integrates directly with GitHub.

### Step 1: Prepare Your Repository

Ensure your GitHub repository contains:
- `streamlit_app.py` ✅
- `requirements.txt` ✅
- `.streamlit/config.toml` ✅
- All data files in `01_harmonized/` (committed to Git)

### Step 2: Sign Up for Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub repositories

### Step 3: Deploy Your App

1. Click **"New app"** on the Streamlit Cloud dashboard
2. Select:
   - **Repository**: `eitt/2026-MAP8_IRI_Empat-a`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Click **"Deploy!"**

Streamlit will automatically:
- Install dependencies from `requirements.txt`
- Run your app
- Assign you a public URL (e.g., `https://map8-iri-playground.streamlit.app`)

### Step 4: Share Your App

Your app is now live! Share the URL with collaborators and users.

---

## ⚙️ Configuration Files

### `.streamlit/config.toml`
This file customizes your app's appearance. Modified settings include:
- **Color scheme**: Matches your Streamlit code styling
- **Font**: Standard sans-serif
- **Error details**: Enabled for debugging

### `requirements.txt`
Lists all Python dependencies. Streamlit Cloud installs these automatically.

Current dependencies:
- `streamlit` - Web framework
- `pandas`, `numpy` - Data manipulation
- `plotly` - Interactive visualizations
- `scikit-learn`, `scipy` - Statistical analysis
- `factor-analyzer` - Factor analysis
- `semopy` - Structural equation modeling
- `openpyxl`, `python-docx`, `matplotlib`, `seaborn` - Additional tools

---

## 📦 Important Notes for Deployment

### Data Files
- Ensure `01_harmonized/df_iri_all_harmonized.csv` and other data files are **committed to Git**
- Large files may cause slow deployments; consider using Git LFS if files exceed 100MB
- Check `.gitignore` to ensure data isn't excluded

### Performance
- First load may take 30-60 seconds (dependency installation)
- Subsequent loads are instant
- Streamlit Cloud provides generous free tier: 1 GB RAM, 100 MB storage per app

### Automatic Redeployment
- Changes pushed to `main` branch automatically redeploy your app
- Deployments typically complete within 2-5 minutes

---

## 🔒 Environment Variables (Optional)

For production deployments with sensitive data, use Streamlit Cloud secrets:

1. Navigate to your app settings on share.streamlit.io
2. Click **"Secrets"**
3. Add environment variables in TOML format

Access in your app with:
```python
import streamlit as st
my_secret = st.secrets["my_secret_key"]
```

---

## 🐛 Troubleshooting

### App won't start
- Check the **Logs** tab on your Streamlit Cloud dashboard
- Ensure `streamlit_app.py` exists in the repository root
- Verify all dependencies are in `requirements.txt`

### Missing data files
- Commit data files to Git
- Check that relative file paths (e.g., `01_harmonized/...`) are correct

### Slow performance
- Profile your app using Streamlit's built-in tools
- Consider caching expensive computations with `@st.cache_data`

### Module import errors
- Add missing packages to `requirements.txt`
- Run `pip install -r requirements.txt` locally to test

---

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/deploy/streamlit-cloud)
- [Streamlit Security Best Practices](https://docs.streamlit.io/deploy/streamlit-cloud/deploy-your-app/security-and-account-safety)
- [GitHub OAuth Guide](https://docs.github.com/en/developers/apps/building-oauth-apps)

---

**Your app is ready for stable, production-grade deployment!** 🎉
