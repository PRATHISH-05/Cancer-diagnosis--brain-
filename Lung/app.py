import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="🏥 Lung Cancer Detection",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #e74c3c;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 1.2em;
    }
    .cancer-box {
        background-color: #ffe6e6;
        border-left: 5px solid #e74c3c;
    }
    .benign-box {
        background-color: #fff3cd;
        border-left: 5px solid #f39c12;
    }
    .normal-box {
        background-color: #d4edda;
        border-left: 5px solid #27ae60;
    }
    .confidence-bar {
        width: 100%;
        height: 30px;
        background-color: #ecf0f1;
        border-radius: 5px;
        overflow: hidden;
        margin: 10px 0;
    }
    .metric-label {
        font-weight: bold;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏥 Lung Cancer Detection System</div>', unsafe_allow_html=True)
st.markdown("**AI-Powered CT Image Analysis for Clinical Decision Support**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📋 Information")
    st.info("""
    **Purpose:** This tool assists radiologists in detecting lung cancer from CT images.
    
    **Model Details:**
    - Architecture: ResNet50 Transfer Learning
    - Training Data: 1933 CT images
    - Recall: 99.36% (catches virtually all cancer cases)
    - Best Model Checkpoint: `ct_cancer_resnet50_best.h5`
    
    **Classification:**
    - **Normal**: Healthy lungs
    - **Benign**: Non-cancerous lesions
    - **Malignant**: Cancer detected
    """)
    
    st.divider()
    st.markdown("### ⚠️ Clinical Disclaimer")
    st.warning("""
    This tool is for **educational and research purposes only**. 
    
    **NOT FOR CLINICAL USE** without:
    - Regulatory approval
    - Independent validation
    - Integration with medical workflows
    - Radiologist supervision
    
    Always consult qualified medical professionals for diagnosis.
    """)

# Load model
@st.cache_resource
def load_model():
    """Load the trained model"""
    model_path = Path('models/ct_cancer_resnet50_best.h5')
    if not model_path.exists():
        st.error(f"❌ Model not found at {model_path}")
        st.stop()
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

# Preprocess image
def preprocess_image(image_array):
    """Preprocess image to match training pipeline"""
    # Ensure grayscale
    if len(image_array.shape) == 3:
        image_gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        image_gray = image_array
    
    # Resize to 224x224
    image_resized = cv2.resize(image_gray, (224, 224), interpolation=cv2.INTER_LANCZOS4)
    
    # Convert to RGB (3 channels for ResNet50)
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_GRAY2RGB)
    
    # Normalize to [0, 1]
    image_normalized = image_rgb.astype('float32') / 255.0
    
    # Add batch dimension
    image_batch = np.expand_dims(image_normalized, axis=0)
    
    return image_batch, image_rgb

# Make prediction
def predict(model, image_batch):
    """Make prediction"""
    prediction_prob = model.predict(image_batch, verbose=0)[0][0]
    return prediction_prob

# Classify prediction with uncertainty zone
def classify_prediction(prob, threshold=0.6, uncertainty_margin=0.1):
    """
    Classify prediction with conservative threshold and uncertainty zone
    
    Args:
        prob: Raw model probability (0-1)
        threshold: Decision boundary (default 0.6 - more conservative than 0.5)
        uncertainty_margin: Zone around threshold for "Requires Review"
    """
    # Define zones
    upper_uncertain = threshold + uncertainty_margin
    lower_uncertain = threshold - uncertainty_margin
    
    if prob < lower_uncertain:
        # Confident Normal/Benign
        category = "Normal/Benign"
        confidence = (1 - prob) * 100
        risk_level = "🟢 LOW RISK"
        status = "CONFIDENT - Normal"
        
    elif lower_uncertain <= prob <= upper_uncertain:
        # Uncertain - Requires Review
        category = "⚠️ UNCERTAIN"
        confidence = None
        risk_level = "🟡 REVIEW NEEDED"
        status = "BORDERLINE - Expert Review Required"
        
    else:  # prob > upper_uncertain
        # Confident Malignant
        category = "Malignant (Cancer)"
        confidence = prob * 100
        risk_level = "🔴 HIGH RISK"
        status = "CONFIDENT - Malignant"
    
    return category, confidence, risk_level, status

# Main app
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Upload CT Image")
    
    uploaded_file = st.file_uploader(
        "Select a CT scan image",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help="Upload grayscale or color CT image (recommended: 224x224 or larger)"
    )
    
    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Show image info
        with st.expander("📊 Image Details"):
            img_array = np.array(image)
            st.write(f"**Shape:** {img_array.shape}")
            st.write(f"**Size:** {image.size}")
            st.write(f"**Format:** {image.format}")

