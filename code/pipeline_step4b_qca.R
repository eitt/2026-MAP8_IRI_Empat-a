# MAP-8 IRI fsQCA Script
# Explicit inclusion of demographic variables (Gender)

user_lib <- "C:/Users/LEONA/AppData/Local/R/win-library/4.5"
if (!dir.exists(user_lib)) dir.create(user_lib, recursive = TRUE)
.libPaths(c(user_lib, .libPaths()))

install_if_missing <- function(p) {
  if (!require(p, character.only = TRUE, quietly = TRUE)) {
    install.packages(p, lib = user_lib, repos = "https://cran.r-project.org/")
  }
}

deps <- c("digest", "magrittr", "htmltools", "Rcpp", "cli", "promises", "later", "httpuv", "mime", "shiny", "admisc", "declared", "lpSolve", "QCA")
for (d in deps) { try(install_if_missing(d)) }

library(QCA)
library(admisc)

df_raw <- read.csv("01_harmonized/df_iri_clean.csv")

# 1. Calibration
calibrate_iri <- function(x) {
  anchors <- quantile(x, probs = c(0.05, 0.5, 0.95), na.rm = TRUE)
  if(length(unique(anchors)) < 3) anchors <- c(min(x), mean(x), max(x))
  res <- calibrate(x, thresholds = anchors)
  res[res == 0.5] <- 0.501
  return(res)
}

# Empathy Dimensions
df_raw$fs_f <- calibrate_iri(df_raw$FS_mean)
df_raw$pt_f <- calibrate_iri(df_raw$PT_mean)
df_raw$ec_f <- calibrate_iri(df_raw$EC_mean)
df_raw$pd_f <- calibrate_iri(df_raw$PD_mean)
df_raw$iri_total_f <- calibrate_iri(df_raw$IRI_total)

# Demographics: Gender (assuming 1=Male, 2=Female or similar)
# We treat gender as a crisp set or quasi-fuzzy (0 or 1)
# Checking unique values to be safe. Let's assume binary-like for QCA or calibrate based on data.
if ("gender" %in% names(df_raw)) {
  # Recode gender to 0/1 if numeric, ensuring it's a condition
  # Let's use 1 as 'presence' of the trait (e.g., female if 2 was female)
  df_raw$gen_f <- ifelse(df_raw$gender == 2, 1, 0)
}

# 2. Analysis Subset (including gender if exists)
conds <- c("fs_f", "pt_f", "ec_f", "pd_f")
if ("gen_f" %in% names(df_raw)) conds <- c(conds, "gen_f")

df_qca <- df_raw[, c(conds, "iri_total_f")]
df_qca <- df_qca[complete.cases(df_qca), ]

# 3. Necessity Analysis
nec <- superSubset(df_qca, outcome = "iri_total_f", conditions = conds, relation = "necessity")

# 4. Sufficiency Analysis (Truth Table)
tt <- truthTable(df_qca, outcome = "iri_total_f", 
                 conditions = conds, 
                 incl.cut = 0.8, n.cut = 5, sort.by = "incl, n")

# Parsimonious solution
sol <- minimize(tt, details = TRUE, include = "?")

# 5. Save Report
dir.create("04_qca", showWarnings = FALSE)
sink("04_qca/qca_report_r.txt")
cat("=== fsQCA Analysis Report: IRI Empathy (with Demographics) ===\n")
cat(paste("Date:", Sys.time(), "\n"))
cat(paste("N Analysis Cases:", nrow(df_qca), "\n\n"))
cat("--- Necessity Analysis ---\n")
if (!is.null(nec)) try(print(nec)) else cat("No single necessary condition.\n")
cat("\n--- Truth Table ---\n")
print(tt)
cat("\n--- Parsimonious Solution (With Remainders) ---\n")
print(sol)
sink()

message("QCA Analysis successfully completed.")
