"""
Brain Tumor Detection System - Dashboard
Central hub for brain tumor detection features
"""
import streamlit as st

st.set_page_config(
    page_title="Brain Tumor Detection",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .dashboard-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    .feature-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 5px solid #667eea;
        color: #000;
    }
    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #666;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    .info-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        color: #000;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">🧠 Brain Tumor Detection System</div>
    <div class="dashboard-subtitle">MRI-based Deep Learning Classification</div>
</div>
""", unsafe_allow_html=True)

# Back Button
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("Home.py")

st.markdown("---")

# Statistics
st.markdown("## 📊 System Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">93.29%</div>
        <div class="stat-label">Model Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">92.71%</div>
        <div class="stat-label">Recall Score</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">4</div>
        <div class="stat-label">Tumor Classes</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">CNN</div>
        <div class="stat-label">Model Type</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Features Overview
st.markdown("## 🎯 Available Features")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Medical Information</div>
        <div class="feature-desc">Learn about tumor types, treatments, symptoms, and prognosis</div>
        <p style="margin-top: 1rem; font-size: 0.85rem;">
            <a href="?page=Brain_02_Medical_Info" target="_self" style="text-decoration: none; color: #667eea; font-weight: bold;">
                Open Page →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📚 Medical Info", key="brain_medical", use_container_width=True):
        st.switch_page("pages/Brain_02_Medical_Info.py")

with feat_col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔬</div>
        <div class="feature-title">Test & Detect</div>
        <div class="feature-desc">Upload MRI image and get AI predictions with analysis</div>
        <p style="margin-top: 1rem; font-size: 0.85rem;">
            <a href="?page=Brain_03_Test_Detect" target="_self" style="text-decoration: none; color: #667eea; font-weight: bold;">
                Open Page →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔬 Test & Detect", key="brain_detect", use_container_width=True):
        st.switch_page("pages/Brain_03_Test_Detect.py")

with feat_col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <div class="feature-title">History & Export</div>
        <div class="feature-desc">View all past analyses and export data in multiple formats</div>
        <p style="margin-top: 1rem; font-size: 0.85rem;">
            <a href="?page=Brain_04_History" target="_self" style="text-decoration: none; color: #667eea; font-weight: bold;">
                Open Page →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📋 History", key="brain_history", use_container_width=True):
        st.switch_page("pages/Brain_04_History.py")

st.markdown("---")

# Tumor Classes Information
st.markdown("## 🧬 Detectable Tumor Classes")

tumor_col1, tumor_col2 = st.columns(2)

with tumor_col1:
    st.markdown("""
    **Glioma**
    - Most common malignant brain tumor
    - Arises from glial cells
    - Can be aggressive
    - Requires immediate treatment
    
    **Meningioma**
    - Grows from brain membranes
    - Usually benign (non-cancerous)
    - Slow growth rate
    - Often treatable with surgery
    """)

with tumor_col2:
    st.markdown("""
    **Pituitary Adenoma**
    - Non-cancerous tumor of pituitary gland
    - Can affect hormone production
    - Usually managed medically
    - Sometimes requires surgery
    
    **Normal**
    - Healthy brain MRI scans
    - No tumor presence detected
    - Regular monitoring recommended
    - Normal brain tissue patterns
    """)

st.markdown("---")

# Quick Start Guide
st.markdown("## 🚀 Quick Start Guide")

tabs = st.tabs(["Upload Image", "Understanding Results", "Generate Report", "View History"])

with tabs[0]:
    st.markdown("""
    ### How to Upload and Analyze:
    
    1. **Go to Test & Detect Page** - Click the "Test & Detect" button above
    2. **Upload Your MRI Image**
       - Click "Browse files" button
       - Select JPG, JPEG, or PNG image
       - Image will be automatically resized
    3. **AI Analysis**
       - Model processes the image
       - Analyzes for tumor patterns
       - Generates confidence scores
    4. **View Results**
       - Original image displayed
       - Heatmap visualization shows tumor probability
       - Highlighted regions show detected anomalies
       - Confidence scores for each class
    """)

with tabs[1]:
    st.markdown("""
    ### Understanding Your Results:
    
    **Predictions:**
    - Model returns confidence % for each tumor class
    - Highest score indicates predicted class
    - Scores sum to 100%
    
    **Visualizations:**
    - **Heatmap**: Color coding shows anomaly intensity
      - Red areas = high tumor probability
      - Blue areas = normal tissue
    - **Detected Regions**: Yellow boxes and blue circles mark suspicious areas
    
    **Confidence Scores:**
    - 0-25%: Low probability
    - 25-50%: Moderate probability  
    - 50-75%: High probability
    - 75-100%: Very high probability
    
    ⚠️ **Important**: Always consult medical professionals for diagnosis
    """)

with tabs[2]:
    st.markdown("""
    ### Generating PDF Reports:
    
    After analyzing an image:
    
    1. **Click "Generate PDF Report"** button
    2. **Report includes:**
       - Original uploaded MRI image
       - Heatmap visualization
       - Detected regions overlay
       - Complete prediction scores
       - Confidence percentages
       - Tumor class information
       - Clinical recommendations
       - Analysis timestamp
    3. **Download PDF** using download button
    4. **Share with physicians** for professional review
    
    Reports are created with ReportLab and include professional formatting.
    """)

with tabs[3]:
    st.markdown("""
    ### Using History & Export:
    
    1. **Go to History Page** - Click the "History" button above
    2. **View Your Analyses:**
       - All past detections listed
       - Timestamps for each analysis
       - Confidence scores displayed
       - Detailed prediction breakdown
    3. **Export Data:**
       - **CSV**: Spreadsheet format for analysis
       - **JSON**: Raw data for integration
       - **Text Report**: Summary of all results
    4. **Track Progress:**
       - See total number of analyses
       - Tumor type distribution
       - Average confidence scores
    """)

st.markdown("---")

# Key Features
st.markdown("## ✨ Key Capabilities")

cap_col1, cap_col2, cap_col3 = st.columns(3)

with cap_col1:
    st.markdown("""
    **🎯 High Accuracy**
    - 93.29% accuracy rate
    - Trained on thousands of MRI images
    - Continuous validation
    - Professional-grade model
    """)

with cap_col2:
    st.markdown("""
    **📊 Advanced Visualization**
    - Dual visualization methods
    - Heatmap analysis
    - Region highlighting
    - Confidence charts
    """)

with cap_col3:
    st.markdown("""
    **📄 Professional Reports**
    - PDF generation
    - High-quality images
    - Clinical recommendations
    - Shareable format
    """)

st.markdown("---")

# Information Box
st.markdown("""
<div class="info-box">
    <strong>📌 Important Note:</strong> This system is designed for educational and preliminary screening purposes. 
    It is NOT a substitute for professional medical diagnosis. Always consult qualified radiologists and oncologists 
    for official diagnosis and treatment decisions. Early detection and professional consultation can significantly improve outcomes.
</div>
""", unsafe_allow_html=True)

# Footer Navigation
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    if st.button("← Back to Home", key="footer_back"):
        st.switch_page("Home.py")

with footer_col2:
    if st.button("📚 Medical Info", key="footer_medical"):
        st.switch_page("pages/Brain_02_Medical_Info.py")

with footer_col3:
    if st.button("🔬 Test & Detect", key="footer_detect"):
        st.switch_page("pages/Brain_03_Test_Detect.py")

with footer_col4:
    if st.button("📋 History", key="footer_history"):
        st.switch_page("pages/Brain_04_History.py")
