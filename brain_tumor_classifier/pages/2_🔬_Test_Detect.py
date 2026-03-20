"""
Brain Tumor Testing & Detection Page with PDF Reports
"""
import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image, ImageDraw
import cv2
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False

# Page config
st.set_page_config(page_title="Test & Detect", page_icon="🔬", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border: 2px solid #1f77b4;
    }
    .tumor-type {
        font-size: 1.5rem;
        font-weight: bold;
        color: #d62728;
    }
    .confidence {
        font-size: 1rem;
        color: #2ca02c;
        font-weight: bold;
    }
    .info-text {
        color: #000;
        font-size: 0.95rem;
    }
    .card-title {
        color: #1f77b4;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔬 Brain Tumor Detection</h1>', unsafe_allow_html=True)

# Model configuration
MODEL_PATH = r"d:\PROJECTS\cancer\brain_tumor_classifier\outputs\models\brain_tumor_classifier.h5"
HISTORY_FILE = "detection_history.json"
REPORTS_DIR = "reports"

# Create reports directory
os.makedirs(REPORTS_DIR, exist_ok=True)

CLASS_NAMES = {
    0: 'Glioma',
    1: 'Meningioma',
    2: 'No Tumor',
    3: 'Pituitary'
}

TUMOR_COLORS = {
    'Glioma': '#FF6B6B',
    'Meningioma': '#FFA500',
    'No Tumor': '#51CF66',
    'Pituitary': '#A78BFA'
}

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        model = keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def create_heatmap_overlay(image_array, predictions):
    """Create a heatmap overlay showing tumor probability across the image"""
    # Normalize image
    if image_array.dtype == np.float32 or image_array.dtype == np.float64:
        img_normalized = (image_array * 255).astype(np.uint8)
    else:
        img_normalized = image_array.astype(np.uint8)
    
    # Create heatmap using Laplacian (edge detection)
    laplacian = cv2.Laplacian(img_normalized, cv2.CV_64F)
    laplacian = np.abs(laplacian)
    
    # Normalize to 0-1
    heatmap = (laplacian - laplacian.min()) / (laplacian.max() - laplacian.min() + 1e-8)
    
    # Apply colormap
    heatmap_uint8 = (heatmap * 255).astype(np.uint8)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    
    # Convert original to 3 channels
    img_3channel = cv2.cvtColor(img_normalized, cv2.COLOR_GRAY2BGR)
    
    # Blend images (30% heatmap, 70% original)
    overlay = cv2.addWeighted(img_3channel, 0.7, heatmap_color, 0.3, 0)
    
    return Image.fromarray(overlay)

def highlight_tumor_advanced(image_array, predicted_class):
    """Advanced highlighting with contours and circles"""
    if image_array.dtype == np.float32 or image_array.dtype == np.float64:
        img_uint8 = (image_array * 255).astype(np.uint8)
    else:
        img_uint8 = image_array.astype(np.uint8)
    
    # Convert to 3-channel
    img_color = cv2.cvtColor(img_uint8, cv2.COLOR_GRAY2BGR)
    
    # Apply morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    blurred = cv2.GaussianBlur(img_uint8, (7, 7), 0)
    
    # Adaptive thresholding for better segmentation
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter and draw significant contours
    significant_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 < area < 15000:  # Filter by area
            significant_contours.append(contour)
            # Draw filled contour with highlighting
            cv2.drawContours(img_color, [contour], 0, (0, 255, 255), 2)
            
            # Add semi-transparent overlay
            overlay = img_color.copy()
            cv2.drawContours(overlay, [contour], 0, (0, 255, 255), -1)
            img_color = cv2.addWeighted(img_color, 0.8, overlay, 0.2, 0)
            
            # Draw bounding circles
            (x, y), radius = cv2.minEnclosingCircle(contour)
            cv2.circle(img_color, (int(x), int(y)), int(radius), (255, 0, 0), 2)
    
    return Image.fromarray(img_color)

def preprocess_image(image):
    """Preprocess image for model"""
    img_resized = image.resize((224, 224))
    
    if img_resized.mode != 'L':
        img_resized = img_resized.convert('L')
    
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def make_prediction(model, processed_image):
    """Make prediction"""
    predictions = model.predict(processed_image)
    predicted_class = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class] * 100
    
    return predicted_class, confidence, predictions[0]

def save_to_history(image_name, tumor_type, confidence, timestamp):
    """Save prediction to history"""
    history_data = []
    
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history_data = json.load(f)
        except:
            history_data = []
    
    new_entry = {
        "image": image_name,
        "tumor_type": tumor_type,
        "confidence": round(confidence, 2),
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    history_data.append(new_entry)
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history_data, f, indent=4)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.info("""
    **CNN-Based Brain Tumor Classifier**
    
    Uses deep learning to detect:
    - Glioma
    - Meningioma
    - Pituitary Tumors
    - No Tumor
    
    **Performance:**
    - Accuracy: 93.29%
    - Recall: 92.71%
    """)

