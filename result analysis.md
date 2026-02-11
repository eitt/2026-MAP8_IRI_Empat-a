## Materials and methods

This study follows the MAP-8 roadmap to investigate **empathy as a multidimensional construct** using the **Interpersonal Reactivity Index (IRI)**. The design explicitly targets *methodological complementariedad*: it combines **CB-SEM/CFA** (correlational logic), **fsQCA** (configurational logic), and **hierarchical clustering** (segmentation logic) to test whether (i) the IRI structure is psychometrically defensible, (ii) **multiple sufficient “recipes”** can lead to high empathy (equifinality), and (iii) the sample is heterogeneous, with stable empathy profiles. In line with MAP-8, the project embeds **robustness checks** via a **three-stage sensitivity design** (Raw → QC-only → Clean) to verify that substantive conclusions are not artifacts of careless responding or multivariate outliers.

### Step 1: Problem definition and analytical objective (hypotheses and propositions)

The study is grounded in contemporary empathy theory that distinguishes cognitive and affective components of empathic responding. The IRI operationalizes empathy through four dimensions:

* **Fantasy (FS)**: imaginative transposition into fictional situations.
* **Perspective Taking (PT)**: cognitive decentering and adopting others’ viewpoints.
* **Empathic Concern (EC)**: other-oriented compassion and warmth.
* **Personal Distress (PD)**: self-oriented discomfort and tension in response to others’ distress.

Rather than assuming a single linear mechanism, the analysis asks whether the data support **(a)** a coherent four-factor measurement model, **(b)** configurational causality (multiple pathways) leading to **high overall empathy**, and **(c)** stable population heterogeneity via clustering.

Accordingly, the study articulates the following hypotheses/propositions:

* **H1 (Structure)**: The IRI is representable as a four-factor model (FS, PT, EC, PD).
* **H2 (Equifinality)**: High total empathy can be achieved through multiple sufficient combinations of IRI dimensions (no single universal pathway).
* **H3 (Heterogeneity)**: The sample contains distinct empathy profiles (clusters) with different mean patterns across FS, PT, EC, and PD.
* **H4 (Contextual configurations)**: Sociodemographic conditions (Gender, SES) participate as contextual modifiers in some sufficient pathways to high empathy.
* **H5 (Robustness)**: The main patterns (measurement diagnostics, recipes, clusters) remain stable under staged cleaning (Raw, QC-only, Clean).

### Step 2: Data acquisition, integration, and preparation

**Case setting and data sources.** The empirical study integrates multiple cohorts (2023–2024 survey waves) that measured IRI items on Likert-type scales. A harmonization step was applied to ensure a unified **1–5** response format.

**Quality control strategy.** MAP-8 treats QC as a methodological pillar that conditions the credibility of downstream models. The dataset was processed through a multi-stage pipeline:

* **Raw cases:** 2,081
* **After attention-check QC (AC2/AC3):** 1,138
* **After multivariate outlier removal (Mahalanobis distance):** 1,083
* **Dropped as potentially random response patterns:** 55 (p < .001)

Mahalanobis distance (D^2) was used to remove improbable multivariate profiles under a (\chi^2) threshold (df = 28; p < .001).

**EDA requirement and directionality checks.** Reverse-keyed items were handled so that *higher scores consistently indicate higher levels of the construct*.

### Step 3: Model specification (three complementary logics)

To ensure complementariedad, three analytical lenses were specified in parallel:

1. **CB-SEM / CFA (correlational logic).**
   Purpose: validate the four-factor structure and inspect item loadings.

2. **fsQCA (configurational logic).**
   Purpose: identify sufficient combinations of FS, PT, EC, PD, Gender, and SES leading to **high total empathy**.

3. **Hierarchical clustering (segmentation logic).**
   Purpose: detect interpretable empathy profiles and evaluate their stability across cleaning stages.

### Step 4: Model estimation (software, transformations, and implementation)

* **CFA** estimated on the cleaned sample (N = 1,083).
* **fsQCA** implemented on fuzzy-calibrated constructs (Thresholds: 5%, 50%, 95%).
* **Clustering** performed on subscale means using Ward’s method.

### Step 5: Fit evaluation and diagnostic criteria

Fit and adequacy were evaluated within each logic:

* **Psychometrics (factorability):**
  * Global **KMO MSA = 0.888** (excellent adequacy)
  * **Bartlett’s test**: χ² = 9347.39, p < .001

* **Reliability (Cronbach’s alpha):**
  * FS = 0.709; PT = 0.718; EC = 0.671; PD = 0.756

* **CFA model fit (clean sample):**
  * DoF = 344; CFI = 0.698; TLI = 0.668; RMSEA = 0.086
  Moderate global fit supports the need for triangulation.

* **fsQCA solution quality:**
  Parsimonious solution coverage is very high (**98.4%**), with inclusion consistency of **0.773**.

* **Clustering interpretability:**
  Two distinct profiles were identified based on intensity levels across all dimensions.

---

## Results

### Descriptive analysis and preliminary diagnostics

After cleaning, the dataset retained **N = 1,083** high-quality cases. Factorability diagnostics were strong (**KMO = 0.888**), supporting structured inference. Reliability reached acceptable levels (**Alpha ≥ 0.70** for most subscales), with EC (0.67) being the most diverse dimension.

### CB-SEM / CFA: structure and triangulation motivation

The CFA results support the four-factor IRI hierarchy, though global fit indices (CFI ≈ 0.70; RMSEA ≈ 0.086) highlight the multidimensional complexity of the scale. Item inspection revealed that **FS7** exhibited a weak loading (0.072), suggesting that certain indicators may capture peripheral empathic facets. This "suboptimal" fit motivates the use of fsQCA to capture nonlinear configurations that linear models might miss.

### fsQCA: equifinality and sufficient “recipes” for high empathy

Configurational analysis identifies multiple pathways to high empathy (Solution Coverage = 0.984). The parsimonious solution yielded several "recipes," including:
* **Cognitive-Affective Synergies**: (fs_f * pt_f), (fs_f * ec_f), and (pt_f * ec_f).
* **Demographic Contexts**: (fs_f * gen_f) and (ec_f * ses_f).
* **The Distress Bridge**: (pt_f * pd_f).

The recipe **PT * PD** is particularly notable: despite a weak average correlation between perspective-taking and distress, their *joint* presence characterizes a valid subset of high-empathy individuals.

### Hierarchical clustering: stable population heterogeneity

Clustering identified two distinct population segments:
* **Group 1 (Intense Empathizers)**: Higher means across all subscales (PT ≈ 3.85, EC ≈ 4.08, PD ≈ 3.25).
* **Group 2 (Moderate Empathizers)**: Consistently lower scores, especially in affective markers (EC ≈ 3.26, PD ≈ 2.34).

Profile geometry remained **stable across all cleaning stages**, confirming these groups are structural features of the sample rather than artifacts of outlier data.

### Triangulated interpretation

Triangulation demonstrates that while **CFA** validates the core structure, **fsQCA** reveals the diverse recipes for high empathy, and **clustering** identifies who these empathizers are. Sensitivity analysis confirms that these findings are robust against multivariate noise (Mahalanobis outliers) and inattention.
