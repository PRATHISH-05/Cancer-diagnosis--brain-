"""
Lung Cancer Testing & Detection Page with PDF Reports
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
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except:
    REPORTLAB_AVAILABLE = False

st.set_page_config(page_title="Lung Test & Detect", page_icon="🔬", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-box {
        padding: 1.2rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border: 2px solid #FF6B6B;
    }
    .tumor-type {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FF6B6B;
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
        color: #FF6B6B;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔬 Lung Cancer Detection</h1>', unsafe_allow_html=True)

# Back Button
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("← Back", key="back_btn"):
        st.switch_page("pages/Lung_01_Dashboard.py")

# Model configuration
MODEL_PATH = r"d:\PROJECTS\cancer\Lung\models\ct_cancer_resnet50_best.h5"
HISTORY_FILE = "lung_detection_history.json"
REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

CLASS_NAMES = {
    0: 'Normal/Benign',
    1: 'Malignant'
}

TUMOR_COLORS = {
    'Normal/Benign': '#51CF66',
    'Malignant': '#FF6B6B'
}

@st.cache_resource
def load_model():
    try:
        model = keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def create_heatmap_overlay(image_array, predictions):
    if image_array.dtype == np.float32 or image_array.dtype == np.float64:
        img_normalized = (image_array * 255).astype(np.uint8)
    else:
        img_normalized = image_array.astype(np.uint8)
    
    laplacian = cv2.Laplacian(img_normalized, cv2.CV_64F)
    laplacian = np.abs(laplacian)
    heatmap = (laplacian - laplacian.min()) / (laplacian.max() - laplacian.min() + 1e-8)
    
    heatmap_uint8 = (heatmap * 255).astype(np.uint8)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    
    img_3channel = cv2.cvtColor(img_normalized, cv2.COLOR_GRAY2BGR)
    overlay = cv2.addWeighted(img_3channel, 0.7, heatmap_color, 0.3, 0)
    
    return Image.fromarray(overlay)

def highlight_tumor_advanced(image_array, predicted_class):
    if image_array.dtype == np.float32 or image_array.dtype == np.float64:
        img_uint8 = (image_array * 255).astype(np.uint8)
    else:
        img_uint8 = image_array.astype(np.uint8)
    
    img_color = cv2.cvtColor(img_uint8, cv2.COLOR_GRAY2BGR)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    blurred = cv2.GaussianBlur(img_uint8, (7, 7), 0)
    
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if 100 < area < 15000:
            cv2.drawContours(img_color, [contour], 0, (0, 255, 255), 2)
            overlay = img_color.copy()
            cv2.drawContours(overlay, [contour], 0, (0, 255, 255), -1)
            img_color = cv2.addWeighted(img_color, 0.8, overlay, 0.2, 0)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            cv2.circle(img_color, (int(x), int(y)), int(radius), (255, 0, 0), 2)
    
    return Image.fromarray(img_color)

def preprocess_image(image):
    # Match training pipeline: grayscale CT -> RGB, resize, normalize
    img_gray = image.convert('L')
    img_rgb = img_gray.convert('RGB')
    img_resized = img_rgb.resize((224, 224), Image.Resampling.LANCZOS)
    img_array = np.array(img_resized, dtype=np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)

def make_prediction(model, processed_image, threshold=0.6):
    predictions = model.predict(processed_image, verbose=0)

    # Model is binary sigmoid: extract malignant probability
    if predictions.ndim == 2:
        malignant_prob = float(predictions[0][0])
    else:
        malignant_prob = float(np.ravel(predictions)[0])

    malignant_prob = float(np.clip(malignant_prob, 0.0, 1.0))
    normal_prob = 1.0 - malignant_prob
    prob_vector = np.array([normal_prob, malignant_prob])

    predicted_class = int(malignant_prob >= threshold)
    confidence = prob_vector[predicted_class] * 100

    return predicted_class, confidence, prob_vector

def generate_pdf_report(original_img, heatmap_img, highlighted_img, cancer_class, confidence, all_predictions, timestamp, filename):
    if not REPORTLAB_AVAILABLE:
        return None, None
    
    try:
        pdf_filename = f"lung_cancer_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
        
        doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FF6B6B'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#FF6B6B'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6
        )
        
        story.append(Paragraph("🫁 Lung Cancer Detection Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        header_data = [
            ['Report Date:', timestamp.strftime('%Y-%m-%d %H:%M:%S')],
            ['Source Image:', filename],
            ['Detection Status:', 'Complete']
        ]
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FF6B6B')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("DETECTION RESULTS", heading_style))
        
        result_data = [
            ['Classification:', cancer_class],
            ['Confidence Score:', f'{confidence:.2f}%'],
            ['Risk Level:', 'High' if confidence > 75 else 'Medium' if confidence > 50 else 'Low']
        ]
        result_table = Table(result_data, colWidths=[2*inch, 4*inch])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FF6B6B')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(result_table)
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("PROBABILITY ANALYSIS", heading_style))
        
        pred_data = [['Classification', 'Probability']]
        for idx in range(len(all_predictions)):
            prob = all_predictions[idx] * 100
            pred_data.append([CLASS_NAMES[idx], f'{prob:.2f}%'])
        
        pred_table = Table(pred_data, colWidths=[3*inch, 3*inch])
        pred_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6B6B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(pred_table)
        story.append(PageBreak())
        
        story.append(Paragraph("IMAGE ANALYSIS", heading_style))
        
        img_path_orig = os.path.join(REPORTS_DIR, f"lung_orig_{timestamp.strftime('%Y%m%d_%H%M%S')}.png")
        original_img.save(img_path_orig)
        story.append(Paragraph("Original CT Scan", styles['Heading3']))
        story.append(RLImage(img_path_orig, width=2.5*inch, height=2.5*inch))
        story.append(Spacer(1, 0.1*inch))
        
        img_path_heat = os.path.join(REPORTS_DIR, f"lung_heat_{timestamp.strftime('%Y%m%d_%H%M%S')}.png")
        heatmap_img.save(img_path_heat)
        story.append(Paragraph("Heatmap Analysis", styles['Heading3']))
        story.append(RLImage(img_path_heat, width=2.5*inch, height=2.5*inch))
        story.append(Spacer(1, 0.1*inch))
        
        img_path_high = os.path.join(REPORTS_DIR, f"lung_high_{timestamp.strftime('%Y%m%d_%H%M%S')}.png")
        highlighted_img.save(img_path_high)
        story.append(Paragraph("Detected Anomaly Regions", styles['Heading3']))
        story.append(RLImage(img_path_high, width=2.5*inch, height=2.5*inch))
        story.append(PageBreak())
        
        story.append(Paragraph("CLINICAL RECOMMENDATIONS", heading_style))
        
        if cancer_class == 'Normal/Benign':
            story.append(Paragraph(
                "✅ Normal Lungs Detected<br/>The CT scan analysis indicates normal lung tissue with no abnormalities. "
                "Regular follow-up based on risk factors is recommended.",
                normal_style
            ))
        else:
            story.append(Paragraph(
                f"🔴 Malignant Tumor Detected (Confidence: {confidence:.2f}%)<br/>"
                "URGENT ACTIONS REQUIRED:<br/>"
                "1. 🏥 Schedule immediate consultation with oncologist<br/>"
                "2. 📋 Arrange additional staging imaging (PET, brain MRI)<br/>"
                "3. 🔬 Consider biopsy for pathological confirmation<br/>"
                "4. 💊 Discuss treatment options (surgery, chemo, radiation, immunotherapy)<br/>"
                "5. 🧬 Request molecular testing (EGFR, ALK, PD-L1)<br/><br/>"
                "This AI tool is for screening assistance only. Professional medical diagnosis and evaluation are essential.",
                normal_style
            ))
        
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("IMPORTANT DISCLAIMER", heading_style))
        story.append(Paragraph(
            "This report is generated by an AI-assisted screening tool for educational purposes only. "
            "It is NOT a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals "
            "(pulmonologists, radiologists, oncologists) for comprehensive medical evaluation and treatment decisions. "
            "Early detection through professional channels can significantly improve outcomes.",
            normal_style
        ))
        
        doc.build(story)
        
        return pdf_filename, pdf_path
    
    except Exception as e:
        st.error(f"PDF Generation Error: {e}")
        return None, None

def save_to_history(image_name, cancer_class, confidence, timestamp, all_predictions):
    history_data = []
    
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history_data = json.load(f)
        except:
            history_data = []
    
    new_entry = {
        "image": image_name,
        "classification": cancer_class,
        "confidence": round(confidence, 2),
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "Normal/Benign%": round(all_predictions[0] * 100, 2),
        "Malignant%": round(all_predictions[1] * 100, 2)
    }
    
    history_data.append(new_entry)
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history_data, f, indent=4)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.info("""
    **ResNet50-Based Lung Cancer Classifier**
    
    Detects:
    - Normal/Benign (non-cancer)
    - Malignant tumors
    
    **Technology:**
    - ResNet50 deep learning
    - CT scan analysis
    - Advanced image processing
    """)

st.markdown("""
<div style="background: linear-gradient(135deg, #FF6B6B 0%, #FFA500 100%); padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1.5rem;">
    <b>📸 Upload a lung CT scan to detect cancer</b><br>
    <small>Supported formats: JPG, JPEG, PNG | Max size: 200MB</small>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Lung CT Scan",
    type=['jpg', 'jpeg', 'png'],
    help="Select a lung CT scan image"
)

