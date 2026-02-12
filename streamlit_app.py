import sys
import subprocess

if __name__ == "__main__" and "streamlit" not in sys.modules:
    print("\n[!] ERROR: You are trying to run this file with 'python'.")
    print("Please use the following command instead:")
    print("    python -m streamlit run streamlit_app.py\n")
    sys.exit(1)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from semopy import Model, calc_stats
from scipy.stats import chi2
import os

# Set page config
st.set_page_config(page_title="MAP-8 IRI Playground", layout="wide", page_icon="🧬")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #1e3a8a; font-family: 'Inter', sans-serif; }
    .stTabs [data-baseweb="tab-panel"] { background-color: white; padding: 20px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 MAP-8 Empathy Research: Psychometric Playground")
st.markdown("Explore sensitivity, data cleaning thresholds, and latent structures of the IRI dataset dynamically.")

# 1. Data Loading
@st.cache_data
def load_data():
    path = '01_harmonized/df_iri_playground.csv'
    if not os.path.exists(path):
        # Fallback to standard if playground doesn't exist for some reason
        path = '01_harmonized/df_iri_all_harmonized.csv'
        if not os.path.exists(path):
            st.error(f"Data not found. Please run 'python scripts/prepare_playground_data.py' first.")
            return None
    return pd.read_csv(path)

df_raw = load_data()

if df_raw is not None:
    # --- Sidebar Controls ---
    st.sidebar.header("🕹️ Control Panel")
    
    # Cleaning Parameters
    st.sidebar.subheader("Data Cleaning")
    qc_level = st.sidebar.select_slider("Attention Check Strictness", options=["Relaxed", "Standard (Default)", "Strict"], value="Standard (Default)")
    
    md_p_threshold = st.sidebar.slider("Mahalanobis P-value Threshold", 0.0001, 0.05, 0.001, format="%.4f", help="Lower p-value = fewer cases dropped as outliers.")
    
    # Reverse Coding Simulator
    st.sidebar.subheader("Reversal Logic")
    do_reversal = st.sidebar.toggle("Apply Correct Reversal (FS7, PD13)", value=True)
    
    # Dataset Selection
    st.sidebar.subheader("Dataset Selection")
    available_years = sorted(df_raw['year'].unique())
    selected_years = st.sidebar.multiselect(
        "Included Years", 
        options=available_years, 
        default=available_years,
        help="Filter data by year (2023, 2024, 2025) or combinations."
    )
    
    # Feature Selection
    st.sidebar.subheader("Variable Management")
    fs_items = [f"FS{i}" for i in [1, 5, 7, 12, 16, 23, 26]]
    pt_items = [f"PT{i}" for i in [3, 8, 11, 15, 21, 25, 28]]
    ec_items = [f"EC{i}" for i in [2, 4, 9, 14, 18, 20, 22]]
    pd_items = [f"PD{i}" for i in [6, 10, 13, 17, 19, 24, 27]]
    all_all = fs_items + pt_items + ec_items + pd_items
    
    exclude_items = st.sidebar.multiselect("Drop Specific Items", all_all, help="Drop problematic items (e.g. FS7) to check fit improvement.")
    
    active_items = [i for i in all_all if i not in exclude_items]

    # CFA Configuration
    st.sidebar.subheader("CFA Configuration")
    marker_vars = {}
    with st.sidebar.expander("🛠️ Marker Variables (Fixed to 1.0)", expanded=False):
        st.caption("Select which item's loading is fixed to 1.0 to set the scale of the latent variable.")
        for name, items in [('FS', fs_items), ('PT', pt_items), ('EC', ec_items), ('PD', pd_items)]:
            current = [i for i in items if i in active_items]
            if current:
                marker_vars[name] = st.selectbox(f"{name} Marker", options=current, index=0)
            else:
                marker_vars[name] = None

    # --- CFA Model Setup ---
    mod_parts = []
    for name, items in [('FS', fs_items), ('PT', pt_items), ('EC', ec_items), ('PD', pd_items)]:
        current = [i for i in items if i in active_items]
        if current:
            # Reorder current list to put marker variable first (semopy fixes the first item by default)
            marker = marker_vars.get(name)
            if marker and marker in current:
                current.remove(marker)
                current.insert(0, marker)
            mod_parts.append(f"{name} =~ {' + '.join(current)}")
    mod_desc = "\n".join(mod_parts)

    # --- Processing Engine ---
    def process_data(df, qc, p_val, reverse, drops, years=None):
        temp = df.copy()
        
        # 0. Filter by selected years
        if years:
            temp = temp[temp['year'].isin(years)]
            
        # 1. Optional Reversal simulation
        if reverse:
            # Note: The 'all_harmonized' file already has some logic applied. 
            # This playground assumes we tweak on top or reset.
            # In our pipeline FS7/PD13 were reversed in 2025.
            pass # Already harmonized in the CSV we are loading
            
        # 2. QC Filtering
        if qc == "Strict":
            temp = temp[temp['qc_fail_count'] == 0]
        elif qc == "Standard (Default)":
            temp = temp[temp['qc_fail_count'] <= 1]
            
        # 3. Drop missing in active items
        temp = temp.dropna(subset=active_items)
        
        # 4. Mahalanobis Step
        if len(temp) > len(active_items):
            data = temp[active_items]
            mu = data.mean()
            cov = data.cov()
            prec = np.linalg.pinv(cov)
            diff = data - mu
            md = diff.apply(lambda x: np.sqrt(np.dot(np.dot(x, prec), x)), axis=1)
            threshold = np.sqrt(chi2.ppf(1 - p_val, df=len(active_items)))
            temp['is_outlier'] = md > threshold
            temp_clean = temp[~temp['is_outlier']].copy()
        else:
            temp_clean = temp.copy()
            
        return temp_clean

    df_active = process_data(df_raw, qc_level, md_p_threshold, do_reversal, exclude_items, selected_years)

    # --- Dashboard Layout ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Sample Size", len(df_active), delta=f"{len(df_active) - len(df_raw)}")
    
    # Calculate global KMO
    try:
        _, kmo_model = calculate_kmo(df_active[active_items])
        m2.metric("KMO MSA", f"{kmo_model:.3f}")
    except: m2.metric("KMO MSA", "Err")

    # Alpha calculation
    def get_alpha(d):
        if d.empty: return 0
        v = d.var(axis=0, ddof=1)
        tv = d.sum(axis=1).var(ddof=1)
        n = d.shape[1]
        return (n/(n-1)) * (1-(v.sum()/tv))

    # Tabs
    tab0, tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Welcome & Guide", 
        "📊 Correlations & Descriptives", 
        "📉 CFA & Fit", 
        "🧩 Subscale Reliability", 
        "🚀 Cross-Dataset Comparison"
    ])

    with tab0:
        st.header("Welcome to the MAP-8 Psychometric Playground! 🧪")
        st.markdown("""
        This tool is designed to help researchers explore the **Interpersonal Reactivity Index (IRI)** dataset across three years of data collection. 
        Adjust the filters in the sidebar to see how data cleaning decisions impact latent structures and fit.
        """)
        
        col_doc1, col_doc2 = st.columns(2)
        
        with col_doc1:
            st.subheader("🧹 Data Cleaning Logic")
            
            with st.expander("1. Attention Check Strictness", expanded=True):
                st.write("""
                **Why?** Respondents sometimes click through surveys without reading. We use 'Trap Questions' (e.g., *'Select Strongly Agree for this item'*) to detect noise.
                - **Relaxed:** Includes everyone.
                - **Standard (Default):** Allows 1 failure ($QC \le 1$).
                - **Strict:** Only includes perfect responders ($QC = 0$).
                """)
            
            with st.expander("2. Mahalanobis Distance (Outliers)", expanded=True):
                st.write("""
                **Why?** To detect multivariate outliers—patterns of responses that are mathematically 'too far' from the average.
                """)
                st.latex(r"D_M(x) = \sqrt{(x - \mu)^T \Sigma^{-1} (x - \mu)}")
                st.write("""
                **Example:** If someone answers '5' to all Empathic Concern items but '1' to all Personal Distress items in a way that is highly improbable, the distance increases. 
                *Lower p-value threshold = stricter exclusion.*
                """)

        with col_doc2:
            st.subheader("⚙️ Psychometric Controls")
            
            with st.expander("3. Reversal Logic", expanded=True):
                st.write("""
                **Why?** Items like **FS7** (*"I am usually objective when I watch a movie..."*) are reversed because a high score indicates *lower* fantasy engagement. 
                Reversing ensures that all items in a subscale point in the **same psychological direction**, which is critical for valid Alpha ($\alpha$) and CFA results.
                """)
                
            with st.expander("4. Variable Management", expanded=True):
                st.write("""
                **Why?** Some items might be 'noisy' or misunderstood by a specific population. By dropping them, you can observe if the **Model Fit (CFI/TLI)** increases. 
                If dropping an item significantly improves fit, it might be a candidate for permanent removal in future research versions.
                """)

        st.divider()
        st.subheader("🛠️ Map of the Playground")
        st.markdown("""
        - **📊 Correlations:** Visualize how items talk to each other. Look for 'blobs' of color within subscales.
        - **📉 CFA & Fit:** The 'Gold Standard' for validation. Checks if the 4-factor structure actually holds up.
        - **🧩 Reliability:** Check Cronbach's Alpha. If $\alpha < 0.70$, the subscale is considered 'weak'.
        - **🚀 Comparison:** The most powerful tool. See if the model performs better in 2023 vs 2025.
        """)

    with tab1:
        st.subheader("Interactive Correlation Matrix")
        corr_type = st.radio("Analyze:", ["Items", "Subscales"], horizontal=True)
        
        if corr_type == "Items":
            corr = df_active[active_items].corr()
        else:
            # Recompute means for active items
            for name, items in [('FS', fs_items), ('PT', pt_items), ('EC', ec_items), ('PD', pd_items)]:
                current = [i for i in items if i in active_items]
                if current: df_active[f'{name}_dyn'] = df_active[current].mean(axis=1)
            sub_cols = [c for c in df_active.columns if c.endswith('_dyn')]
            corr = df_active[sub_cols].corr()

        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r', range_color=[-1, 1],
                       aspect="auto", title=f"Correlation Heatmap ({corr_type})")
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader(f"📈 Descriptive Statistics ({corr_type})")
        
        if corr_type == "Items":
            stats_df = df_active[active_items].describe().T
            # Add Skew and Kurtosis
            stats_df['skew'] = df_active[active_items].skew()
            stats_df['kurtosis'] = df_active[active_items].kurtosis()
        else:
            sub_cols = [c for c in df_active.columns if c.endswith('_dyn')]
            stats_df = df_active[sub_cols].describe().T
            stats_df['skew'] = df_active[sub_cols].skew()
            stats_df['kurtosis'] = df_active[sub_cols].kurtosis()
            # Clean up index labels for subscales
            stats_df.index = [i.replace('_dyn', '') for i in stats_df.index]

        # Formatting for display
        st.dataframe(stats_df.style.format("{:.3f}"), use_container_width=True)
        st.caption(f"Summary metrics for the currently selected data subset (N={len(df_active)})")

    with tab2:
        st.subheader("Confirmatory Factor Analysis (CFA)")
        st.info("Dynamic CFA using semopy. This may take a few seconds after changing items.")
        
        with st.expander("View Model Specification"):
            st.code(mod_desc)

        if st.button("Run CFA"):
            with st.spinner("Optimizing Latent Model..."):
                try:
                    model = Model(mod_desc)
                    model.fit(df_active)
                    est = model.inspect()
                    stats = calc_stats(model)
                    
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.write("**Core Fit Indices**")
                        # Display key metrics at a glance
                        s = stats.iloc[0]
                        f1, f2 = st.columns(2)
                        f1.metric("CFI", f"{s.get('CFI', 0):.3f}")
                        f2.metric("TLI", f"{s.get('TLI', 0):.3f}")
                        f3, f4 = st.columns(2)
                        f3.metric("RMSEA", f"{s.get('RMSEA', 0):.3f}")
                        f4.metric("SRMR", f"{s.get('SRMR', 0):.3f}" if 'SRMR' in s else "N/A")
                        
                        st.divider()
                        st.write("**All Parameters**")
                        st.dataframe(stats.T, height=400)
                    with c2:
                        st.write("**Standardized Factor Loadings**")
                        # Get standardized loadings if possible
                        try:
                            std_est = model.inspect(std_est=True)
                        except:
                            std_est = est
                        loadings = std_est[std_est['op'] == '~'].rename(columns={'lval': 'Item', 'rval': 'Latent', 'Estimate': 'Loading'})
                        st.dataframe(loadings[['Latent', 'Item', 'Loading', 'p-value']], height=600)
                except Exception as e:
                    st.error(f"SEM Error: {e}")

    with tab3:
        st.subheader("Cronbach's Alpha Sensitivity")
        rel_data = []
        for name, items in [('Fantasy', fs_items), ('Perspective Taking', pt_items), ('Empathic Concern', ec_items), ('Personal Distress', pd_items)]:
            current = [i for i in items if i in active_items]
            if current:
                alpha = get_alpha(df_active[current])
                rel_data.append({"Subscale": name, "Alpha": alpha, "Items Included": len(current)})
        
        st.table(pd.DataFrame(rel_data))
        
        # Item-Total Correlation
        target_sub = st.selectbox("Detailed Sensitivity for:", ["Fantasy", "Perspective Taking", "Empathic Concern", "Personal Distress"])
        sub_map = {"Fantasy": fs_items, "Perspective Taking": pt_items, "Empathic Concern": ec_items, "Personal Distress": pd_items}
        sel_items = [i for i in sub_map[target_sub] if i in active_items]
        
        if sel_items:
            it_corr = {}
            total = df_active[sel_items].sum(axis=1)
            for item in sel_items:
                it_corr[item] = df_active[item].corr(total - df_active[item])
            st.bar_chart(pd.Series(it_corr), color="#1e3a8a")
            st.caption(f"Corrected Item-Total Correlations for {target_sub}")

    with tab4:
        st.subheader("🚀 Cross-Dataset Model Fit Comparison")
        st.markdown("Compare psychometric indicators across individual years and the merged selection.")
        
        if st.button("Generate Comparison Table"):
            results = []
            
            # Helper to run analysis
            def run_quick_cfa(data, label):
                if len(data) < 50: return None
                try:
                    m = Model(mod_desc)
                    m.fit(data)
                    s = calc_stats(m).iloc[0].to_dict()
                    s['Dataset'] = label
                    s['N'] = len(data)
                    return s
                except: return None

            # 1. Individual Years
            for yr in available_years:
                df_yr = process_data(df_raw, qc_level, md_p_threshold, do_reversal, exclude_items, [yr])
                res = run_quick_cfa(df_yr, f"Year {yr}")
                if res: results.append(res)
            
            # 2. Merged Selection
            if len(selected_years) > 1:
                res_merged = run_quick_cfa(df_active, "Merged Selection")
                if res_merged: results.append(res_merged)
            
            if results:
                df_res = pd.DataFrame(results)
                cols_to_show = ['Dataset', 'N', 'CFI', 'TLI', 'RMSEA', 'SRMR']
                existing_cols = [c for c in cols_to_show if c in df_res.columns]
                
                df_display = df_res[existing_cols].set_index('Dataset')
                
                # Safely prepare styling
                format_dict = {c: '{:.3f}' for c in ['CFI', 'TLI', 'RMSEA', 'SRMR'] if c in df_display.columns}
                high_max_cols = [c for c in ['CFI', 'TLI'] if c in df_display.columns]
                high_min_cols = [c for c in ['RMSEA', 'SRMR'] if c in df_display.columns]

                st.write("### Fit Indices Comparison")
                styler = df_display.style.format(format_dict)
                if high_max_cols:
                    styler = styler.highlight_max(subset=high_max_cols, color='#dcfce7')
                if high_min_cols:
                    styler = styler.highlight_min(subset=high_min_cols, color='#dcfce7')
                
                st.dataframe(styler, use_container_width=True)
                
                # Plotly Visualization
                plot_cols = [c for c in ['CFI', 'TLI'] if c in df_res.columns]
                if plot_cols:
                    fig_comp = px.bar(df_res, x='Dataset', y=plot_cols, barmode='group',
                                     title="Comparative Fit (Higher is Better)",
                                     color_discrete_sequence=['#1e3a8a', '#3b82f6'])
                    st.plotly_chart(fig_comp, use_container_width=True)
                
                st.info("💡 **Interpretation:** CFI/TLI > 0.90 are acceptable; > 0.95 good. RMSEA/SRMR < 0.08 acceptable; < 0.05 good.")
                
                # --- NEW: Loadings Comparison ---
                st.divider()
                st.subheader("📈 Cross-Dataset Factor Loadings Comparison")
                st.markdown("Compare how strongly each item loads onto its latent construct across datasets.")
                
                loading_results = []
                
                def get_loadings(data, label):
                    if len(data) < 50: return None
                    try:
                        m = Model(mod_desc)
                        m.fit(data)
                        est = m.inspect(std_est=True)
                        loadings = est[est['op'] == '~'].copy()
                        loadings = loadings.rename(columns={'lval': 'Item', 'rval': 'Latent', 'Estimate': f'Loading_{label}'})
                        return loadings[['Latent', 'Item', f'Loading_{label}']]
                    except: return None

                # Collect loadings for each subset
                all_loadings = []
                
                # 1. Individual Years
                for yr in available_years:
                    df_yr = process_data(df_raw, qc_level, md_p_threshold, do_reversal, exclude_items, [yr])
                    res = get_loadings(df_yr, f"Year {yr}")
                    if res is not None: all_loadings.append(res)
                
                # 2. Merged Selection
                if len(selected_years) > 1:
                    res_merged = get_loadings(df_active, "Merged")
                    if res_merged is not None: all_loadings.append(res_merged)
                
                if all_loadings:
                    # Merge all loading dataframes on Latent and Item
                    df_comp_load = all_loadings[0]
                    for df_next in all_loadings[1:]:
                        df_comp_load = pd.merge(df_comp_load, df_next, on=['Latent', 'Item'], how='outer')
                    
                    # Display Table
                    st.write("#### Standardized Loadings (β)")
                    loading_cols = [c for c in df_comp_load.columns if 'Loading_' in c]
                    st.dataframe(df_comp_load.style.background_gradient(subset=loading_cols, cmap='Blues', vmin=0, vmax=1).format({c: '{:.3f}' for c in loading_cols}), use_container_width=True)
                    
                    # Visualization: Stability of Loadings
                    df_melt = df_comp_load.melt(id_vars=['Latent', 'Item'], value_vars=loading_cols, var_name='Dataset', value_name='Loading')
                    df_melt['Dataset'] = df_melt['Dataset'].str.replace('Loading_', '')
                    
                    fig_load = px.bar(df_melt, x='Item', y='Loading', color='Dataset', barmode='group', 
                                     facet_col='Latent', facet_col_wrap=2,
                                     title="Latent Structure Stability (Comparative Loadings)",
                                     color_discrete_sequence=px.colors.qualitative.Prism)
                    fig_load.update_yaxes(range=[0, 1])
                    fig_load.update_layout(height=800)
                    st.plotly_chart(fig_load, use_container_width=True)
                    
                    st.info("💡 **Insight:** High stability across years indicates 'Measurement Invariance'—the items mean the same thing to different cohorts.")
                else:
                    st.warning("Could not calculate loadings for subsets.")
            else:
                st.error("Insufficient data or model failure in subsets. Ensure enough items are active.")

else:
    st.info("Awaiting pipeline completion to load harmonized data...")
