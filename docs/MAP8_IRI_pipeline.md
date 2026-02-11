# MAP-8 Implementation Guide for Empathy Research Using the IRI (Spanish versions)

This document operationalizes the **MAP-8 (Modeling and Analysis Pipeline)** roadmap for an empathy project using the **Interpersonal Reactivity Index (IRI)** across two datasets (2023, 2024). It is designed to be used as a practical *analysis playbook* with explicit preprocessing, EDA, harmonization, and method-specific pipelines (CB-SEM, fsQCA, and Hierarchical Clustering). Note: 2025 is currently excluded.

**Primary inputs**
- MAP-8 methodology source: *2. Draft.docx* fileciteturn1file12  
- IRI datasets:
  - *1_2023_data_IRI.xlsx*
  - *2_2024_data_IRI.xlsx*
  - (3_2025_data_IRI.xlsx is excluded)

---

## 1) Conceptual context: IRI as a multidimensional empathy instrument (Spanish)

The IRI conceptualizes empathy as a **multidimensional construct** with four subscales that jointly represent both **cognitive** and **affective** components:

- **Cognitive empathy**
  - **Perspective Taking (PT)**: tendency to adopt others’ viewpoints.
  - **Fantasy (FS)**: tendency to imaginatively transpose oneself into fictional situations.

- **Affective empathy**
  - **Empathic Concern (EC)**: other-oriented feelings of compassion and concern.
  - **Personal Distress (PD)**: self-oriented discomfort and anxiety when witnessing others’ distress.

In your project, the same item identifiers appear with **two Spanish wordings**:
- **Arenas-Estévez et al. (2021)** wording
- **Rangel et al. (2024)** wording

**Key point for comparability:** treat item IDs as the anchor (FS1, EC2, PT3, …, PT28). Wording differences matter for interpretation, but measurement alignment is enforced via item IDs, response scale, and invariance checks (MAP-8 Step 8).

---

## 2) Data inventory and variable harmonization

### 2.1 Datasets (as provided)
**2023 dataset** (*1_2023_data_IRI.xlsx*):  
- Items use **no “E” prefix** (e.g., `FS1`, `EC2`, `PT3`, `PD6`, …).
- Includes **precomputed scores**: `IRITOTAL`, `PT`, `FS`, `EC`, `PD`, and composites.

**2024 dataset** (*2_2024_data_IRI.xlsx*):  
- Items use **“E” prefix** (e.g., `EFS1`, `EEC2`, `EPT3`, `EPD6`, …).
- Contains **attention checks** `AC1–AC4` and `attention_check`.
- Contains subscale totals: `IRI_pt`, `IRI_fs`, `IRI_ec`, `IRI_pd`.

**2025 dataset** (*3_2025_data_IRI.xlsx*):  
- Items use `iri_` prefix (e.g., `iri_FS1`, `iri_EC2`, …).
- Attention checks are encoded as **expected-response variables**, e.g.:
  - `iri_ac1_rta5` (expected response = 5)
  - `iri_ac2_rta1` (expected response = 1)
- Includes `iri_commitment` and more granular demographic labels.

---

### 2.2 Canonical naming scheme (recommended)
Create a unified dataframe with **canonical column names**:

**Identifiers**
- `respondent_id` (from `ID` or `iri_id`)
- `year` (2023/2024/2025)

**Demographics (minimum)**
- `age`
- `gender` (harmonize from `gender`/`sex`)
- `ses` (harmonize from `economic_level` or `socioeconomic_level`)
- Optional: `faculty` / `academic_unit`, `school_location`, `public_school`, `university_student`

**IRI items**
- `FS1, EC2, PT3, …, PT28` (numeric Likert)
- Attention checks in canonical form:
  - `AC1_commitment`
  - `AC2_check_expected5`
  - `AC3_check_expected1`
  - (Optional) `AC4` if used in 2024

---

### 2.3 Recoding and Unification (Critical decision based on EDA)

Based on inspection of item ranges and internal consistency, the following unification rule must be applied during Step 2 of the pipeline:

| Dataset | Item scale | Reverse-keyed items already recoded? | Action                                    |
| ------- | ---------: | ------------------------------------ | ----------------------------------------- |
| 2023    |        0–4 | Yes                                  | Add +1 to all items; Do **not** reverse |
| 2024    |        1–5 | Yes                                  | Do **not** reverse again                  |
| 2025    |        1–5 | Partial                              | Reverse **FS7** and **PD13** only (Formula: 6-x) |

---

## 3) Orientation and scoring rules

### 3.1 Unification Logic
1. **Scale Range Unification**: Convert all datasets to a 1–5 scale.
   - For 2023: `x_new = x + 1`
2. **Selective Reversal (2025 only)**:
   - Reverse `iri_FS7` and `iri_PD13` using `x_rev = 6 - x`.
   - All other items across all years appear to be stored in their correct orientation (higher = more empathy).

### 3.2 Subscale computation (recommended approach)
Compute subscales as **means** (not sums) using the unified 1–5 items. Since the orientation is corrected during harmonization, use the standard item names:

