# MAP-8 Pipeline Execution Summary
Date: 2026-02-10

## 1. Data Preparation and EDA
=== MAP-8 EDA & Cleaning Report ===
Raw cases total: 2081
Cases after Quality Control (AC2/AC3 filtering): 1138
Final cases after Outlier Removal (Mahalanobis Distance): 1083
Dropped as inattentive: 943
Dropped as potentially random: 55


## 2. Measurement Reliability (Step 4A)
Global KMO MSA: 0.888
Bartlett Sphericity: Chi2=9347.39, p=0.000e+00

--- Scale Reliabilities ---
FS: Alpha = 0.709
PT: Alpha = 0.718
EC: Alpha = 0.671
PD: Alpha = 0.756

=== CFA Model Fit ===
       DoF  DoF Baseline         chi2  chi2 p-value  chi2 Baseline       CFI       GFI      AGFI       NFI       TLI     RMSEA         AIC         BIC    LogLik
Value  344           378  3085.171752           0.0    9444.774337  0.697668  0.673346  0.641061  0.673346  0.667787  0.085817  118.302545  427.526941  2.848727

## 3. Empathy Profiles - Clustering (Step 4C)
cluster,FS_mean,PT_mean,EC_mean,PD_mean
1,3.6577946768060836,3.8522542096686583,4.076588810429114,3.2504073872895165
2,2.92212543554007,3.528571428571429,3.2634146341463413,2.3365853658536584


## 4. fsQCA Calibration (Step 4B)
=== fsQCA Analysis Report: _with_md ===
Date: 2026-02-11 16:02:27.470166 
N Analysis Cases: 1067 

--- Necessity Analysis ---
No single necessary condition.

--- Truth Table ---

  OUT: output value
    n: number of cases in configuration
 incl: sufficiency inclusion score
  PRI: proportional reduction in inconsistency

     fs_f pt_f ec_f pd_f gen_f ses_f   OUT    n   incl  PRI  
64    1    1    1    1     1     1      1     28  0.999 0.997
63    1    1    1    1     1     0      1     87  0.998 0.995
48    1    0    1    1     1     1      1     20  0.993 0.982
62    1    1    1    1     0     1      1     18  0.991 0.974
59    1    1    1    0     1     0      1     44  0.990 0.970
61    1    1    1    1     0     0      1     40  0.990 0.964
60    1    1    1    0     1     1      1     14  0.984 0.952
55    1    1    0    1     1     0      1     7   0.984 0.903
47    1    0    1    1     1     0      1     46  0.981 0.943
31    0    1    1    1     1     0      1     25  0.979 0.919
32    0    1    1    1     1     1      1     6   0.975 0.905
30    0    1    1    1     0     1      1     10  0.975 0.854
58    1    1    1    0     0     1      1     23  0.974 0.910
46    1    0    1    1     0     1      1     11  0.970 0.878
45    1    0    1    1     0     0      1     24  0.967 0.825
51    1    1    0    0     1     0      1     6   0.966 0.679
53    1    1    0    1     0     0      1     11  0.961 0.745
54    1    1    0    1     0     1      1     7   0.959 0.768
29    0    1    1    1     0     0      1     10  0.958 0.717
57    1    1    1    0     0     0      1     35  0.957 0.824
43    1    0    1    0     1     0      1     10  0.954 0.687
16    0    0    1    1     1     1      1     6   0.943 0.695
23    0    1    0    1     1     0      1     10  0.941 0.471
27    0    1    1    0     1     0      1     22  0.935 0.636
15    0    0    1    1     1     0      1     17  0.929 0.595
41    1    0    1    0     0     0      1     12  0.915 0.390
39    1    0    0    1     1     0      1     20  0.910 0.541
26    0    1    1    0     0     1      1     10  0.905 0.454
35    1    0    0    0     1     0      1     6   0.899 0.221
40    1    0    0    1     1     1      1     13  0.880 0.563
13    0    0    1    1     0     0      1     11  0.878 0.230
19    0    1    0    0     1     0      1     11  0.875 0.122
49    1    1    0    0     0     0      1     23  0.870 0.349
38    1    0    0    1     0     1      1     7   0.868 0.352
28    0    1    1    0     1     1      1     8   0.867 0.446
50    1    1    0    0     0     1      1     15  0.865 0.443
21    0    1    0    1     0     0      1     11  0.861 0.175
37    1    0    0    1     0     0      1     34  0.847 0.294
25    0    1    1    0     0     0      1     34  0.841 0.236
20    0    1    0    0     1     1      1     5   0.827 0.098
10    0    0    1    0     0     1      1     5   0.818 0.050
 7    0    0    0    1     1     0      1     20  0.812 0.109
 8    0    0    0    1     1     1      0     8   0.800 0.215
 9    0    0    1    0     0     0      0     7   0.790 0.034
34    1    0    0    0     0     1      0     9   0.765 0.054
33    1    0    0    0     0     0      0     18  0.761 0.072
 3    0    0    0    0     1     0      0     16  0.754 0.022
 6    0    0    0    1     0     1      0     7   0.749 0.066
 4    0    0    0    0     1     1      0     6   0.720 0.022
18    0    1    0    0     0     1      0     11  0.713 0.029
17    0    1    0    0     0     0      0     43  0.676 0.022
 5    0    0    0    1     0     0      0     46  0.641 0.023
 2    0    0    0    0     0     1      0     16  0.566 0.001
 1    0    0    0    0     0     0      0     71  0.492 0.002


--- Parsimonious Solution (With Remainders) ---

M1: fs_f*pt_f + fs_f*ec_f + fs_f*pd_f + fs_f*gen_f + pt_f*ec_f + pt_f*pd_f +
    pt_f*gen_f + ec_f*pd_f + ec_f*ses_f + pd_f*gen_f*~ses_f -> iri_total_f

                       inclS   PRI   covS   covU  
------------------------------------------------- 
 1          fs_f*pt_f  0.935  0.869  0.677  0.020 
 2          fs_f*ec_f  0.961  0.923  0.731  0.006 
 3          fs_f*pd_f  0.918  0.835  0.661  0.018 
 4         fs_f*gen_f  0.896  0.833  0.455  0.004 
 5          pt_f*ec_f  0.918  0.839  0.719  0.014 
 6          pt_f*pd_f  0.940  0.869  0.598  0.005 
 7         pt_f*gen_f  0.860  0.775  0.424  0.002 
 8          ec_f*pd_f  0.944  0.886  0.676  0.004 
 9         ec_f*ses_f  0.871  0.781  0.239  0.001 
10  pd_f*gen_f*~ses_f  0.844  0.747  0.318  0.002 
------------------------------------------------- 
                   M1  0.773  0.634  0.984 



## 5. Directory Structure Created
```
00_raw/          - Original Excel files
01_harmonized/   - Cleaned and combined CSVs
02_eda/          - Descriptive statistics
03_sem/          - Reliability and correlations
04_qca/          - Fuzzy set calibration
05_clustering/   - Dendrogram, silhouette, cluster centroids
06_reports/      - This summary report
```

*Execution complete according to MAP8_IRI_pipeline.md guidelines.*
