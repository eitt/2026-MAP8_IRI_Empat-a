import os
import subprocess
import sys
import time

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    print(f"[*] {description}...")
    try:
        # Use shell=True for Windows compatibility with R and pip
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description}")
        if result.stdout:
            # Print last few lines of output to keep it clean
            lines = result.stdout.strip().split('\n')
            for line in lines[-5:]:
                print(f"    {line}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed during: {description}")
        print(f"    Error: {e.stderr}")
        return False

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    print_header("MAP-8 IRI RESEARCH: FULL REPRODUCTION PIPELINE")
    print(f"Working Directory: {root_dir}\n")

    # 1. Environment Setup (Python)
    if not run_command("python -m pip install -r requirements.txt", "Updating Python Dependencies"):
        print("Continuing anyway, assuming dependencies might already be met...")

    # 2. Data Preparation
    if not run_command("python scripts/pipeline_step2_data_prep.py", "Step 1/5: Data Harmonization & Outlier Detection"):
        sys.exit(1)

    # 3. Psychometric Analysis (SEM)
    if not run_command("python scripts/pipeline_step4a_advanced_sem.py", "Step 2/5: CB-SEM & Reliability Analysis"):
        print("Warning: SEM failed or had convergence issues. Check 03_sem logs.")

    # 4. Clustering
    if not run_command("python scripts/pipeline_step4c_clustering.py", "Step 3/5: Hierarchical Cluster Analysis"):
        print("Warning: Clustering failed. Check 05_clustering.")

    # 5. configurational Analysis (QCA)
    r_path = r'C:\Program Files\R\R-4.5.1\bin\R.exe'
    if os.path.exists(r_path):
        qca_cmd = f'"{r_path}" --silent --no-echo --no-save --no-restore -f code/pipeline_step4b_qca.R'
        run_command(qca_cmd, "Step 4/5: fsQCA Analysis (R)")
    else:
        print(f"[SKIP] R not found at {r_path}. Skipping configurational analysis.")

    # 6. Technical Summary
    run_command("python scripts/generate_final_report.py", "Consolidating Technical Pipeline MD")

    # 7. Final Academic Manuscript (Word)
    # We use a loop here to wait if Word is open
    for attempt in range(3):
        print(f"[*] Generating Word Manuscript (Attempt {attempt+1}/3)...")
        try:
            result = subprocess.run("python scripts/generate_word_report.py", shell=True, check=True, capture_output=True, text=True)
            print("[SUCCESS] Manuscript generated: 06_reports/Manuscript_Results_Replication.docx")
            break
        except subprocess.CalledProcessError as e:
            if "PermissionError" in e.stdout or "[Errno 13]" in e.stdout:
                print("    [!] ERROR: Manuscript.docx is open in Word. Please close it.")
                if attempt < 2:
                    print("    Waiting 10 seconds for user to close file...")
                    time.sleep(10)
                else:
                    print("    [FAIL] Could not overwrite manuscript. Results saved in logs.")
            else:
                print(f"    [ERROR] {e.stdout}")
                break

    print_header("PIPELINE COMPLETE")
    print("Project successfully replicated from scratch.")
    print("Main Output: 06_reports/Manuscript_Results_Replication.docx")
    print("Analysis Playground: python -m streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()
