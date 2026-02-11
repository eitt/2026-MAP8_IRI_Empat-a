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
- **Python 3.10+**: `pandas`, `numpy`, `semopy`, `factor_analyzer`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`.
- **R 4.5+**: `QCA`, `admisc`, `jsonlite`, `rlang`.

### Execution
To run the entire pipeline from data cleaning to final reporting, execute the master script:

```powershell
python main.py
```

## 🛠️ Pipeline Details

1.  **Data Harmonization**: Unifies 2023 (0-4 scale) and 2024-2025 (1-5 scale) into a single standard 1-5 scale. Corrects specific reverse-coding inconsistencies in the 2025 data (`FS7`, `PD13`).
2.  **Psychometric Analysis**: Performs CFA and Cronbach's Alpha reliability checks.
3.  **Configurational Analysis (fsQCA)**: Identifies combinations of empathy dimensions (and demographics) that lead to high total empathy.
4.  **Latent Profiling**: Uses Hierarchical Clustering (Ward's method) to discover natural empathy profiles within the population.

## 📝 Documentation
Detailed methodology notes are located in `docs/MAP8_IRI_pipeline.md`.
Instrument comparison and wording details are in `docs/IRI_Instruments.md`.
