# MAP-8 IRI Empathy Research Project

This project implements the **MAP-8 (Modeling and Analysis Pipeline)** roadmap for analyzing empathy dimensions using the Interpersonal Reactivity Index (IRI) across two cohort datasets (2023, 2024). 

> **Note:** The 2025 dataset is currently excluded from the core pipeline as per research requirements to focus on validated two-year longitudinal patterns.

## 📁 Project Structure

```text
2026-MAP8_IRI_Empat-a/
├── 00_raw/                # Original Excel datasets (2023, 2024, 2025)
├── 01_harmonized/         # Unified CSVs (Standardized 1-5 scale, Dual-Cleaning versions)
├── 02_eda/                # Comparative Descriptive Stats & Outlier Diagnostics
├── 03_sem/                # Reliability, Factorability, and CFA (Dual Versions)
├── 04_qca/                # fsQCA reports with Sociodemographic variables (Gender, SES)
├── 05_clustering/         # Hierarchical Profiles & Sensitivity Figures
├── 06_reports/            # Final Consolidated Manuscript & Technical Summaries
├── code/                  # Analysis scripts (R)
├── scripts/               # Processing, Modeling, and Word Synthesis (Python)
├── docs/                  # Methodology and instrument documentation
├── main.py                # Master execution pipeline
├── run_full_reproduction.py # One-click environment sync & pipeline execution
└── README.md              # Project overview
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.12+**: `pandas`, `numpy`, `semopy`, `factor_analyzer`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `python-docx`, `openpyxl`.
- **R 4.5.1+**: `QCA`, `admisc` (Dependencies are automatically resolved by the pipeline).

### ⚡ One-Click Reproduction
To execute the entire pipeline from scratch (synchronizing dependencies, harmonizing data, running dual-mode analysis, and generating the final academic manuscript):

```powershell
python run_full_reproduction.py
```
*The script handles R execution automatically if the path `C:\Program Files\R\R-4.5.1\bin\R.exe` exists.*

### 🛠️ Granular Execution Workflow
If you prefer to run steps individually:

1. **Full Pipeline Execution**:
   Performs dual-mode analysis (QC-only vs QC+MD), SEM/CFA, Clustering, and fsQCA.
   ```powershell
   python main.py
   ```

2. **Generate the Academic Manuscript**:
   Synthesizes all tables/figures into a formatted Word document with **Sensitivity Analysis**.
   ```powershell
   python scripts/generate_word_report.py
   ```

3. **Analysis Dashboard**: 
   Explore the results interactively via the Streamlit playground.
   ```powershell
   python -m streamlit run streamlit_app.py
   ```

## ✨ New Features & Methodological Advances

### 🔍 Dual-Mode Sensitivity Analysis
The pipeline now operates on two data levels to ensure maximum transparency:
- **Level 1 (QC-Only)**: Full sample after attention-check filtering ($N \approx 1,138$).
- **Level 2 (QC + MD)**: Refined sample after removing multivariate outliers via **Mahalanobis Distance** ($N \approx 1,083$).
*The final report contrasts results from both levels to demonstrate finding stability.*

### 👥 Sociodemographic Integration
fsQCA configurations now explicitly incorporate:
- **Gender**: Dummy-coded (`1=Female`, `0=Male`).
- **SES**: Dichotomized (`1=High SES [Level 3+]`, `0=Low SES`).

### 📊 Comprehensive Academic Reporting
The generated Word Manuscript follows the **MAP-8 structure** and includes:
- **Table 1**: Comparative Descriptive Statistics.
- **Table 3**: Standardized CFA Loadings.
- **Table 4**: Parsimonious Configurational Solutions.
- **Table 7**: SEM Fit Sensitivity (CFI, TLI, RMSEA comparison across cleaning modes).
- **Figure 1**: Comparative Cluster Boxplots.

## 📝 Documentation
- **Methodology**: Detailed step-by-step logic in `docs/MAP8_IRI_pipeline.md`.
- **Instruments**: Technical comparison of IRI items in `docs/IRI_Instruments.md`.
- **Manuscript Blueprint**: Logic and structure overview in `MAP8_case_study_and_IRI_blueprint.md`.