- `FS_mean` = mean(FS1, FS5, FS7, FS12, FS16, FS23, FS26)
- `PT_mean` = mean(PT3, PT8, PT11, PT15, PT21, PT25, PT28)
- `EC_mean` = mean(EC2, EC4, EC9, EC14, EC18, EC20, EC22)
- `PD_mean` = mean(PD6, PD10, PD13, PD17, PD19, PD24, PD27)

Optional composites:
- `IRI_total` = mean(FS_mean, PT_mean, EC_mean, PD_mean)

### 3.3 Attention checks and data quality gating
Because the datasets include quality-control items (AC1–AC3 and variants), define an explicit **screening policy**:

- **Commitment request (AC1):** may be informational (do not automatically exclude unless the protocol defines it).
- **AC2 expected response = 5:** exclude if response ≠ 5.
- **AC3 expected response = 1:** exclude if response ≠ 1.
- If multiple checks exist (e.g., 2024 also has AC4/`attention_check`), define a rule such as:
  - *Exclude if ≥1 attention check fails* (strict), or
  - *Exclude if ≥2 attention checks fail* (lenient).

Record two variables for transparency:
- `attention_fail_count`
- `included_after_qc` (boolean)

---

## 4) MAP-8 pipeline tailored to your multi-dataset IRI analysis

The MAP-8 roadmap defines eight sequential steps: **Hypothesis Definition, Data Acquisition/Preparation, Model Specification, Model Estimation, Fit Evaluation, Model Interpretation, Report Writing, and Validation/Replication.** fileciteturn1file12

Below is a concrete, implementation-ready version for your IRI datasets.

---

### Step 1 — Hypothesis definition
**Goal:** articulate a theory-driven set of hypotheses about empathy dimensions and outcomes.

**Minimum deliverables**
1. **Conceptual model**: define FS, PT, EC, PD as latent variables (or observed composites if needed).
2. **Outcomes (Y)**: specify the primary dependent variable(s). Examples:
   - Prosocial intention/behavior (if present)
   - Academic or well-being indicators (if present)
   - Group/classification targets (if used)
3. **Controls**: age, gender, SES, academic unit, cohort year.

**Example hypothesis families**
- H1 (measurement): IRI retains a four-factor structure in Spanish across years.
- H2 (structural): cognitive empathy (PT, FS) predicts outcome Y net of affective empathy (EC, PD).
- H3 (configurational): multiple empathy profiles (high EC + high PT; high PD + low PT; etc.) can lead to the same outcome (equifinality).
- H4 (segmentation): clusters differ in mean empathy subscales and in demographic composition.

---

### Step 2 — Data acquisition and preparation
**Goal:** standardize, clean, and harmonize data; run EDA; create analysis-ready datasets.

**Pipeline**
1. **Load each dataset** and add `year`.
2. **Rename columns** to canonical names (Section 2.2–2.3).
3. **Enforce data types**: Likert items numeric; demographics standardized.
4. **EDA (mandatory because orientation can differ):**
   - Missingness per variable, per year.
   - Response distributions (skewness, floor/ceiling).
   - Inconsistent coding (e.g., “sex” vs “gender”; different SES levels).
   - Outliers in age.
5. **Reverse-code items** (Section 3.1).
6. **Compute subscales** (Section 3.2).
7. **Quality-control filtering** using attention checks (Section 3.3).
8. **Create analysis datasets**:
   - `df_clean` (post-QC)
   - `df_sem` (complete cases for SEM, or prepared for robust estimators)
   - `df_qca` (calibration-ready)
   - `df_cluster` (scaled features for clustering)

**Documentation**
- Maintain a **data dictionary** with:
  - original column name → canonical name
  - coding, valid ranges
  - reverse-key indicator
  - missingness rate
  - any transformations

---

### Step 3 — Model specification
**Goal:** choose and formalize the complementary models: CB-SEM, fsQCA, and clustering.

#### 3A) CB-SEM specification
- **Measurement model:** four latent variables (FS, PT, EC, PD) each measured by its items.
- **Structural model:** paths from empathy factors to outcome(s) and covariates.
- If outcomes are not available yet, start with:
  - CFA (confirmatory factor analysis) + invariance tests.

**Estimator note:** Likert items are ordinal. Prefer robust estimators suitable for ordinal indicators (e.g., WLSMV in SEM software that supports it). If using covariance-based SEM with ML, justify and apply robust corrections.

#### 3B) fsQCA specification
- Define:
  - **Conditions** (e.g., high PT, high EC, low PD) and demographics (optional).
  - **Outcome**: the substantive outcome Y, or a derived classification (e.g., high overall empathy).

Because “positive orientation” may differ across constructs, calibration must be transparent (Step 4).

#### 3C) Clustering specification
- Features:
  - Usually the **four subscale means** (FS_mean, PT_mean, EC_mean, PD_mean).
  - Optionally include demographics if segmentation is intended (but keep interpretability).
