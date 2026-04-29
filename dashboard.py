import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BRCA1 Analysis", layout="wide")
st.title("🧬 BRCA1 Gene Mutation Dashboard")
st.markdown("### Genomic Variant Analysis for Breast Cancer Research")

data = {
    'Mutation': ['185delAG', '5382insC', 'C61G', 'T1700A', 'R1699Q'],
    'Type': ['Frameshift', 'Insertion', 'Missense', 'Missense', 'Missense'],
    'Risk Level': [0.98, 0.94, 0.88, 0.72, 0.82],
    'Clinical Significance': ['Pathogenic', 'Pathogenic', 'Likely Pathogenic', 'VUS', 'Pathogenic']
}

df = pd.DataFrame(data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Variant Data Table")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Risk Level Visualization")
    fig = px.bar(df, x='Mutation', y='Risk Level', color='Clinical Significance', 
                 title='Risk Impact by Mutation Type', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

st.info("Note: This dashboard is for educational purposes in genomic research.")