if uploaded_file is not None:
    model = load_model()
    
    if model is None:
        st.error("❌ Failed to load model")
    else:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown('<div class="card-title">📸 Original CT Scan</div>', unsafe_allow_html=True)
            display_image = image.resize((220, 220))
            st.image(display_image, use_column_width=True)
            
            processed_image = preprocess_image(image)
            
            with st.spinner('🔬 Analyzing CT Scan...'):
                predicted_class, confidence, all_predictions = make_prediction(model, processed_image)
                cancer_class = CLASS_NAMES[predicted_class]
                timestamp = datetime.now()
        
        with col2:
            st.markdown('<div class="card-title">🎯 Detection Results</div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="prediction-box">', unsafe_allow_html=True)
            st.markdown(f'<p class="tumor-type">{cancer_class}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="confidence">Confidence: {confidence:.2f}%</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.progress(confidence / 100, text=f"Model Confidence: {confidence:.1f}%")
            
            st.markdown("**Detailed Predictions:**")
            for idx in range(len(all_predictions)):
                prob = float(all_predictions[idx]) * 100
                color = TUMOR_COLORS.get(CLASS_NAMES[idx], '#FF6B6B')
                st.markdown(f"""
                <div style="margin: 0.5rem 0; padding: 0.5rem; border-left: 4px solid {color}; background: #f0f2f6; border-radius: 4px; color: #000;">
                    <b>{CLASS_NAMES[idx]}</b>: {prob:.2f}%
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="card-title">🔍 Tumor Visualization & Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("**Heatmap Analysis**")
            st.text("Red areas = high cancer probability | Blue areas = normal tissue")
            # Convert image to grayscale for heatmap
            img_gray = image.resize((224, 224)).convert('L')
            img_array = np.array(img_gray) / 255.0
            heatmap_img = create_heatmap_overlay(img_array, all_predictions)
            st.image(heatmap_img.resize((220, 220)), use_column_width=True)
        
        with col2:
            st.markdown("**Detected Regions**")
            st.text("Yellow boxes = Anomalies | Blue circles = Bounding regions")
            highlighted_img = highlight_tumor_advanced(img_array, predicted_class)
            st.image(highlighted_img.resize((220, 220)), use_column_width=True)
        
        st.markdown("---")
        st.markdown('<div class="card-title">📊 Confidence Distribution</div>', unsafe_allow_html=True)
        
        fig, ax = plt.subplots(figsize=(6, 3.5))
        classes = [CLASS_NAMES[i] for i in range(len(all_predictions))]
        probs = [all_predictions[i] * 100 for i in range(len(all_predictions))]
        colors_list = [TUMOR_COLORS[c] for c in classes]
        
        bars = ax.bar(classes, probs, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Probability (%)', fontsize=11)
        ax.set_ylim(0, 100)
        ax.grid(axis='y', alpha=0.3)
        
        for bar, prob in zip(bars, probs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{prob:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.xticks(rotation=15, fontsize=9)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown('<div class="card-title">💡 Clinical Recommendation</div>', unsafe_allow_html=True)
        
        if cancer_class == 'Normal/Benign':
            st.success(f"""
            ✅ **Normal Lungs Detected** ({confidence:.2f}% confidence)
            
            The CT scan appears normal without visible abnormalities.
            However, always consult with healthcare professionals for complete evaluation.
            """)
        else:
            st.error(f"""
            🔴 **Malignant Tumor Detected** ({confidence:.2f}% confidence)
            
            **URGENT - Important Actions:**
            1. 🏥 Consult oncologist immediately
            2. 📋 Arrange staging imaging
            3. 🔬 Discuss biopsy for confirmation
            4. 💊 Explore treatment options
            5. 🧬 Request molecular testing
            """)
        
        save_to_history(uploaded_file.name, cancer_class, confidence, timestamp, all_predictions)
        
        st.markdown("---")
        st.markdown('<div class="card-title">📥 Download Results</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            result_text = f"""
Lung Cancer Detection Report
============================
Date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Image: {uploaded_file.name}

CLASSIFICATION: {cancer_class}
CONFIDENCE: {confidence:.2f}%

ALL PREDICTIONS:
"""
            for idx in range(len(all_predictions)):
                prob = all_predictions[idx] * 100
                result_text += f"{CLASS_NAMES[idx]}: {prob:.2f}%\n"
            
            result_text += f"""

DISCLAIMER:
This is an AI-assisted screening tool for educational purposes.
Always consult qualified healthcare professionals for diagnosis and treatment.
"""
            
            st.download_button(
                label="📄 Download Text Report",
                data=result_text,
                file_name=f"lung_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_txt"
            )
        
        with col2:
            if REPORTLAB_AVAILABLE:
                if st.button("🔄 Generate PDF Report", key="gen_pdf"):
                    with st.spinner("⏳ Generating PDF..."):
                        pdf_filename, pdf_path = generate_pdf_report(
                            image.resize((224, 224)), heatmap_img, highlighted_img,
                            cancer_class, confidence, all_predictions, timestamp, uploaded_file.name
                        )
                        
                        if pdf_path and os.path.exists(pdf_path):
                            with open(pdf_path, 'rb') as f:
                                pdf_data = f.read()
                            
                            st.download_button(
                                label="📥 Download PDF",
                                data=pdf_data,
                                file_name=pdf_filename,
                                mime="application/pdf",
                                key="download_pdf"
                            )
                            st.success("✅ PDF generated successfully!")
        
        with col3:
            json_data = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "image": uploaded_file.name,
                "predictions": {
                    "classification": cancer_class,
                    "confidence": round(confidence, 2),
                    "all_predictions": {
                        CLASS_NAMES[i]: round(all_predictions[i] * 100, 2) 
                        for i in range(len(all_predictions))
                    }
                }
            }
            
            st.download_button(
                label="📊 Download JSON",
                data=json.dumps(json_data, indent=2),
                file_name=f"lung_data_{timestamp.strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_json"
            )

else:
    st.info("👆 Upload a lung CT scan to start detection")

st.markdown("---")
footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)

with footer_col1:
    if st.button("← Back", key="footer_back"):
        st.switch_page("pages/Lung_01_Dashboard.py")

with footer_col2:
    if st.button("📚 Medical Info", key="footer_medical"):
        st.switch_page("pages/Lung_02_Medical_Info.py")

with footer_col3:
    if st.button("📋 History", key="footer_history"):
        st.switch_page("pages/Lung_04_History.py")

with footer_col4:
    if st.button("🏥 Home", key="footer_home"):
        st.switch_page("Home.py")