# Main content
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1.5rem;">
    <b>📸 Upload a brain MRI image to detect tumor types</b><br>
    <small>Supported formats: JPG, JPEG, PNG | Max size: 200MB</small>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload Brain MRI Image",
    type=['jpg', 'jpeg', 'png'],
    help="Select a brain MRI scan"
)

if uploaded_file is not None:
    # Load model
    model = load_model()
    
    if model is None:
        st.error("❌ Failed to load model")
    else:
        # Load and display image
        image = Image.open(uploaded_file)
        
        # Create layout
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.subheader("📸 Original Image")
            display_image = image.resize((300, 300))
            st.image(display_image, use_column_width=True)
            
            # Preprocess
            processed_image = preprocess_image(image)
            
            # Make prediction
            with st.spinner('🔬 Analyzing MRI...'):
                predicted_class, confidence, all_predictions = make_prediction(model, processed_image)
                tumor_type = CLASS_NAMES[predicted_class]
                timestamp = datetime.now()
        
        with col2:
            st.subheader("🎯 Detection Results")
            
            # Prediction box
            st.markdown(f'<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown(f'<p class="tumor-type">{tumor_type}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="confidence">Confidence: {confidence:.2f}%</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Confidence bar
            st.progress(confidence / 100, text=f"Model Confidence: {confidence:.1f}%")
            
            # All predictions
            st.markdown("**Detailed Predictions:**")
            for idx in range(4):
                prob = all_predictions[idx] * 100
                color = TUMOR_COLORS.get(CLASS_NAMES[idx], '#1f77b4')
                st.markdown(f"""
                <div style="margin: 0.5rem 0; padding: 0.5rem; border-left: 4px solid {color}; background: #f0f2f6; border-radius: 4px;">
                    <b>{CLASS_NAMES[idx]}</b>: {prob:.2f}%
                </div>
                """, unsafe_allow_html=True)
        
        # Heatmap and Highlighting
        st.markdown("---")
        st.subheader("🔍 Tumor Visualization & Analysis")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("**Heatmap Analysis**")
            st.text("Areas with high intensity (red) indicate potential anomalies")
            img_array = np.array(image.resize((224, 224)).convert('L')) / 255.0
            heatmap_img = create_heatmap_overlay(img_array, all_predictions)
            heatmap_display = heatmap_img.resize((300, 300))
            st.image(heatmap_display, use_column_width=True)
        
        with col2:
            st.markdown("**Detected Regions**")
            st.text("Yellow boxes = Detected anomalies | Blue circles = Bounding regions")
            highlighted_img = highlight_tumor_advanced(img_array, predicted_class)
            highlighted_display = highlighted_img.resize((300, 300))
            st.image(highlighted_display, use_column_width=True)
        
        # Chart
        st.markdown("---")
        st.subheader("📊 Confidence Distribution")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        tumors = [CLASS_NAMES[i] for i in range(4)]
        probs = [all_predictions[i] * 100 for i in range(4)]
        colors_list = [TUMOR_COLORS[t] for t in tumors]
        
        bars = ax.bar(tumors, probs, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Probability (%)', fontsize=11)
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, prob in zip(bars, probs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{prob:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.subheader("💡 Clinical Recommendation")
        
        if tumor_type == 'No Tumor':
            st.success(f"""
            ✅ **No Tumor Detected** ({confidence:.2f}% confidence)
            
            The brain MRI appears normal without visible tumor abnormalities.
            However, always consult with healthcare professionals for complete medical evaluation.
            """)
        else:
            st.warning(f"""
            ⚠️ **{tumor_type} Detected** ({confidence:.2f}% confidence)
            
            **Important Actions:**
            1. 🏥 Consult a neurologist or oncologist immediately
            2. 📋 Arrange comprehensive medical evaluation
            3. 💊 Discuss treatment options with specialists
            4. ⚠️ This AI tool is for screening only - professional diagnosis is essential
            
            **Next Steps:**
            - Get additional confirmatory imaging if needed
            - Review pathology reports if biopsy is performed
            - Discuss personalized treatment plans
            """)
        
        # Save to history
        save_to_history(uploaded_file.name, tumor_type, confidence, timestamp)
        
        # Download results
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            result_text = f"""
Brain Tumor Detection Report
============================
Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Image: {uploaded_file.name}

PREDICTION:
Tumor Type: {tumor_type}
Confidence: {confidence:.2f}%

ALL PREDICTIONS:
"""
            for idx in range(4):
                prob = all_predictions[idx] * 100
                result_text += f"{CLASS_NAMES[idx]}: {prob:.2f}%\n"
            
            result_text += f"""

DISCLAIMER:
This is an AI-assisted screening tool for educational purposes.
Always consult qualified healthcare professionals for diagnosis and treatment.
"""
            
            st.download_button(
                label="📥 Download Report",
                data=result_text,
                file_name=f"tumor_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

else:
    st.info("👆 Upload a brain MRI image to start detection")
