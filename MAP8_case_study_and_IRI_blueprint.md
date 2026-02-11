# MAP-8 Case Study in the Draft Manuscript and an IRI-Based Replication Blueprint

This document has two purposes:

1. **Describe the MAP-8 case study implemented in _2. Draft.docx_** (telework dataset), including the constructs, hypotheses, and the concrete outputs (graphs/tables) used across the **eight MAP-8 steps**.
2. **Provide a step-by-step blueprint to reproduce an analogous MAP-8 case study using the IRI datasets (2023–2024)**, emphasizing **methodological complementariedad** (CB-SEM + fsQCA + Hierarchical Clustering). Note: 2025 is excluded.

Source: *2. Draft.docx* fileciteturn1file12

---

## Part A — What the Draft Manuscript Implements (the Telework Case Study)

### Case study overview (context + constructs)
The draft applies MAP-8 to a case study in a **teleworking environment** (COVID-19 period), conducted at a **public university in Colombia**. The study models relationships among three organizational behavior constructs:

- **Affective Commitment (AC)**  
- **Organizational Compatibility (OC)**  
- **Job Satisfaction (JS)**  

The goal is to illustrate methodological complementariedad by combining:

- **CB-SEM** (confirmatory, correlational/structural testing),
- **fsQCA** (configurational causality, equifinality),
- **HCA** / hierarchical clustering (segmentation into homogeneous profiles).

---

## A1) MAP-8 Step-by-step Implementation in the Draft

### Step 1 — Hypothesis Definition
The draft defines five hypotheses to cover both correlational and configurational logic:

- **H1:** AC is directly associated with JS.  
- **H2:** AC is directly associated with OC.  
- **H3:** OC is a direct antecedent of JS.  
- **H4:** Equifinality: multiple configurations can lead to outcomes in telework.  
- **H5:** Heterogeneity: the sample includes distinct clusters with different levels of AC, OC, JS.

**What this step produces (deliverables):**
- A conceptual model linking AC → OC → JS (with AC also → JS).
- A clear bridge between **linear hypotheses (H1–H3)** and **configurational/segmentation hypotheses (H4–H5)**.

---

### Step 2 — Data Acquisition and Preparation
The draft describes:
- The study setting (telework during 2020–2021).
- A survey-based dataset (employees: professors, administrative staff, support staff).
- Cleaning and preparation aligned with SEM assumptions and downstream QCA/clustering needs.

**EDA + data quality checks highlighted:**
- Descriptives (means per construct indicators).
- Reliability and factorability: **Cronbach’s alpha**, **KMO**, and **Bartlett’s test**.

**Key quantitative diagnostics reported (as written in the draft):**
- Cronbach’s alpha = **0.92**
- KMO = **0.88**
- Bartlett’s χ² = **2302.58**, p < 0.001

**Graph output referenced:**
- **Figure 2:** Correlation heatmap between variables.

---

### Step 3 — Model Specification
The draft specifies a three-method design:

- **CB-SEM**: a structural model to test H1–H3.
- **fsQCA**: to test equifinality (H4).
- **HCA**: to detect heterogeneous profiles (H5).

It positions the three methods as complementary:
- SEM tests theory-driven linear relations.
- fsQCA maps causal complexity and multiple sufficient paths.
- Clustering detects subgroups where patterns differ.

**Table output referenced:**
- **Table 1:** Comparison of CB-SEM, fsQCA, and clustering (foundations, requirements, strengths/limits, applications).

---

### Step 4 — Model Estimation
The draft estimates each method as follows:

- **CB-SEM**: model developed to test H1–H3 (reported parameter count: **47**).
- **fsQCA**: constructs synthesized (averaged) to enable set calibration and necessity analysis.
- **HCA**: clustering performed on AC/OC/JS scores.

**Graph output referenced:**
- **Figure 3:** Variables synthesized into constructs (construct-building diagram).

---

### Step 5 — Fit Evaluation
The draft explicitly reports SEM fit as suboptimal and motivates revision/iteration.

**Fit indices reported (as written in the draft):**
- χ² significant (p < 0.05)
- CFI = **0.820**
- TLI/NNFI = **0.798**
- RMSEA = **0.105**
- SRMR = **0.089**
- AGFI = **0.702**
- AIC = **8509.29**
- BIC = **8657.49**

This step illustrates MAP-8’s practical logic: **diagnose fit**, decide whether to respecify, and then rely on complementary methods (fsQCA, clustering) to preserve interpretive value even when SEM fit is imperfect.

---

### Step 6 — Model Interpretation
The draft reports three method-specific interpretations:

