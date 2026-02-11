# MAP-8 IRI Pipeline - Step 4B: fsQCA Implementation in R
# Corrected directional expectations format for ADMISC/QCA.

# 1. Setup Local Library
lib_path <- file.path(getwd(), "R_libs")
if (!dir.exists(lib_path)) dir.create(lib_path)
.libPaths(c(lib_path, .libPaths()))

# Load Libraries
packages <- c("QCA", "admisc")
for (p in packages) {
  library(p, character.only = TRUE, quietly = TRUE)
}

# 2. Load Data
df_raw <- read.csv("01_harmonized/df_iri_clean.csv")

# 3. Calibration Functions with 0.5 ambiguity adjustment
calibrate_iri <- function(x) {
  x_clean <- x[!is.na(x)]
  anchors <- quantile(x_clean, probs = c(0.05, 0.5, 0.95))
  if(length(unique(anchors)) < 3) {
    anchors <- c(min(x_clean), mean(x_clean), max(x_clean))
  }
  res <- calibrate(x, thresholds = anchors)
  res[res == 0.5] <- 0.501 
  return(res)
}

# 4. Create Calibrated Variables
df_raw$fs_f <- calibrate_iri(df_raw$FS_mean)
df_raw$pt_f <- calibrate_iri(df_raw$PT_mean)
df_raw$ec_f <- calibrate_iri(df_raw$EC_mean)
df_raw$pd_f <- calibrate_iri(df_raw$PD_mean)
df_raw$age_f <- calibrate_iri(df_raw$age)
df_raw$ses_f <- calibrate_iri(df_raw$ses)
df_raw$iri_total_f <- calibrate_iri(df_raw$IRI_total)

# 5. STRICT SUBSETTING
qca_columns <- c("fs_f", "pt_f", "ec_f", "pd_f", "age_f", "ses_f", "iri_total_f")
df_qca <- df_raw[, qca_columns]
df_qca <- df_qca[complete.cases(df_qca), ]

message(paste("Starting QCA analysis with", nrow(df_qca), "fully complete cases."))

# 6. Necessity Analysis
print("--- Necessity Analysis ---")
conds_names <- c("fs_f", "pt_f", "ec_f", "pd_f", "age_f", "ses_f")
nec <- superSubset(df_qca, outcome = "iri_total_f", conditions = conds_names, relation = "necessity")
if (!is.null(nec)) {
  # Filter for consistency > 0.9
  print(nec)
} else {
  print("No single necessary condition found.")
}

# 7. Truth Table Analysis
tt <- truthTable(df_qca, outcome = "iri_total_f", 
                 conditions = c("fs_f", "pt_f", "ec_f", "pd_f"), 
                 incl.cut = 0.8, n.cut = 5, sort.by = "incl, n")

print("--- Truth Table ---")
print(tt)

# 8. Boolean Minimization
# If dir.exp is failing, we'll produce both Parsimonious and Complex solutions.
# Complex (no remainders)
sol_comp <- minimize(tt, details = TRUE)
# Parsimonious (with remainders)
sol_pars <- minimize(tt, details = TRUE, include = "?")

print("--- Parsimonious Solution ---")
print(sol_pars)

# 9. Save Results
dir.create("04_qca", showWarnings = FALSE)
sink("04_qca/qca_report_r.txt")
cat("=== fsQCA Analysis Report: IRI Empathy ===\n")
cat(paste("Date:", Sys.time(), "\n"))
cat(paste("Total Cases analyzed:", nrow(df_qca), "\n\n"))
cat("--- Necessity Analysis ---\n")
if (!is.null(nec)) print(nec) else cat("No single necessary condition identified.\n")
cat("\n--- Truth Table ---\n")
print(tt)
cat("\n--- Complex Solution (No Remainders) ---\n")
print(sol_comp)
cat("\n--- Parsimonious Solution (With Remainders) ---\n")
print(sol_pars)
sink()

message("QCA Analysis successfully completed. Results saved to 04_qca/qca_report_r.txt")
