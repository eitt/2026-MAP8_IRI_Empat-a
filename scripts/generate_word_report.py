import os
import pandas as pd
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_table_header_bg(cell):
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'D9D9D9')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_report():
    print("Generating Comprehensive Word Manuscript...")
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    # Title
    title = doc.add_heading("MAP-8 Case Study: Multidimensional Analysis of Empathy (IRI Replication)", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Section: Methodological Overview ---
    doc.add_heading("1. Methodological Foundations", level=1)
    doc.add_paragraph("This study applies the MAP-8 framework to explore empathy constructs using three complementary methods: "
                   "Confirmatory Factor Analysis (CFA) for linear structures, Fuzzy-Set Qualitative Comparative Analysis (fsQCA) "
                   "for configurational causality, and Hierarchical Clustering for latent profile identification.")

    # --- Section: Sample & Quality Control ---
    doc.add_heading("2. Data Preparation and Quality Control", level=1)
    eda_path = '02_eda/eda_cleaning_report.txt'
    if os.path.exists(eda_path):
        with open(eda_path, 'r') as f:
            doc.add_paragraph(f.read())

    # --- Section: Reliability & CFA ---
    doc.add_heading("3. Psychometric Validation", level=1)
    sem_report_path = '03_sem/advanced_sem_detailed_report.txt'
    if os.path.exists(sem_report_path):
        with open(sem_report_path, 'r') as f:
            content = f.read()
            kmo = re.search(r"Global KMO MSA: ([\d\.]+)", content)
            if kmo: doc.add_paragraph(f"Factorability check: KMO = {kmo.group(1)}.")

    # Reliability Table
    doc.add_heading("Table 1. Reliability Metrics (Cronbach's Alpha)", level=2)
    rel_path = '03_sem/reliability_stats.csv'
    if os.path.exists(rel_path):
        df_rel = pd.read_csv(rel_path)
        table = doc.add_table(rows=len(df_rel)+1, cols=2)
        table.style = 'Table Grid'
        table.cell(0,0).text = "Construct"
        table.cell(0,1).text = "Alpha (\u03B1)"
        for cell in table.rows[0].cells: set_table_header_bg(cell)
        for i, row in df_rel.iterrows():
            table.cell(i+1, 0).text = str(row['Construct'])
            table.cell(i+1, 1).text = f"{row['Alpha']:.3f}"

    # CFA Loadings
    doc.add_heading("4. Confirmatory Factor Analysis Results", level=1)
    cfa_path = '03_sem/cfa_estimates.csv'
    if os.path.exists(cfa_path):
        df_cfa = pd.read_csv(cfa_path)
        loadings = df_cfa[df_cfa['op'] == '~']
        doc.add_heading("Table 2. Standardized Factor Loadings", level=2)
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdrs = ["Latent", "Item", "Estimate", "p-value"]
        for j, h in enumerate(hdrs):
            table.cell(0,j).text = h
            set_table_header_bg(table.cell(0,j))
        for _, r in loadings.iterrows():
            row_cells = table.add_row().cells
            row_cells[0].text = str(r['rval'])
            row_cells[1].text = str(r['lval'])
            row_cells[2].text = f"{r['Estimate']:.3f}"
            p = r['p-value']
            try:
                p_text = "Fixed" if str(p).strip() in ['-', '0.0'] and r['Estimate'] == 1.0 else ("< 0.001" if float(p) < 0.001 else f"{float(p):.3f}")
            except: p_text = str(p)
            row_cells[3].text = p_text

    # --- Section: Clustering ---
    doc.add_heading("5. Heterogeneity and Empathy Profiles", level=1)
    doc.add_paragraph("Hierarchical clustering identified homogeneous subgroups based on empathy dimensions.")
    box_img = '05_clustering/cluster_boxplots.png'
    if os.path.exists(box_img):
        doc.add_picture(box_img, width=Inches(5.0))
        doc.add_paragraph("Figure 1. Comparison of IRI subscale distributions across identified clusters.").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Section: fsQCA ---
    doc.add_heading("6. Configurational Pathways (fsQCA)", level=1)
    qca_path = '04_qca/qca_report_r.txt'
    if os.path.exists(qca_path):
        with open(qca_path, 'r') as f:
            qca_txt = f.read()
            if "--- Parsimonious Solution" in qca_txt:
                sol = qca_txt.split("--- Parsimonious Solution")[1].strip()
                doc.add_heading("Table 3. Parsimonious Solution for High Total Empathy", level=2)
                p = doc.add_paragraph()
                run = p.add_run(sol)
                run.font.name = 'Courier New'
                run.font.size = Pt(9)

    doc.save('06_reports/Manuscript_Results_Final.docx')
    print("Final Word Manuscript generated.")

if __name__ == "__main__":
    create_report()