- **CB-SEM:** linear association testing (with an emphasis on fit limitations and need for revision).
- **fsQCA:** necessity analysis; AC emerges as a necessary antecedent for OC and JS (draft reports inclN and covN values).
- **HCA:** segmentation into clusters with meaningful patterns.

**Graph output referenced:**
- **Figure 4:** Boxplot by cluster (AC/OC/JS distributions across clusters).

---

### Step 7 — Report Writing
The draft frames results into a “Results and discussion” narrative and emphasizes:
- methodological triangulation,
- complementarity and interpretability,
- practical guidance for management research.

Deliverables include:
- EDA narrative + Figure 2,
- SEM fit table (indices),
- QCA necessity/configuration outputs (textual + possibly tables),
- clustering profile descriptions + Figure 4.

---

### Step 8 — Validation and Replication
The draft includes a dedicated validation section:
- cross-validating fsQCA solutions with alternative calibration thresholds,
- testing alternative distance metrics in HCA,
- structuring the roadmap to facilitate reuse in similar contexts.

This provides the template for replication logic you want to implement with IRI: **robustness checks + sensitivity analyses + cross-year comparability**.

---

## A2) What Graphs and Tables the Draft Uses (inventory)

### Figures
- **Figure 1:** MAP-8 roadmap diagram.
- **Figure 2:** Correlation heatmap between variables.
- **Figure 3:** Construct synthesis diagram (observed items → constructs).
- **Figure 4:** Boxplots by cluster (profile comparison).

### Tables
- **Table 1:** Comparative table (CB-SEM vs fsQCA vs clustering): assumptions, outputs, strengths, and use cases.
- SEM fit indices table (embedded as text but should be a formal table in replication).
- Reliability/factorability table (α, KMO, Bartlett).

---

---

## Part B — Blueprint to Generate an IRI MAP-8 Case Study (2023–2025)

This section translates the telework case structure into an **IRI-based empathy case study**, maintaining the same MAP-8 logic and the same complementarity principle.

### Core constructs (IRI)
- **FS** (Fantasy)
- **PT** (Perspective Taking)
- **EC** (Empathic Concern)
- **PD** (Personal Distress)

Your three Excel datasets include IRI items and demographics; the blueprint assumes a harmonized dataframe `df_iri_all` with a `year` indicator (2023/2024/2025).

---

## B1) MAP-8 Steps for the IRI Case Study

### Step 1 — Hypothesis Definition (IRI version)
Define hypotheses that explicitly span the three analytic logics:

**Correlational (SEM-like) hypotheses**
- H1: PT and EC positively covary as “prosocial empathy” components.
- H2: PD shows weaker or negative association with PT (emotional overarousal vs cognitive regulation).
- H3: Demographics (age, gender, SES) predict empathy dimensions.

**Configurational (fsQCA) hypothesis**
- H4: Multiple empathy “recipes” (e.g., high EC & high PT; high FS & high EC; low PD & high PT) can lead to a high outcome (e.g., “high overall empathy” or any external criterion you later include).

**Segmentation (HCA) hypothesis**
- H5: The population is heterogeneous; clusters reflect distinct empathy profiles (e.g., “high EC–high PT”, “high PD”, “high FS”, “balanced-high”, etc.).

**Deliverables**
- A conceptual diagram: FS/PT/EC/PD (+ controls) and target outcome definition.

---

### Step 2 — Data Acquisition and Preparation (IRI version; must include EDA)
Because you have **three cohorts** and **different coding conventions**, Step 2 must be explicit and auditable.

**Mandatory operations**
1. Harmonize item names to canonical IDs (FS1…PT28).
2. Confirm item ranges (2023 is 0–4; 2024/2025 are 1–5).
3. Apply reverse coding only where needed (based on your earlier QC findings).
4. Compute subscale scores as **means** (FS_mean, PT_mean, EC_mean, PD_mean).
5. Apply attention-check filtering consistently across years.
6. EDA outputs:
   - missingness heatmap,
   - distribution plots per subscale (by year),
   - correlation heatmap (items and/or subscales),
   - descriptive table (mean, SD, min/max, skewness) by year.

**IRI replication of draft outputs**
- **Figure 2 (IRI):** correlation heatmap among subscales (and optionally items).
- **Reliability table:** α/ω per subscale + KMO + Bartlett (if factor analysis/CFA planned).

---

### Step 3 — Model Specification (IRI version)
Specify the three complementary methods, explicitly linked to your hypotheses:

1. **CB-SEM / CFA-first strategy**
   - Measurement: four-factor CFA (FS/PT/EC/PD with item indicators).
   - Structural: optional regressions from demographics to latent factors.