with col2:
    st.subheader("🤖 Analysis Results")
    
    # Threshold adjustment
    with st.expander("⚙️ Advanced Settings (Optional)"):
        col_threshold1, col_threshold2 = st.columns(2)
        with col_threshold1:
            decision_threshold = st.slider(
                "Decision Threshold",
                min_value=0.4,
                max_value=0.8,
                value=0.65,
                step=0.05,
                help="Lower = more conservative (fewer false positives). Default 0.65 recommended."
            )
        with col_threshold2:
            uncertainty_margin = st.slider(
                "Uncertainty Margin",
                min_value=0.02,
                max_value=0.15,
                value=0.1,
                step=0.02,
                help="Zone around threshold requiring expert review"
            )
        
        st.info(f"""
        **Current Settings:**
        - Normal/Benign Zone: 0.00 - {decision_threshold - uncertainty_margin:.2f}
        - Review Zone: {decision_threshold - uncertainty_margin:.2f} - {decision_threshold + uncertainty_margin:.2f}
        - Malignant Zone: {decision_threshold + uncertainty_margin:.2f} - 1.00
        """)
    
    if uploaded_file:
        # Convert to array
        image_array = np.array(Image.open(uploaded_file))
        
        # Preprocess
        image_batch, processed_image = preprocess_image(image_array)
        
        # Load model
        model = load_model()
        
        # Make prediction
        prediction_prob = predict(model, image_batch)
        category, confidence, risk_level, status = classify_prediction(
            prediction_prob, 
            threshold=decision_threshold,
            uncertainty_margin=uncertainty_margin
        )
        
        # Display prediction
        st.markdown(f"### {risk_level}")
        
        # Result box with color coding
        if category == "Malignant (Cancer)":
            st.markdown(f'<div class="result-box cancer-box">'
                       f'<strong>🚨 PREDICTION: {category}</strong><br>'
                       f'<span class="metric-label">Confidence: {confidence:.2f}%</span><br>'
                       f'<span style="color: #c0392b; font-size: 0.9em;">{status}</span>'
                       f'</div>', unsafe_allow_html=True)
            st.error("⚠️ **Potential malignancy detected** - URGENT radiologist review required")
            
        elif category == "⚠️ UNCERTAIN":
            st.markdown(f'<div class="result-box benign-box">'
                       f'<strong>⚠️ PREDICTION: {category}</strong><br>'
                       f'<span class="metric-label">Confidence: N/A (Borderline)</span><br>'
                       f'<span style="color: #d68910; font-size: 0.9em;">{status}</span>'
                       f'</div>', unsafe_allow_html=True)
            st.warning("**Uncertain Result** - This image is in the borderline zone. Expert radiologist review is REQUIRED for clinical decision.")
            
        else:
            st.markdown(f'<div class="result-box normal-box">'
                       f'<strong>✅ PREDICTION: {category}</strong><br>'
                       f'<span class="metric-label">Confidence: {confidence:.2f}%</span><br>'
                       f'<span style="color: #186a3b; font-size: 0.9em;">{status}</span>'
                       f'</div>', unsafe_allow_html=True)
            st.success("No malignancy detected - Routine follow-up recommended")
        
        # Detailed metrics
        st.divider()
        st.subheader("📈 Detailed Analysis")
        
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        
        with col_metrics1:
            st.metric(
                label="Raw Model Score",
                value=f"{prediction_prob:.4f}",
                help="Direct model output (0-1)"
            )
        
        with col_metrics2:
            st.metric(
                label="Cancer Probability",
                value=f"{prediction_prob*100:.2f}%"
            )
        
        with col_metrics3:
            st.metric(
                label="Normal/Benign Probability",
                value=f"{(1-prediction_prob)*100:.2f}%"
            )
        
        # Visual zone indicator
        st.markdown("### Decision Zones")
        col_zone1, col_zone2, col_zone3 = st.columns(3)
        
        with col_zone1:
            zone_prob = max(0, min(1, (decision_threshold - uncertainty_margin)))
            st.write(f"**🟢 Normal/Benign**")
            st.write(f"0.00 → {zone_prob:.2f}")
            if prediction_prob < (decision_threshold - uncertainty_margin):
                st.success("✅ You are here")
        
        with col_zone2:
            lower = decision_threshold - uncertainty_margin
            upper = decision_threshold + uncertainty_margin
            st.write(f"**🟡 Uncertain Zone**")
            st.write(f"{lower:.2f} → {upper:.2f}")
            if lower <= prediction_prob <= upper:
                st.warning("⚠️ You are here")
        
        with col_zone3:
            zone_prob = min(1, (decision_threshold + uncertainty_margin))
            st.write(f"**🔴 Malignant**")
            st.write(f"{zone_prob:.2f} → 1.00")
            if prediction_prob > (decision_threshold + uncertainty_margin):
                st.error("⚠️ You are here")
        
        # Confidence visualization
        st.markdown("### Confidence Visualization")
        
        fig_col1, fig_col2 = st.columns([1, 1])
        
        with fig_col1:
            # Progress bars
            st.write("**Score Distribution**")
            st.progress(prediction_prob, text=f"Cancer: {prediction_prob*100:.1f}%")
            st.progress(1-prediction_prob, text=f"Normal: {(1-prediction_prob)*100:.1f}%")
        
        with fig_col2:
            # Zone indicator
            st.write("**Position in Decision Space**")
            
            # Create visual indicator
            zone_lower = decision_threshold - uncertainty_margin
            zone_upper = decision_threshold + uncertainty_margin
            
            # Normalize score for display (0-10 scale)
            display_score = prediction_prob * 10
            
            st.write(f"""
            ```
            0 ← Normal ─────── Uncertain ─────── Malignant ← 10
                        {zone_lower*10:.1f}        {zone_upper*10:.1f}
                        
            Your Score: {display_score:.1f}
            ```
            """)
    
    else:
        st.info("👆 Upload an image to get started")

# Footer
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("### 📊 Model Performance")
    st.markdown("""
    - **Recall:** 99.36%
    - **Precision:** 70.91%
    - **AUC-ROC:** 0.8745
    - **Accuracy:** 77.59%
    """)

with col_footer2:
    st.markdown("### 🎯 Clinical Priority")
    st.markdown("""
    - **Higher threshold** (0.65 vs 0.5)
    - Reduces false positives
    - "Uncertain zone" for review
    - Radiologist always involved
    - Conservative approach
    """)

with col_footer3:
    st.markdown("### 🔧 System Info")
    st.markdown("""
    - Framework: TensorFlow 2.12
    - Model: ResNet50
    - Input: 224×224 CT images
    - Output: Binary classification
    """)

st.markdown("""
---
**🏥 Lung Cancer Detection System** | Educational & Research Use Only  
*For clinical deployment: FDA approval & hospital integration required*
""")
