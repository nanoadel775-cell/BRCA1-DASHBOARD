<div align="center">
  <h1>🧬 BRCA1 Clinical Profiler Pro</h1>
  <p><i>Next-Generation Genomic Variant Analysis & Simulation Dashboard</i></p>
</div>

<br>

## 📌 Overview
The **BRCA1 Clinical Profiler Pro** is a high-performance, interactive dashboard designed to explore, understand, and visualize specific mutations within the BRCA1 gene. Built with Python and Streamlit, this tool takes raw genomic data and turns it into accessible scientific insight. It features a zero-backend 3D molecular viewer, real-time risk simulations, and advanced Plotly analytics.

*Note: This is an educational project designed to bridge the gap between computer science and genetics.*

## ✨ Key Features
- **🔬 3D Molecular Viewer:** Interactive rendering of the BRCA1 BRCT Domain crystal structure directly within the app using pure JavaScript for lightning-fast loading.
- **🧮 Patient Risk Simulator:** Dynamically calculate adjusted risk metrics based on environmental and hereditary modifiers using a custom algorithm.
- **📊 Advanced Analytics:** Features a custom Glassmorphic Dark UI, Mutational Radar Charts, and Donut distributions.
- **⚡ Low-Resource Optimized:** Leverages Streamlit caching (`@st.cache_data`) and client-side rendering to ensure it runs perfectly on low-end hardware.

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed.

### Installation
1. Clone this repository:
   ```bash
   https://github.com/nanoadel775-cell/BRCA1-DASHBOARD.git
   ```
2. Install the required dependencies:
   ```bash
   pip install streamlit pandas plotly
   ```
3. Run the application locally:
   ```bash
   streamlit run dashboard.py
   ```

## 🧠 About the Developer
This project was built by a 14-year-old student passionate about the intersection of computer science and biology. The core goal of this repository is to understand the **BRCA1 gene** specifically because of its strong connection to highly malignant forms of cancer. By visualizing how structural mutations (like Frameshifts and Missense mutations) affect DNA repair mechanisms, this software models how normal cells transition to malignancy.

---
*For educational and research demonstration purposes only. Not intended for clinical diagnostic use.*