- Choose hierarchical clustering (HCA) if you want dendrogram interpretability and comparability with MAP-8.

---

### Step 4 — Model estimation
**Goal:** estimate parameters for each method.

#### 4A) CB-SEM estimation
- Fit CFA first; then full SEM.
- Report:
  - loadings, reliability (omega/CR), AVE where relevant
  - factor correlations and discriminant validity checks
  - structural path coefficients with SE/CI

#### 4B) fsQCA calibration and solution
- **Calibration choices must be justified**:
  - Quantile-based (e.g., 5th / 50th / 95th percentiles) is common.
  - Mean-based can be used, but explain why.
- Decide whether high scores represent set membership (“high empathic concern”) or membership in “low personal distress” (requires inverted condition).
- Produce:
  - necessity analysis
  - truth table
  - intermediate solution (and conservative solution if needed)
  - report consistency and coverage for each configuration

#### 4C) Clustering estimation
- Standardize features (z-scores) before distance computation.
- Evaluate cluster solutions:
  - elbow / silhouette / gap (as available)
  - dendrogram cut stability
- Save:
  - cluster labels
  - cluster centroids/means per subscale
  - cluster sizes per year

---

### Step 5 — Fit evaluation
**Goal:** ensure model adequacy, diagnose problems, and iterate responsibly.

#### SEM fit
Report multiple indices (not only one):
- χ² (with caution), CFI/TLI, RMSEA, SRMR  
Interpret conservatively; use modification indices sparingly and theoretically.

#### fsQCA fit
- **Consistency thresholds** (often ≥0.80) and PRI consistency.
- Robustness checks:
  - alternative calibration anchors
  - alternative frequency thresholds for truth table
  - alternative outcome definitions

#### Clustering fit
- Internal validity:
  - silhouette score trends
  - within/between variance patterns
- Practical validity:
  - interpretability of clusters as empathy profiles
  - stability across years

---

### Step 6 — Model interpretation
**Goal:** translate outputs into substantive conclusions about empathy, profiles, and mechanisms.

**Integration logic (MAP-8 principle)**
- Use **SEM** to test theory-driven linear relations and measurement quality.
- Use **fsQCA** to reveal **equifinal pathways** (multiple empathy “recipes” leading to the same outcome).
- Use **clustering** to identify **latent profiles**, then compare:
  - profile prevalence across years
  - profile differences in outcomes (if available)
  - demographic composition differences

A practical integration pattern:
1. CFA/SEM establishes that FS/PT/EC/PD are measured reliably.
2. Clustering produces empathy profiles (e.g., “high EC–high PT”, “high PD”, etc.).
3. fsQCA explains how combinations (including “low PD”) relate to outcomes within or across clusters.

---

### Step 7 — Report writing (structure template)
**Recommended section flow**
1. Introduction (empathy, IRI, Spanish adaptations, why multi-method)
2. Method
   - Samples (by year), measures (IRI + attention checks)
   - Data harmonization and EDA (transparent)
   - MAP-8 roadmap description (brief; then operational steps)
3. Results
   - EDA + descriptives
   - CFA/SEM (measurement then structural)
   - Clustering profiles
   - fsQCA solutions
   - Triangulated interpretation (how results converge/diverge)
4. Discussion
   - theoretical implications (cognitive vs affective empathy roles)
   - methodological value of MAP-8 in psychometric/behavioral research
   - limitations (wording differences, sampling, invariance, attention filtering)
5. Conclusion and future work

---

### Step 8 — Validation and replication
**Goal:** demonstrate robustness and generalizability.

Minimum validation set:
- **Measurement invariance across years** (configural → metric → scalar where feasible).
- **Sensitivity analyses**
  - include/exclude borderline attention-check cases
  - compare scoring via mean vs sum
  - compare treating items as ordinal vs continuous in SEM
- **Out-of-sample checks**
  - fit SEM on 2023+2024 and test on 2025 (if feasible)
  - replicate fsQCA solutions with alternative calibrations
- **Cluster stability**
  - bootstrap or subsample stability checks
  - compare cluster centroids across years

---

## 5) Recommended outputs (what to save for reproducibility)
Create a project folder with:
- `00_raw/` (original xlsx)
- `01_harmonized/`
  - `df_iri_harmonized.csv`
  - `data_dictionary.csv`
- `02_eda/`
  - missingness tables, descriptives, distribution plots
- `03_sem/`
  - model syntax, fit indices, parameter tables
- `04_qca/`
  - calibration rules, truth tables, solutions
- `05_clustering/`
  - cluster solution diagnostics, labels, centroids
- `06_reports/`
  - manuscript tables/figures, appendix for reproducibility

---

## 6) Notes to align with your datasets
- 2023 already contains computed IRI totals; recompute from items after harmonization to ensure scoring consistency across years.
- 2024/2025 attention checks are explicit and should be used to define a consistent inclusion rule across all years.
- Because item wording differs (Arenas-Estévez vs Rangel), prioritize **invariance testing** before making strong longitudinal claims.

---

*End of document.*
