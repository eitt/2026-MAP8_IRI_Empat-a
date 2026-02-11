import os
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_report():
    print("Generating Word Manuscript...")
    doc = Document()

    # Title
    title = doc.add_heading("MAP-8 Empathy Research: Psychometric and Configurational Analysis Results", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Section 1: Reliability ---
    doc.add_heading("1. Reliability and Inter-scale Correlations", level=1)
    doc.add_paragraph("The internal consistency of the IRI scales was evaluated using Cronbach's Alpha. Preliminary EFA checks (KMO and Bartlett) confirmed the suitability of the data.")
    
    # Load reliability stats from report
    sem_report_path = '03_sem/advanced_sem_detailed_report.txt'
    if os.path.exists(sem_report_path):
        with open(sem_report_path, 'r') as f:
            lines = f.readlines()
            # Extract basic scale stats (FS/PT/EC/PD Alpha)
            stat_lines = [l.strip() for l in lines if l.startswith("--- Scale:")]
            for sl in stat_lines:
                doc.add_paragraph(sl, style='List Bullet')

    # Load correlation table
    corr_path = '03_sem/factor_correlations.csv'
    if os.path.exists(corr_path):
        doc.add_heading("Factor Correlations", level=2)
        df_corr = pd.read_csv(corr_path, index_col=0)
        
        table = doc.add_table(rows=df_corr.shape[0]+1, cols=df_corr.shape[1]+1)
        table.style = 'Table Grid'
        
        # Header
        table.cell(0, 0).text = "Dimension"
        for j, col in enumerate(df_corr.columns):
            table.cell(0, j+1).text = str(col)
        
        # Rows
        for i, row_label in enumerate(df_corr.index):
            table.cell(i+1, 0).text = str(row_label)
            for j, val in enumerate(df_corr.iloc[i]):
                table.cell(i+1, j+1).text = f"{val:.3f}"

    # --- Section 2: CFA ---
    doc.add_heading("2. Confirmatory Factor Analysis (CFA)", level=1)
    doc.add_paragraph("A CFA was performed to validate the multidimensional structure of the IRI.")
    
    # Load CFA Estimates
    cfa_path = '03_sem/cfa_estimates.csv'
    if os.path.exists(cfa_path):
        doc.add_heading("Table: Latent Factor Loadings", level=2)
        df_cfa = pd.read_csv(cfa_path)
        # In semopy, loadings are usually op == '~'
        loadings = df_cfa[df_cfa['op'] == '~']
        
        table = doc.add_table(rows=len(loadings)+1, cols=4)
        table.style = 'Table Grid'
        headers = ["Latent", "Item", "Estimate", "p-value"]
        for i, h in enumerate(headers):
            table.cell(0, i).text = h
            
        for i, (_, row) in enumerate(loadings.iterrows()):
            table.cell(i+1, 0).text = str(row['rval'])
            table.cell(i+1, 1).text = str(row['lval'])
            table.cell(i+1, 2).text = f"{row['Estimate']:.3f}"
            p_val = row['p-value']
            try:
                p_text = "< 0.001" if float(p_val) < 0.001 else f"{float(p_val):.3f}"
            except:
                p_text = str(p_val)
            table.cell(i+1, 3).text = p_text

    # --- Section 3: Clustering ---
    doc.add_heading("3. Empathy Profiles (Hierarchical Clustering)", level=1)
    doc.add_paragraph("Using Ward's method, latent profiles were identified based on subscale means.")
    
    cluster_img = '05_clustering/cluster_profiles.png'
    if os.path.exists(cluster_img):
        doc.add_picture(cluster_img, width=Inches(5.5))
        para = doc.add_paragraph("Figure 1. Empathy profiles identified via Hierarchical Clustering.")
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Section 4: fsQCA ---
    doc.add_heading("4. Configurational Analysis (fsQCA)", level=1)
    doc.add_paragraph("The fsQCA analysis reveals pathways leading to high total empathy.")
    
    qca_report_path = '04_qca/qca_report_r.txt'
    if os.path.exists(qca_report_path):
        with open(qca_report_path, 'r') as f:
            qca_text = f.read()
            if "--- Parsimonious Solution ---" in qca_text:
                sol_part = qca_text.split("--- Parsimonious Solution ---")[1]
                doc.add_heading("Table: Parsimonious Solution for High Total Empathy", level=2)
                # Cleaning up the ASCII table a bit for word
                clean_sol = sol_part.replace("----------------------------------------", "")
                doc.add_paragraph(clean_sol.strip())

    # Save
    os.makedirs('06_reports', exist_ok=True)
    doc_file = '06_reports/Manuscript_Results_Draft.docx'
    doc.save(doc_file)
    print(f"Word Manuscript saved to {doc_file}")

if __name__ == "__main__":
    create_report()
