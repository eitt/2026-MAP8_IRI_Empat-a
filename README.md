# MAP-8 IRI Empathy Research Project

This project implements the **MAP-8 (Modeling and Analysis Pipeline)** roadmap for analyzing empathy dimensions using the Interpersonal Reactivity Index (IRI) across three cohort datasets (2023, 2024, 2025).

## 📁 Project Structure

```text
2026-MAP8_IRI_Empat-a/
├── 00_raw/                # Original Excel datasets (2023, 2024, 2025)
├── 01_harmonized/         # Unified CSV files (1-5 scale, properly oriented)
├── 02_eda/                # Exploratory Data Analysis & Cleaning Reports
├── 03_sem/                # Reliability, KMO, Bartlett, and CFA estimates
├── 04_qca/                # fsQCA Truth Tables and configurational solutions
├── 05_clustering/         # Hierarchical Clustering (Ward) profiles & boxplots
├── 06_reports/            # Final Consolidated Manuscript (Word)
├── code/                  # Analysis scripts (R)
├── scripts/               # Processing and reporting scripts (Python)
├── docs/                  # Methodology and instrument documentation
├── main.py                # Master execution pipeline
└── README.md              # Project overview
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.12+**: `pandas`, `numpy`, `semopy`, `factor_analyzer`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `python-docx`, `openpyxl`.
- **R 4.5.1+**: `QCA`, `admisc` (The pipeline automatically handles dependency resolution in R).

### Execution Workflow

The analysis is automated via a two-step process:

1. **Run the Analysis Pipeline**:
   This performs data harmonization, multivariate outlier detection (Mahalanobis Distance), SEM/CFA, Clustering, and fsQCA.
   ```powershell
   python main.py
   ```
   *Note: Ensure your R executable is located at `C:\Program Files\R\R-4.5.1\bin\R.exe` or update the path in `main.py`.*

2. **Generate the Manuscript**:
   This harvests all tables and figures into a formatted Word document.
   ```powershell
   python scripts/generate_word_report.py
   ```
   *Output: `06_reports/Manuscript_Results_Final.docx`*

## 🛠️ Methodological Highlights

- **Advanced Data Cleaning**: Uses **Mahalanobis Distance** ($\chi^2$ threshold, $p < 0.001$) to identify and remove potentially random or inconsistent response patterns. 
- **Scale Harmonization**: Standardizes variables across years into a unified **1–5 scale**, correcting specific reverse-coding inconsistencies (e.g., 2025 FS7/PD13).
- **Comprehensive SEM**: Reports Global KMO, Bartlett’s Sphericity, Cronbach’s Alpha, and standardized CFA loadings.
- **Configurational Complexity**: Uses **fsQCA** to identify equifinal pathways to high empathy, complementing traditional linear models.

## 📝 Documentation
- **Methodology**: Detailed step-by-step logic in `docs/MAP8_IRI_pipeline.md`.
- **Instruments**: Technical comparison of IRI items in `docs/IRI_Instruments.md`.
- **Case Study Blueprint**: Alignment with the draft manuscript in `MAP8_case_study_and_IRI_blueprint.md`.
