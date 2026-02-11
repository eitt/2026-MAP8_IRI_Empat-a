import os
import pandas as pd
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_table_header_bg(cell):
    """Set background color of a cell to light gray."""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'D9D9D9') # Light Gray
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_report():
    print("Generating Enhanced Word Manuscript...")
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    # Title
    title = doc.add_heading("MAP-8 Empathy Research: Psychometric and Configurational Analysis Results", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Section 1: Reliability Analysis ---
    doc.add_heading("1. Reliability and Internal Consistency", level=1)
    doc.add_paragraph("The internal consistency of the IRI scales was evaluated using Cronbach's Alpha. Preliminary sampling adequacy was confirmed via KMO and Bartlett tests.")
    
    # Load reliability stats from report
    sem_report_path = '03_sem/advanced_sem_detailed_report.txt'
    if os.path.exists(sem_report_path):
        with open(sem_report_path, 'r') as f:
            content = f.read()
            
            # Extract KMO
            kmo_match = re.search(r"Global KMO MSA: ([\d\.]+)", content)
            if kmo_match:
                doc.add_paragraph(f"Global KMO Measure of Sampling Adequacy: {kmo_match.group(1)} (Excellent).")
            
            # Create Reliability Table
            doc.add_heading("Table 1. Cronbach's Alpha per Subscale", level=2)
            scales = re.findall(r"--- Scale: (\w+) \(Cronbach's Alpha: ([\d\.]+)\) ---", content)
            
            if scales:
                table = doc.add_table(rows=1, cols=2)
                table.style = 'Table Grid'
                hdr_cells = table.rows[0].cells
                hdr_cells[0].text = 'IRI Subscale'
                hdr_cells[1].text = "Cronbach's Alpha (\u03B1)"
                for cell in hdr_cells: set_table_header_bg(cell)
                
                for scale_name, alpha_val in scales:
                    row_cells = table.add_row().cells
                    row_cells[0].text = scale_name
                    row_cells[1].text = alpha_val
    
    # Load correlation table
    corr_path = '03_sem/factor_correlations.csv'
    if os.path.exists(corr_path):
        doc.add_heading("Table 2. Inter-scale Correlations", level=2)
        df_corr = pd.read_csv(corr_path, index_col=0)
        
        table = doc.add_table(rows=df_corr.shape[0]+1, cols=df_corr.shape[1]+1)
        table.style = 'Table Grid'
        
        # Header
        table.cell(0, 0).text = "Dimension"
        set_table_header_bg(table.cell(0, 0))
        for j, col in enumerate(df_corr.columns):
            cell = table.cell(0, j+1)
            cell.text = str(col)
            set_table_header_bg(cell)
        
        # Rows
        for i, row_label in enumerate(df_corr.index):
            table.cell(i+1, 0).text = str(row_label)
            for j, val in enumerate(df_corr.iloc[i]):
                table.cell(i+1, j+1).text = f"{val:.3f}"

    # --- Section 2: Confirmatory Factor Analysis ---
    doc.add_heading("2. Confirmatory Factor Analysis (CFA)", level=1)
    doc.add_paragraph("A CFA was performed using semopy to validate the multidimensional structure of the IRI.")
    
    # Extract Fit Indices
    if os.path.exists(sem_report_path):
        with open(sem_report_path, 'r') as f:
            content = f.read()
            indices_match = re.search(r"CFI\s+GFI\s+AGFI\s+NFI\s+TLI\s+RMSEA\nValue\s+[\d\.]+\s+[\d\.]+\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)", content)
            if indices_match:
                doc.add_paragraph(f"Model Fit Indices: CFI = {indices_match.group(3)}, TLI = {indices_match.group(5)}, RMSEA = {indices_match.group(6)}.")

    # Load CFA Estimates
    cfa_path = '03_sem/cfa_estimates.csv'
    if os.path.exists(cfa_path):
        doc.add_heading("Table 3. Latent Factor Loadings", level=2)
        df_cfa = pd.read_csv(cfa_path)
        loadings = df_cfa[df_cfa['op'] == '~']
        
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Latent Variable"
        hdr_cells[1].text = "Item"
        hdr_cells[2].text = "Standardized Estimate"
        hdr_cells[3].text = "p-value"
        for cell in hdr_cells: set_table_header_bg(cell)
            
        for _, row in loadings.iterrows():
            row_cells = table.add_row().cells
            row_cells[0].text = str(row['rval'])
            row_cells[1].text = str(row['lval'])
            row_cells[2].text = f"{row['Estimate']:.3f}"
            p_val = row['p-value']
            try:
                if str(p_val).strip() == '-':
                    p_text = "Fixed"
                else:
                    p_text = "< 0.001" if float(p_val) < 0.001 else f"{float(p_val):.3f}"
            except (ValueError, TypeError):
                p_text = str(p_val)
            row_cells[3].text = p_text

    # --- Section 3: Empathy Profiles (Clustering) ---
    doc.add_heading("3. Empathy Profiles (Clustering Analysis)", level=1)
    doc.add_paragraph("Hierarchical clustering (Ward's method) identified distinct empathy profiles among the study participants.")
    
    cluster_img = '05_clustering/cluster_profiles.png'
    if os.path.exists(cluster_img):
        doc.add_picture(cluster_img, width=Inches(5.0))
        para = doc.add_paragraph("Figure 1. Identified empathy profiles based on IRI subscale means.")
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Section 4: Configurational Analysis (fsQCA) ---
    doc.add_heading("4. Configurational Analysis (fsQCA)", level=1)
    doc.add_paragraph("Configurational analysis identifies pathways to high empathy (equifinality).")
    
    qca_report_path = '04_qca/qca_report_r.txt'
    if os.path.exists(qca_report_path):
        with open(qca_report_path, 'r') as f:
            qca_text = f.read()
            
            # Extract Truth Table
            if "--- Truth Table ---" in qca_text:
                doc.add_heading("Table 4. Truth Table Overview", level=2)
                tt_part = qca_text.split("--- Truth Table ---")[1].split("---")[0].strip()
                # Use a monospace font for ASCII tables if possible, otherwise just a paragraph
                p = doc.add_paragraph()
                r = p.add_run(tt_part)
                r.font.name = 'Courier New'
                r.font.size = Pt(8)

            # Extract Parsimonious Solution Tables
            if "--- Parsimonious Solution (With Remainders) ---" in qca_text:
                doc.add_heading("Table 5. Parsimonious Solution Configurations", level=2)
                sol_part = qca_text.split("--- Parsimonious Solution (With Remainders) ---")[1].strip()
                p = doc.add_paragraph()
                r = p.add_run(sol_part)
                r.font.name = 'Courier New'
                r.font.size = Pt(9)

    # Save
    os.makedirs('06_reports', exist_ok=True)
    doc_file = '06_reports/Manuscript_Results_Draft.docx'
    doc.save(doc_file)
    print(f"Enhanced Word Manuscript generated successfully: {doc_file}")

if __name__ == "__main__":
    create_report()