2. **fsQCA**
   - Conditions: calibrated membership in high PT, high EC, high FS, low PD (note: “low PD” is a distinct condition).
   - Outcome: “high empathy” (composite), or an external criterion if present.

3. **HCA**
   - Features: FS_mean, PT_mean, EC_mean, PD_mean (standardized).
   - Output: cluster labels (empathy profiles) + profile interpretation.

**Table to include (replicating Table 1 logic)**
- A compact “method comparison and role” table specifically for the IRI case.

---

### Step 4 — Model Estimation (IRI version)
**SEM**
- Estimate CFA; if acceptable, proceed to SEM with covariates.
- Treat items as ordinal where possible (robust estimators).

**fsQCA**
- Calibrate sets using transparent anchors (quantiles or theory-based cutpoints).
- Run necessity + sufficiency; produce intermediate solution.
- Provide consistency/coverage per configuration.

**HCA**
- Compute distances (e.g., Ward linkage on Euclidean; test sensitivity).
- Select k using silhouette/elbow + interpretability.
- Save centroids and within-cluster distributions.

**Figure 3 (IRI analogue)**
- Diagram: items → FS/PT/EC/PD → composite outcome and/or clusters.

---

### Step 5 — Fit Evaluation (IRI version)
**SEM**
- Fit indices (CFI/TLI/RMSEA/SRMR) and loading quality.
- If multi-year comparisons are intended: measurement invariance checks.

**fsQCA**
- Consistency thresholds; PRI consistency.
- Robustness: alternative calibration anchors; frequency thresholds.

**Clustering**
- Silhouette + stability (bootstrap/subsample).
- Compare k solutions; interpretability as empathy profiles.

---

### Step 6 — Model Interpretation (IRI version; integration logic)
Interpret each method separately and then triangulate:

- SEM clarifies whether the four-factor empathy structure holds and how dimensions relate linearly.
- fsQCA explains how **combinations** of empathy dimensions produce “high empathy” (equifinality).
- HCA yields actionable empathy profiles; then compare profiles by year and demographics.

**Figure 4 (IRI analogue)**
- Boxplots of FS/PT/EC/PD by cluster; optionally stratified by year.

---

### Step 7 — Report Writing (IRI version; recommended Results flow)
1. Sample description by year + QC exclusions (attention checks).
2. EDA + descriptives + Figure 2 heatmap.
3. Reliability/factorability table.
4. CFA/SEM results (measurement first).
5. Clustering profiles + Figure 4 boxplots + profile narrative.
6. fsQCA solutions table + interpretation.
7. Triangulation: where methods converge/diverge and what that means for empathy inference.

---

### Step 8 — Validation and Replication (IRI version; cross-year robustness)
Minimum validation package:
- **Cross-year invariance testing** (configural → metric → scalar where feasible).
- Sensitivity analyses:
  - alternative reverse-coding decisions where borderline,
  - alternative calibration anchors for fsQCA,
  - alternative distance/linkage for HCA.
- Replication logic:
  - train on 2023–2024, validate on 2025 (or reverse).
  - compare cluster centroids year-by-year.

---

## B2) Recommended Tables and Figures for the IRI Case Study (mirroring the draft)

### Figures
- **Figure 1:** MAP-8 roadmap (reuse as framework figure).
- **Figure 2:** Correlation heatmap (subscales and/or items).
- **Figure 3:** Construct synthesis diagram (items → subscales → composite outcome).
- **Figure 4:** Boxplots by cluster (FS/PT/EC/PD distributions).

### Tables
- **Table 1 (adapted):** Role of CB-SEM, fsQCA, HCA in empathy research (assumptions + outputs).
- **Table 2:** Descriptive statistics by year (FS/PT/EC/PD, demographics).
- **Table 3:** Reliability + factorability (α/ω, KMO, Bartlett).
- **Table 4:** SEM fit indices + standardized loadings summary.
- **Table 5:** fsQCA solutions (configurations, consistency, coverage).
- **Table 6:** Cluster profiles (centroids, sizes, demographic composition).

---

## B3) Operational checkpoints (to keep complementariedad coherent)
1. Ensure **measurement quality first** (CFA/reliability) before strong substantive claims.
2. Use **fsQCA** to explain **equifinality** (multiple empathy pathways).
3. Use **HCA** to identify **profiles** and then interpret SEM/QCA differences across profiles.
4. Keep a **reproducibility log**: coding conventions, recoding rules, QC rules, and sensitivity variants.

---

*End of document.*
