# MAP-8 IRI Empathy Research Project

This project implements the **MAP-8 (Modeling and Analysis Pipeline)** roadmap for analyzing empathy dimensions using the Interpersonal Reactivity Index (IRI) across three longitudinal datasets (2023, 2024, 2025).

## 📁 Project Structure

```text
2026-MAP8_IRI_Empat-a/
├── 00_raw/                # Original Excel datasets (2023, 2024, 2025)
├── 01_harmonized/         # Unified CSV files (1-5 scale, properly oriented)
├── 02_eda/                # Exploratory Data Analysis summaries
├── 03_sem/                # SEM/CFA and Reliability output (Python: semopy)
├── 04_qca/                # fsQCA analysis results (R: QCA/admisc)
├── 05_clustering/         # Hierarchical clustering profiles and dendrograms
├── 06_reports/            # Final consolidated executive summaries
├── code/                  # Analysis scripts (R)
├── scripts/               # Processing and analysis scripts (Python)
├── docs/                  # Methodology and instrument documentation
├── main.py                # Master execution script
└── README.md              # Project overview
```

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**: `pandas`, `numpy`, `semopy`, `factor_analyzer`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `python-docx`.
- **R 4.5+**: `QCA`, `admisc`, `jsonlite`, `rlang`.

### Execution Workflow

The project is designed to be run in two main steps:

1. **Analysis Pipeline**: Run all statistical models (Data Prep, SEM, Clustering, QCA).
   ```powershell
   python main.py
   ```
   *Note: Ensure R is installed at `C:\Program Files\R\R-4.5.1\bin\R.exe` for the QCA step.*

2. **Manuscript Generation**: Create the final Word report with tables and figures.
   ```powershell
   python scripts/generate_word_report.py
   ```

## 🛠️ Pipeline Details

1.  **Data Harmonization**: Unifies 2023-2025 datasets into a standard 1-5 scale.
2.  **Psychometric Analysis**: Performs CFA and Reliability checks (Outputs: `03_sem/`).
3.  **Configurational Analysis (fsQCA)**: Identifies pathways to high empathy (Outputs: `04_qca/`).
4.  **Latent Profiling**: Discovers empathy profiles via Clustering (Outputs: `05_clustering/`).
5.  **Reporting**: Generates an executive summary and a publication-ready Word manuscript (Outputs: `06_reports/`).

## 📝 Documentation
Detailed methodology notes are located in `docs/MAP8_IRI_pipeline.md`.
Instrument comparison and wording details are in `docs/IRI_Instruments.md`.
