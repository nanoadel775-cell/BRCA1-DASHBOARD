import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit.components.v1 as components
import base64

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRCA1 Clinical Profiler Pro",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Optimization: Cache Data ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load core dataset enriched with metadata for the advanced features.
    Maintains the original 5 rows but adds descriptive columns for simulation."""
    data = {
        'Mutation': ['185delAG', '5382insC', 'C61G', 'T1700A', 'R1699Q'],
        'Type': ['Frameshift', 'Insertion', 'Missense', 'Missense', 'Missense'],
        'Base Risk Level': [0.98, 0.94, 0.88, 0.72, 0.82],
        'Clinical Significance': ['Pathogenic', 'Pathogenic', 'Likely Pathogenic', 'VUS', 'Pathogenic'],
        'Discovery Year': [1995, 1996, 1998, 2005, 2001],
        'Global Freq (%)': [0.080, 0.052, 0.011, 0.125, 0.034],
        'Summary': [
            "A well-known founder mutation, highly prevalent in the Ashkenazi Jewish population, causing a truncated, non-functional BRCA1 protein.",
            "A common insertion resulting in a frameshift. Strongly associated with hereditary breast and ovarian cancer.",
            "Missense mutation in the RING domain affecting BARD1 binding, strongly disrupting tumor suppression.",
            "Variant of Uncertain Significance. While it alters an amino acid, clincal impact remains actively debated.",
            "Pathogenic missense mutation in the BRCT domain, disrupting critical phosphoprotein binding and DNA repair mechanics."
        ],
        'Sequence Context': [
            "A G A <span style='color:#f87171;'>[DEL AG]</span> T C A",
            "C G G <span style='color:#f87171;'>[INS C]</span> T C G",
            "T G C <span style='color:#f87171;'>[C->G]</span> A T T",
            "C G A <span style='color:#f87171;'>[T->A]</span> C C G",
            "A T G <span style='color:#f87171;'>[G->A]</span> C A T"
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# ── Global CSS & Theming ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stDataFrame {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: linear-gradient(145deg, #07090e 0%, #0d1220 50%, #151b2b 100%) !important;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    height: 55px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    padding: 10px 12px;
    font-size: 0.95rem;
    font-weight: 600;
    color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom: 2px solid #38bdf8 !important;
}

/* Custom Cards */
.info-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    margin-bottom: 16px;
}
.info-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.sequence-strip {
    font-family: 'Courier New', monospace;
    font-size: 1.5rem;
    letter-spacing: 6px;
    color: #94a3b8;
    background: #07090e;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    border: 1px dashed rgba(148, 163, 184, 0.3);
    margin: 10px 0;
}

hr { border-color: rgba(255,255,255,0.05) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Configurations ───────────────────────────────────────────────────
st.sidebar.markdown("## ⚙️ Control Panel")
selected_mutation_idx = st.sidebar.selectbox("🎯 Target Mutation Context", range(len(df)), format_func=lambda i: df['Mutation'][i])
target_data = df.iloc[selected_mutation_idx]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧮 Patient Modifiers (Simulator)")
sim_age = st.sidebar.slider("Patient Age", 20, 80, 45, help="Increases relative risk multiplier over time.")
sim_fhx = st.sidebar.checkbox("Family History (1st Degree)", value=True)
sim_env = st.sidebar.selectbox("Environmental Risk Factor", ["Low", "Moderate", "High"], index=1)

# Simulator Math
multiplier = 1.0 + ((sim_age - 45) * 0.005)
if sim_fhx: multiplier += 0.15
if sim_env == "Moderate": multiplier += 0.05
elif sim_env == "High": multiplier += 0.15

simulated_risk = min(target_data['Base Risk Level'] * multiplier, 0.999)

def generate_csv():
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="brca1_variants.csv" style="display:inline-block; padding:8px 16px; background:#38bdf8; color:#0f172a; text-decoration:none; border-radius:6px; font-weight:bold;">📥 Download Full CSV</a>'

st.sidebar.markdown("---")
st.sidebar.markdown(generate_csv(), unsafe_allow_html=True)

# ── Plotly Base Config ───────────────────────────────────────────────────────
PLOTLY_LAYOUT_BASE = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8"),
    margin=dict(l=20, r=20, t=30, b=20)
)
SIG_COLORS = {"Pathogenic": "#f87171", "Likely Pathogenic": "#fb923c", "VUS": "#a78bfa"}

# ── Main Header ─────────────────────────────────────────────────────────────
st.markdown("<h1 style='color: #f8fafc; font-weight: 800; font-size: 2.8rem; margin-bottom:0;'>🧬 BRCA1 Insight Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: 0;'>Next-Generation Genomic Variant Analysis & Simulation</p>", unsafe_allow_html=True)

# ── Application Tabs ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "🧮 Simulator", 
    "🔬 3D View",
    "📚 Context"
])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Variants", len(df))
    c2.metric("Mean Risk", f"{df['Base Risk Level'].mean():.2f}")
    c3.metric("Pathogenic", len(df[df['Clinical Significance'] == 'Pathogenic']))
    c4.metric("Top Freq", df.iloc[df['Global Freq (%)'].idxmax()]['Mutation'])
    
    col_a, col_b = st.columns([1.5, 1])
    with col_a:
        st.markdown("### 📋 Variant Baseline Registry")
        st.dataframe(
            df[['Mutation', 'Type', 'Clinical Significance', 'Base Risk Level', 'Discovery Year']],
            use_container_width=True, hide_index=True,
            column_config={
                "Base Risk Level": st.column_config.ProgressColumn("Base Risk Level", format="%.2f", min_value=0, max_value=1.0)
            }
        )
    with col_b:
        st.markdown("### 🎯 Mutational Risk Radar")
        fig_radar = go.Figure(go.Scatterpolar(
            r=df['Base Risk Level'].tolist() + [df['Base Risk Level'].iloc[0]],
            theta=df['Mutation'].tolist() + [df['Mutation'].iloc[0]],
            fill='toself', line=dict(color='#38bdf8'), fillcolor='rgba(56, 189, 248, 0.15)'
        ))
        fig_radar.update_layout(**PLOTLY_LAYOUT_BASE, height=280, polar=dict(radialaxis=dict(visible=True, range=[0,1], gridcolor="rgba(148,163,184,0.1)")))
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

with tab2:
    st.markdown(f"### Simulation Targets: **{target_data['Mutation']}**")
    
    metrics_cols = st.columns(3)
    metrics_cols[0].metric("Base Population Risk", f"{target_data['Base Risk Level']:.3f}", "Baseline", delta_color="off")
    metrics_cols[1].metric("Applied Multipliers", f"x{multiplier:.2f}", "+ Patient Factors", delta_color="inverse")
    metrics_cols[2].metric("Adjusted Patient Risk", f"{simulated_risk:.3f}", f"{(simulated_risk - target_data['Base Risk Level']):.3f} vs Base", delta_color="inverse")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=simulated_risk * 100,
        title={'text': "Simulated Lifetime Risk (%)", 'font': {'size': 20, 'color': '#e2e8f0'}},
        delta={'reference': target_data['Base Risk Level'] * 100, 'increasing': {'color': "#f87171"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#38bdf8"},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range': [0, 50], 'color': "rgba(52, 211, 153, 0.1)"},
                {'range': [50, 75], 'color': "rgba(251, 146, 60, 0.1)"},
                {'range': [75, 100], 'color': "rgba(248, 113, 113, 0.1)"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig_gauge.update_layout(**PLOTLY_LAYOUT_BASE, height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)

with tab3:
    st.markdown(f"### Structural Impact Context: **{target_data['Mutation']}**")
    st.info("💡 **Interactive Element**: Below is an interactive 3D model of the BRCA1 BRCT Domain (PDB: 1JNX). Use your mouse to rotate, scroll to zoom.")
    
    # Render py3Dmol securely via HTML block - zero python backend overhead!
    html_3d = """
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <div id="mol-container" style="width: 100%; height: 450px; border-radius: 12px; background: #070a10; overflow: hidden; border: 1px solid rgba(56, 189, 248, 0.2);"></div>
    <script>
        let viewer = $3Dmol.createViewer("mol-container", {backgroundColor: '#070a10'});
        $3Dmol.download("pdb:1JNX", viewer, {}, function() {
            viewer.setStyle({cartoon: {color: 'spectrum'}});
            viewer.zoomTo();
            viewer.render();
            viewer.zoom(0.8);
        });
    </script>
    """
    components.html(html_3d, height=450)
    
    st.markdown(f"#### Local Sequence Alignment")
    st.markdown(f"<div class='sequence-strip'>5' ... {target_data['Sequence Context']} ... 3'</div>", unsafe_allow_html=True)


with tab4:
    col_x, col_y = st.columns([1, 1])
    
    with col_x:
        st.markdown(f"<div class='info-card'><div class='info-title'>🧬 AI Functional Summary</div><p style='color: #e2e8f0; line-height: 1.6;'>{target_data['Summary']}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-card'><div class='info-title'>🕒 Historical Context</div><p style='color: #cbd5e1;'>This specific variant was first categorized heavily in clinical literature around the year <b>{target_data['Discovery Year']}</b>. Its structural classification remains firmly categorized as <b>{target_data['Type']}</b>, contributing heavily to its <b>{target_data['Clinical Significance']}</b> status.</p></div>", unsafe_allow_html=True)

    with col_y:
        st.markdown("### Global Population Pathogenicity")
        fig_bar = go.Figure(go.Bar(
            x=df['Mutation'], y=df['Global Freq (%)'], 
            marker_color=[SIG_COLORS.get(s, "#38bdf8") for s in df['Clinical Significance']]
        ))
        fig_bar.update_layout(
            **PLOTLY_LAYOUT_BASE, height=280, 
            yaxis_title="Allele Frequency (%)",
            xaxis_title="Variant Profile"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# Footer
st.markdown("<hr><p style='text-align: center; color: #475569; font-size: 0.8rem;'>🔬 Built for Research Validation • Optimized on Python & Streamlit • v2.0 Next-Gen</p>", unsafe_allow_html=True)
