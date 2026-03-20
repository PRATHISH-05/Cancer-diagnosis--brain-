"""
Medical Information about Brain Tumors
"""
import streamlit as st

st.set_page_config(page_title="Medical Information", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    .medical-header {
        color: #1f77b4;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .tumor-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border-left: 5px solid #d62728;
    }
    .stat-box {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="medical-header">🧬 Brain Tumor Medical Information</h1>', unsafe_allow_html=True)

# Back Button
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("pages/Brain_01_Dashboard.py")

# Overview
st.header("📊 Overview")
st.markdown("""
Brain tumors are abnormal growths of cells in the brain. They can originate in the brain (primary) 
or spread from cancer elsewhere (secondary). Early detection is crucial for better treatment outcomes.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h3>~695K</h3>
        <p>Annual diagnosis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h3>5-Year</h3>
        <p>Survival rate varies</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <h3>4 Types</h3>
        <p>Detected here</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <h3>MRI</h3>
        <p>Primary diagnosis</p>
    </div>
    """, unsafe_allow_html=True)

# Tumor Types
st.header("🔍 Tumor Types Explained")

st.markdown("""
<div class="tumor-card">
    <h3>🔴 Glioma</h3>
    <p><b>Type:</b> Primary brain tumor<br>
    <b>Prevalence:</b> ~30% of all brain tumors<br>
    <b>Origin:</b> Glial cells that support nerve cells<br>
    <b>Grade:</b> I-IV (Low to High malignancy)<br>
    <b>Symptoms:</b> Headaches, seizures, vision problems, cognitive changes<br>
    <b>Treatment:</b> Surgery, radiation therapy, chemotherapy
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tumor-card">
    <h3>🟠 Meningioma</h3>
    <p><b>Type:</b> Tumor of the meninges (protective membranes)<br>
    <b>Prevalence:</b> ~37% of primary brain tumors<br>
    <b>Origin:</b> Cells covering brain and spinal cord<br>
    <b>Malignancy:</b> Mostly benign (WHO Grade I)<br>
    <b>Symptoms:</b> Headaches, vision changes, hearing loss<br>
    <b>Treatment:</b> Surgery, sometimes radiation therapy
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tumor-card">
    <h3>💜 Pituitary Adenoma</h3>
    <p><b>Type:</b> Hormone-secreting tumor<br>
    <b>Prevalence:</b> ~3% of brain tumors<br>
    <b>Origin:</b> Pituitary gland cells<br>
    <b>Malignancy:</b> Benign<br>
    <b>Symptoms:</b> Hormone imbalances, vision problems, headaches<br>
    <b>Treatment:</b> Medication, surgery, radiation
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tumor-card">
    <h3>✅ No Tumor</h3>
    <p><b>Status:</b> Normal brain scan<br>
    <b>Significance:</b> No abnormal growths detected<br>
    <b>What it means:</b> Brain structure appears healthy<br>
    <b>Follow-up:</b> Regular check-ups recommended based on medical history<br>
    <b>Important:</b> Always consult with healthcare professionals for complete evaluation
    </p>
</div>
""", unsafe_allow_html=True)

# Diagnostic Information
st.header("🩺 Diagnostic Methods")

col1, col2 = st.columns(2)

with col1:
    st.subheader("MRI Imaging")
    st.markdown("""
    - **Best for:** Soft tissue visualization
    - **Advantages:** No radiation, detailed images
    - **Time:** 30-60 minutes
    - **Sensitivity:** 90-95% for brain tumors
    - **Resolution:** Can detect tumors as small as 2-3mm
    """)

with col2:
    st.subheader("CT Imaging")
    st.markdown("""
    - **Best for:** Quick screening, bone detail
    - **Advantages:** Fast, widely available
    - **Time:** 5-10 minutes
    - **Sensitivity:** 60-70% for brain tumors
    - **Limitation:** Lower soft tissue contrast
    """)

# Risk Factors
st.header("⚠️ Risk Factors")

risk_factors = {
    "Modifiable": [
        "Radiation exposure (occupational/medical)",
        "Mobile phone exposure (under investigation)",
        "Environmental toxins"
    ],
    "Non-Modifiable": [
        "Age (more common with age)",
        "Genetic conditions (NF1, NF2, Li-Fraumeni)",
        "Family history of cancer",
        "Previous cancer treatment",
        "Immunosuppression"
    ]
}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Potentially Modifiable")
    for factor in risk_factors["Modifiable"]:
        st.markdown(f"• {factor}")

with col2:
    st.subheader("Non-Modifiable")
    for factor in risk_factors["Non-Modifiable"]:
        st.markdown(f"• {factor}")

# Treatment Options
st.header("💊 Treatment Options")

tabs = st.tabs(["Surgery", "Radiation", "Chemotherapy", "Targeted Therapy"])

with tabs[0]:
    st.markdown("""
    **Neurosurgical Resection**
    - Most common primary treatment
    - Goal: Remove as much tumor as safely possible
    - Timing: Often first treatment before radiation/chemo
    - Risks: Infection, bleeding, neurological deficits
    - Effectiveness: Varies by tumor type and grade
    """)

with tabs[1]:
    st.markdown("""
    **Radiation Therapy**
    - External Beam Radiation (EBRT)
    - Stereotactic Radiosurgery (SRS/Gamma Knife)
    - Proton Beam Therapy
    - Often combined with surgery
    - Typical course: 25-30 fractions over 5-6 weeks
    """)

with tabs[2]:
    st.markdown("""
    **Chemotherapy**
    - Commonly used: TMZ (Temozolomide)
    - Platinum-based agents
    - Combination regimens
    - Often combined with radiation
    - May have side effects: Nausea, hair loss, fatigue
    """)

with tabs[3]:
    st.markdown("""
    **Targeted & Immunotherapy**
    - Tumor treating fields (TTF)
    - Immune checkpoint inhibitors
    - Targeted agents for specific mutations
    - Clinical trials for newer approaches
    - Personalized based on tumor genetics
    """)

# Prognosis
st.header("📈 Prognosis & Survival Rates")

st.markdown("""
**5-Year Survival Rates** (approximate, varies by grade):

| Tumor Type | Grade | Survival Rate |
|-----------|-------|--------------|
| Glioma (Glioblastoma) | IV | 5-10% |
| Glioma (Astrocytoma) | III | 25-40% |
| Meningioma | I | 90-95% |
| Pituitary Adenoma | I | 95%+ |

*Note: These are general statistics and individual outcomes vary based on multiple factors.*
""")

# Warning Signs
st.header("🚨 Warning Signs & Symptoms")

warning_symptoms = {
    "Common": ["Persistent headaches", "Nausea/vomiting", "Vision problems", "Hearing loss"],
    "Neurological": ["Seizures", "Balance/coordination problems", "Weakness/numbness", "Cognitive changes"],
    "Behavioral": ["Personality changes", "Mood changes", "Memory problems", "Speech difficulties"]
}

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Common Symptoms")
    for symptom in warning_symptoms["Common"]:
        st.warning(f"⚠️ {symptom}")

with col2:
    st.subheader("Neurological")
    for symptom in warning_symptoms["Neurological"]:
        st.warning(f"⚠️ {symptom}")

with col3:
    st.subheader("Behavioral")
    for symptom in warning_symptoms["Behavioral"]:
        st.warning(f"⚠️ {symptom}")

# Important Notice
st.info("""
**⚠️ IMPORTANT DISCLAIMER**

This information is for educational purposes only and should not replace professional medical advice. 
If you experience any concerning symptoms, please consult with a qualified healthcare professional immediately.
Early detection and professional medical evaluation are critical for better outcomes.
""")

# Footer Navigation
st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    if st.button("← Back", key="footer_back"):
        st.switch_page("pages/Brain_01_Dashboard.py")

with footer_col2:
    if st.button("🔬 Test & Detect", key="footer_detect"):
        st.switch_page("pages/Brain_03_Test_Detect.py")

with footer_col3:
    if st.button("📋 History", key="footer_history"):
        st.switch_page("pages/Brain_04_History.py")

with footer_col4:
    if st.button("🏥 Home", key="footer_home"):
        st.switch_page("Home.py")
