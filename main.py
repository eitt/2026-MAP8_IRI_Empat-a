import os
import subprocess

def run_script(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {cmd}: {result.stderr}")
    else:
        print(result.stdout)
    return result.returncode

def main():
    # 1. Data Prep
    print("Step 1: Data Preparation...")
    run_script("python scripts/pipeline_step2_data_prep.py")

    # 2. SEM / Reliability
    print("Step 2: SEM & Reliability Analysis...")
    run_script("python scripts/pipeline_step4a_advanced_sem.py")

    # 3. Clustering
    print("Step 3: Hierarchical Clustering...")
    run_script("python scripts/pipeline_step4c_clustering.py")

    # 4. QCA (Requires R)
    print("Step 4: fsQCA Analysis (R)...")
    r_path = r'C:\Program Files\R\R-4.5.1\bin\R.exe'
    if os.path.exists(r_path):
        run_script(f'"{r_path}" --silent --no-echo --no-save --no-restore -f code/pipeline_step4b_qca.R')
    else:
        print("R not found at specified path. Skipping QCA execution via master script.")

    # 5. Final Report
    print("Step 5: Generating Final Report...")
    run_script("python scripts/generate_final_report.py")

if __name__ == "__main__":
    main()
