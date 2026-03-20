"""
Medical Information about Lung Cancer
"""
import streamlit as st

st.set_page_config(page_title="Lung Cancer Medical Info", page_icon="🫁", layout="wide")

st.markdown("""
<style>
    .medical-header {
        color: #FF6B6B;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .tumor-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border-left: 5px solid #FF6B6B;
    }
    .stat-box {
        padding: 1rem;
        background: linear-gradient(135deg, #FF6B6B 0%, #FFA500 100%);
        color: white;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="medical-header">🫁 Lung Cancer Medical Information</h1>', unsafe_allow_html=True)

# Back Button
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("pages/Lung_01_Dashboard.py")

# Overview
st.header("📊 Overview")
st.markdown("""
Lung cancer is a leading cause of cancer death worldwide. It develops when abnormal cells grow in the lungs 
and can spread to other parts of the body. Early detection is crucial for better treatment outcomes.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h3>~2.2M</h3>
        <p>New cases annually</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h3>~1.8M</h3>
        <p>Annual deaths</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <h3>3 Types</h3>
        <p>Detected here</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <h3>CT Scan</h3>
        <p>Primary screening</p>
    </div>
    """, unsafe_allow_html=True)

# Lung Cancer Types
st.header("🔍 Lung Cancer Types & Classifications")

st.markdown("""
<div class="tumor-card">
    <h3>✅ Normal Lungs</h3>
    <p><b>Description:</b> Healthy lung tissue with no nodules or abnormalities<br>
    <b>Appearance:</b> Clear air-filled lungs with normal vasculature<br>
    <b>Significance:</b> No cancer detected<br>
    <b>Follow-up:</b> Regular screening recommended based on risk factors<br>
    <b>Prognosis:</b> Excellent - no immediate intervention needed
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tumor-card">
    <h3>⚪ Benign Nodules</h3>
    <p><b>Type:</b> Non-cancerous lung growths<br>
    <b>Prevalence:</b> Very common - found in 20-50% of adults<br>
    <b>Characteristics:</b> Usually small, round, well-defined<br>
    <b>Growth Rate:</b> Slow or no growth over time<br>
    <b>Malignancy Risk:</b> Low (less than 1% malignancy rate)<br>
    <b>Management:</b> Monitoring with regular CT scans
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tumor-card">
    <h3>🔴 Malignant Tumors</h3>
    <p><b>Type:</b> Cancerous lung growths<br>
    <b>Prevalence:</b> Requires immediate medical attention<br>
    <b>Characteristics:</b> Irregular shape, may have spiculated margins<br>
    <b>Growth Rate:</b> Variable - can grow rapidly<br>
    <b>Metastasis Risk:</b> High - can spread to other organs<br>
    <b>Treatment:</b> Surgery, radiation, chemotherapy, immunotherapy, targeted therapy
    </p>
</div>
""", unsafe_allow_html=True)

# Lung Cancer Subtypes
st.header("🫁 Major Lung Cancer Subtypes")

tabs = st.tabs(["Small Cell Lung Cancer", "Non-Small Cell Lung Cancer", "Staging"])

with tabs[0]:
    st.markdown("""
    **Small Cell Lung Cancer (SCLC)**
    - Comprises ~15% of lung cancers
    - Highly aggressive and fast-growing
    - Often has spread beyond the lung at diagnosis
    - Associated with smoking
    - Treated with chemotherapy and radiation
    - 5-year survival: ~7%
    """)

with tabs[1]:
    st.markdown("""
    **Non-Small Cell Lung Cancer (NSCLC)**
    - Comprises ~85% of lung cancers
    - Slower growth than SCLC
    - Main types:
      - Adenocarcinoma (40% of lung cancers)
      - Squamous cell carcinoma (25%)
      - Large cell carcinoma (10%)
    - Treatment: Surgery, radiation, chemotherapy, targeted therapy
    - Better prognosis than SCLC
    """)

with tabs[2]:
    st.markdown("""
    **TNM Staging System**
    
    | Stage | Description | 5-Year Survival |
    |-------|-------------|-----------------|
    | Stage I | Tumor confined to lung | 56% |
    | Stage II | Spread to nearby lymph nodes | 40% |
    | Stage III | Spread to chest wall/organs | 19% |
    | Stage IV | Metastasis to distant sites | 5% |
    
    Early stage detection significantly improves survival rates.
    """)

# Diagnostic Information
st.header("🩺 Diagnostic Methods")

col1, col2 = st.columns(2)

with col1:
    st.subheader("CT Scan (Primary)")
    st.markdown("""
    - **Best for:** Detailed lung visualization
    - **Advantages:** High sensitivity, detects small nodules
    - **Time:** 10-30 minutes
    - **Sensitivity:** 95%+ for lesions >5mm
    - **Resolution:** Can detect nodules as small as 1-2mm
    - **Radiation:** Low dose CT available
    """)

with col2:
    st.subheader("Other Imaging Methods")
    st.markdown("""
    - **Chest X-Ray:** Quick screening, less sensitive
    - **PET Scan:** Metabolic activity assessment
    - **MRI:** Soft tissue and brain metastases
    - **Ultrasound:** Pleural effusion evaluation
    - **Bronchoscopy:** Airway visualization
    """)

# Risk Factors
st.header("⚠️ Risk Factors for Lung Cancer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Major Risk Factors")
    st.markdown("""
    - **Smoking** - #1 risk factor (90% of cases)
    - **Secondhand smoke exposure**
    - **Radon gas exposure**
    - **Asbestos exposure**
    - **Air pollution**
    - **Previous lung disease** (COPD, tuberculosis)
    """)

with col2:
    st.subheader("Additional Risk Factors")
    st.markdown("""
    - **Age** - Most common after 65
    - **Family history**
    - **Personal history of cancer**
    - **Occupational exposure**
    - **Genetics** (KRAS, TP53 mutations)
    - **Immunosuppression**
    """)

# Prevention
st.header("🛡️ Prevention & Early Detection")

st.markdown("""
**Primary Prevention:**
- Quit smoking (or never start)
- Avoid secondhand smoke
- Reduce radon exposure
- Minimize asbestos contact
- Improve air quality
- Regular exercise

**Secondary Prevention (Screening):**
- Low-dose CT screening for high-risk individuals
- Annual screening recommended for:
  - Current smokers aged 50-80
  - Former smokers (quit <15 years ago)
  - 20+ pack-year smoking history

**Why Early Detection Matters:**
- Stage I lung cancer: 56% 5-year survival
- Stage IV lung cancer: 5% 5-year survival
- Early detection saves lives
""")

# Treatment Options
st.header("💊 Treatment Options")

tabs = st.tabs(["Surgery", "Radiation", "Chemotherapy", "Targeted/Immuno"])

with tabs[0]:
    st.markdown("""
    **Surgical Options**
    - Lobectomy (removal of lung lobe)
    - Pneumonectomy (entire lung removal)
    - Wedge resection (part of lobe)
    - Video-assisted thoracoscopic surgery (VATS)
    - Robotic-assisted surgery
    
    **Best for:** Early-stage cancers, good lung function
    **Success rate:** 70-90% for stage I
    """)

with tabs[1]:
    st.markdown("""
    **Radiation Therapy**
    - External Beam Radiation Therapy (EBRT)
    - Stereotactic Body Radiation Therapy (SBRT)
    - Brachytherapy (internal radiation)
    
    **Used for:**
    - Inoperable patients
    - Palliative care
    - Brain metastases
    - Post-surgical adjuvant therapy
    """)

with tabs[2]:
    st.markdown("""
    **Chemotherapy**
    - Platinum-based combinations
    - Pemetrexed, docetaxel, paclitaxel
    - Often combined with radiation
    - Side effects: Nausea, fatigue, hair loss
    
    **Timing:**
    - Neoadjuvant (before surgery)
    - Adjuvant (after surgery)
    - Concurrent with radiation
    """)

with tabs[3]:
    st.markdown("""
    **Targeted Therapy**
    - EGFR inhibitors
    - ALK inhibitors
    - ROS1 inhibitors
    - BRAF/MEK inhibitors
    
    **Immunotherapy**
    - PD-1/PD-L1 checkpoint inhibitors
    - Pembrolizumab, nivolumab, atezolizumab
    - Anti-CTLA-4 agents
    - Excellent response in some patients
    """)

# Warning Signs
st.header("🚨 Warning Signs & Symptoms")

warning_col1, warning_col2, warning_col3 = st.columns(3)

with warning_col1:
    st.subheader("Respiratory Symptoms")
    for symptom in [
        "Persistent cough (>3 weeks)",
        "Hemoptysis (coughing blood)",
        "Shortness of breath",
        "Wheezing or hoarseness",
        "Chest pain"
    ]:
        st.warning(f"⚠️ {symptom}")

with warning_col2:
    st.subheader("Systemic Symptoms")
    for symptom in [
        "Fatigue/weakness",
        "Weight loss",
        "Loss of appetite",
        "Recurrent pneumonia",
        "Night sweats"
    ]:
        st.warning(f"⚠️ {symptom}")

with warning_col3:
    st.subheader("Advanced Disease")
    for symptom in [
        "Arm/shoulder pain",
        "Facial swelling",
        "Superior vena cava syndrome",
        "Neurological symptoms",
        "Bone pain"
    ]:
        st.warning(f"⚠️ {symptom}")

# Prognosis
st.header("📈 Prognosis & Survival Rates")

st.markdown("""
**5-Year Survival Rates by Stage (NSCLC):**

| Stage | Characteristics | 5-Year Survival |
|-------|-----------------|-----------------|
| IA | Tumor <3cm, no spread | 92% |
| IB | Tumor 3-5cm, no spread | 80% |
| IIA | Tumor >5cm or nodal spread | 71% |
| IIB | Larger tumor/more nodes | 55% |
| IIIA | Chest wall/mediastinal involvement | 36% |
| IIIB | Extensive mediastinal involvement | 26% |
| IV | Distant metastasis | 10% |

**Factors Improving Outcomes:**
- Early stage at diagnosis
- Younger age
- Good performance status
- Molecular testing (EGFR, ALK mutations)
- Immunotherapy eligibility
""")

# Important Notice
st.info("""
**⚠️ IMPORTANT DISCLAIMER**

This information is for educational purposes only and should not replace professional medical advice. 
If you experience concerning symptoms, please consult with a qualified healthcare professional immediately.
Early detection and professional medical evaluation are critical for better outcomes.
""")

# Footer Navigation
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    if st.button("← Back", key="footer_back"):
        st.switch_page("pages/Lung_01_Dashboard.py")

with footer_col2:
    if st.button("🔬 Test & Detect", key="footer_detect"):
        st.switch_page("pages/Lung_03_Test_Detect.py")

with footer_col3:
    if st.button("📋 History", key="footer_history"):
        st.switch_page("pages/Lung_04_History.py")

with footer_col4:
    if st.button("🏥 Home", key="footer_home"):
        st.switch_page("Home.py")
