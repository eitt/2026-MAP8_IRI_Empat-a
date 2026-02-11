# MAP-8 Pipeline Execution Summary
Date: 2026-02-10

## 1. Data Preparation and EDA
=== MAP-8 EDA & Cleaning Report ===
Note: 2025 dataset excluded per user request.

Raw cases total: 2081
Raw cases by year:
year
2023    1110
2024     971

Cases after Quality Control (AC2/AC3 filtering): 1138
Cases after Outlier Removal (Mahalanobis Distance): 1083
Dropped as potentially random: 55

Final Cleaned Sample by year:
year
2023    1062
2024      21

=== Descriptive Statistics (Cleaned Sample) ===
           FS_mean      PT_mean      EC_mean      PD_mean    IRI_total
count  1083.000000  1083.000000  1083.000000  1083.000000  1083.000000
mean      3.100778     3.607176     3.460889     2.558502     3.181836
std       0.706600     0.621080     0.622542     0.659950     0.438926
min       1.428571     1.428571     1.285714     1.000000     1.821429
25%       2.571429     3.142857     3.000000     2.142857     2.892857
50%       3.000000     3.571429     3.428571     2.571429     3.142857
75%       3.571429     4.000000     3.857143     3.000000     3.464286
max       5.000000     5.000000     5.000000     4.428571     4.500000

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

=== Factor Loadings ===
    lval op rval  Estimate  Std. Err    z-value   p-value
0    FS1  ~   FS  1.000000         -          -         -
1    FS5  ~   FS  1.563764  0.119979  13.033673       0.0
2    FS7  ~   FS  0.071578  0.067313   1.063354  0.287621
3   FS12  ~   FS  0.407608  0.073151   5.572175       0.0
4   FS16  ~   FS  1.705609   0.12676  13.455401       0.0
5   FS23  ~   FS  1.688855  0.122113  13.830276       0.0
6   FS26  ~   FS  1.629182   0.12089  13.476606       0.0
7    PT3  ~   PT  1.000000         -          -         -
8    PT8  ~   PT  1.986766  0.250421   7.933709       0.0
9   PT11  ~   PT  2.683988  0.328562   8.168904       0.0
10  PT15  ~   PT  0.822804  0.169667   4.849514  0.000001
11  PT21  ~   PT  2.254133  0.279954   8.051805       0.0
12  PT25  ~   PT  2.316856  0.293699   7.888543       0.0
13  PT28  ~   PT  2.380786  0.299723   7.943302       0.0
14   EC2  ~   EC  1.000000         -          -         -
15   EC4  ~   EC  0.233110  0.056545   4.122569  0.000037
16   EC9  ~   EC  0.847688  0.063872  13.271621       0.0
17  EC14  ~   EC  0.323601  0.056495   5.727953       0.0
18  EC18  ~   EC  0.256307  0.050356   5.089849       0.0
19  EC20  ~   EC  1.272293  0.081116  15.684946       0.0
20  EC22  ~   EC  1.443579  0.088366  16.336373       0.0
21   PD6  ~   PD  1.000000         -          -         -
22  PD10  ~   PD  0.835425  0.050086  16.679825       0.0
23  PD13  ~   PD  0.447334  0.048915   9.145105       0.0
24  PD17  ~   PD  1.153548   0.05693  20.262584       0.0
25  PD19  ~   PD  0.273195  0.042607   6.411987       0.0
26  PD24  ~   PD  0.964069  0.048251  19.980494       0.0
27  PD27  ~   PD  0.674298  0.040274  16.742714       0.0

## 3. Empathy Profiles - Clustering (Step 4C)
cluster,FS_mean,PT_mean,EC_mean,PD_mean
1,3.6577946768060836,3.8522542096686583,4.076588810429114,3.2504073872895165
2,2.92212543554007,3.528571428571429,3.2634146341463413,2.3365853658536584


## 4. fsQCA Calibration (Step 4B)
=== fsQCA Analysis Report: IRI Empathy (with Demographics) ===
Date: 2026-02-11 09:23:45.910546 
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
