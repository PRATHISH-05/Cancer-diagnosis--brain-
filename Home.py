"""
Cancer Detection Platform - Simple Landing Page
"""
import streamlit as st

st.set_page_config(
    page_title="Cancer Detection Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
    }
    .hero p {
        font-size: 1rem;
        margin: 0.5rem 0;
        opacity: 0.95;
    }
    
    /* System Cards */
    .system-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .system-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    .system-card h2 {
        margin: 1rem 0 0.5rem 0;
    }
    .system-card p {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Disclaimer */
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 2rem 0;
        color: #856404;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid #e0e0e0;
        margin-top: 3rem;
        color: #999;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Banner
st.markdown("""
<div class="hero">
    <h1>🏥 Cancer Detection Platform</h1>
    <p>AI-Powered Medical Imaging Analysis</p>
    <p style="font-size: 0.95rem; margin-top: 1rem;">Select a system to begin</p>
</div>
""", unsafe_allow_html=True)

# Main Systems
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="system-card">
        <div style="font-size: 3rem;">🧠</div>
        <h2>Brain Tumor Detection</h2>
        <p><strong>Model Accuracy: 93.29%</strong></p>
        <p>Analyze MRI scans to detect Glioma, Meningioma, Pituitary tumors</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Brain System", key="brain_enter", use_container_width=True):
        st.switch_page("pages/Brain_01_Dashboard.py")

with col2:
    st.markdown("""
    <div class="system-card">
        <div style="font-size: 3rem;">🫁</div>
        <h2>Lung Cancer Detection</h2>
        <p><strong>Recall Score: 99.36%</strong></p>
        <p>Analyze CT scans to detect Normal, Benign, and Malignant cases</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Enter Lung System", key="lung_enter", use_container_width=True):
        st.switch_page("pages/Lung_01_Dashboard.py")

st.markdown("---")

# Medical Disclaimer
st.markdown("""
<div class="warning-box">
    <strong>⚠️ Medical Disclaimer</strong><br>
    This platform is for educational purposes only and is NOT a substitute for professional medical diagnosis. 
    Always consult licensed healthcare professionals for any medical concerns.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🏥 Cancer Detection Platform | AI-Powered Medical Imaging Analysis</p>
    <p>© 2026 | Educational & Research Use Only</p>
</div>
""", unsafe_allow_html=True)
