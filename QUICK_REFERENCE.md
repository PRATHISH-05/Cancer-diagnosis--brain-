# 🏥 Unified Cancer Detection Platform - Quick Reference

## 🚀 Getting Started

### Launch the Application
```bash
cd d:\PROJECTS\cancer\brain_tumor_classifier
streamlit run Home.py
```

**Access URL**: http://localhost:8501

---

## 🧭 Navigation Map

### Home Page (Home.py)
```
🏥 Cancer Detection Platform
│
├─ 🧠 Brain Tumor Detection ───→ Brain_01_Dashboard.py
│
└─ 🫁 Lung Cancer Detection ───→ Lung_01_Dashboard.py
```

### Brain Tumor System
```
Brain_01_Dashboard.py (Hub)
│
├─ 📚 Medical Info ───────────→ Brain_02_Medical_Info.py
├─ 🔬 Test & Detect ─────────→ Brain_03_Test_Detect.py
└─ 📋 History ───────────────→ Brain_04_History.py
```

### Lung Cancer System
```
Lung_01_Dashboard.py (Hub)
│
├─ 📚 Medical Info ───────────→ Lung_02_Medical_Info.py
├─ 🔬 Test & Detect ─────────→ Lung_03_Test_Detect.py
└─ 📋 History ───────────────→ Lung_04_History.py
```

---

## 🎯 Key Features by Page

### Home Page (Home.py)
- **Purpose**: Multi-cancer platform entry point
- **Features**:
  - Cancer type selection buttons
  - System statistics overview
  - Platform capabilities showcase
  - Medical disclaimer

### Brain Dashboard (Brain_01_Dashboard.py)
- **Purpose**: Brain tumor system hub
- **Features**:
  - Model performance metrics (93.29% accuracy)
  - Feature overview cards
  - Quick access to all features
  - Navigation to all brain pages

### Brain Medical Info (Brain_02_Medical_Info.py)
- **Content**:
  - Tumor types (Glioma, Meningioma, Pituitary, No Tumor)
  - Diagnostic methods
  - Risk factors
  - Treatment options
  - Prognosis & survival rates
  - Warning signs & symptoms

### Brain Test & Detect (Brain_03_Test_Detect.py)
- **Features**:
  - MRI image upload
  - Real-time AI detection
  - Confidence scores
  - Heatmap visualization
  - Region highlighting
  - PDF report generation
  - Export options (TXT, JSON, PDF)
  - Auto-save to history

### Brain History (Brain_04_History.py)
- **Features**:
  - Statistics dashboard
  - Detection breakdown chart
  - Detailed records table
  - Individual detection cards
  - Export options (CSV, JSON, TXT)
  - Clear history

### Lung Dashboard (Lung_01_Dashboard.py)
- **Purpose**: Lung cancer system hub
- **Features**:
  - Model info (ResNet50, 90%+ accuracy)
  - Feature overview cards
  - Quick access to all features
  - Navigation to all lung pages

### Lung Medical Info (Lung_02_Medical_Info.py)
- **Content**:
  - Cancer types (Normal, Benign, Malignant)
  - Subtypes (SCLC vs NSCLC)
  - Staging system
  - Diagnostic methods
  - Risk factors & prevention
  - Treatment options
  - Prognosis & survival rates
  - Warning signs & symptoms

### Lung Test & Detect (Lung_03_Test_Detect.py)
- **Features**:
  - CT scan image upload
  - Real-time AI detection
  - Confidence scores
  - Heatmap visualization
  - Region highlighting
  - PDF report generation
  - Export options (TXT, JSON, PDF)
  - Auto-save to history

### Lung History (Lung_04_History.py)
- **Features**:
  - Statistics dashboard
  - Classification breakdown chart
  - Detailed records table
  - Individual detection cards
  - Export options (CSV, JSON, TXT)
  - Clear history

---

## 📊 Detection Classes

### Brain Tumor System
1. **Glioma** - Malignant primary brain tumor
2. **Meningioma** - Membrane tumor (usually benign)
3. **Pituitary** - Hormone-secreting tumor
4. **No Tumor** - Normal brain scan

### Lung Cancer System
1. **Normal** - Healthy lung tissue
2. **Benign** - Non-cancerous nodules
3. **Malignant** - Cancerous growths

---

## 📁 File Structure

```
brain_tumor_classifier/
├── Home.py                      ← Main dashboard
├── pages/
│   ├── Brain_01_Dashboard.py
│   ├── Brain_02_Medical_Info.py
│   ├── Brain_03_Test_Detect.py
│   ├── Brain_04_History.py
│   ├── Lung_01_Dashboard.py
│   ├── Lung_02_Medical_Info.py
│   ├── Lung_03_Test_Detect.py
│   └── Lung_04_History.py
├── outputs/models/
│   └── brain_tumor_classifier.h5
├── detection_history.json       ← Brain history
├── lung_detection_history.json  ← Lung history
└── reports/                     ← Generated PDFs
```

---

## 🔍 Workflow Examples

### Brain Tumor Screening Workflow
1. Open Home.py → Click 🧠 Brain Tumor
2. Click 🔬 Test & Detect
3. Upload MRI image
4. Review predictions & visualizations
5. Click "Generate PDF Report"
6. Download report
7. View History page for past results

### Lung Cancer Screening Workflow
1. Open Home.py → Click 🫁 Lung Cancer
2. Click 🔬 Test & Detect
3. Upload CT scan
4. Review predictions & visualizations
5. Click "Generate PDF Report"
6. Download report
7. View History page for past results

### Learning Medical Information
1. Open Home.py → Select cancer type
2. Click 📚 Medical Info
3. Browse disease information
4. Learn about treatments
5. Understand symptoms

---

## 📊 Model Information

### Brain Tumor Classifier
- **Type**: CNN (Convolutional Neural Network)
- **Accuracy**: 93.29%
- **Recall**: 92.71%
- **Input**: MRI images (224×224 grayscale)
- **Output**: 4-class probabilities

### Lung Cancer Classifier
- **Type**: ResNet50 (Transfer Learning)
- **Input**: CT scans (224×224 grayscale)
- **Output**: 3-class probabilities

---

## 💾 Data Management

### History Files
- **Brain**: `detection_history.json`
- **Lung**: `lung_detection_history.json`

### Generated Reports
- Location: `reports/` directory
- Formats: PDF, PNG (images), TXT, JSON

### Export Options
- **CSV**: Spreadsheet format (detailed predictions)
- **JSON**: Raw data format
- **PDF**: Professional report with images
- **TXT**: Text summary report

---

## 🎨 UI Features

### Visualizations
- **Heatmap**: Color-coded anomaly detection (Red=tumor, Blue=normal)
- **Detected Regions**: Yellow boxes + blue circles marking suspicious areas
- **Confidence Chart**: Bar chart showing all class probabilities

### Navigation
- Back buttons on every page
- Footer navigation bar
- `st.switch_page()` for seamless page transitions
- Color-coded systems (Purple for Brain, Red/Orange for Lung)

### Accessibility
- Black text on contrasting backgrounds
- Clear visual hierarchy
- Emoji labels for quick identification
- Responsive layouts
- Medical disclaimers on all pages

---

## ⚠️ Important Notes

### Medical Disclaimers
- ⚠️ AI tool is for **educational/screening purposes only**
- ⚠️ **NOT** a substitute for professional diagnosis
- ⚠️ Always consult licensed healthcare professionals
- ⚠️ Early detection through professionals is critical

### System Requirements
- Python 3.8+
- TensorFlow/Keras
- Streamlit
- OpenCV, PIL, NumPy, Pandas, ReportLab, Matplotlib

### Installation
```bash
pip install -r requirements.txt
pip install reportlab
```

---

## 🐛 Troubleshooting

### App won't start
```bash
# Ensure you're in the correct directory
cd d:\PROJECTS\cancer\brain_tumor_classifier

# Run with explicit Python path if needed
python -m streamlit run Home.py
```

### ReportLab not installed
```bash
pip install reportlab
```

### Models not loading
- Verify model files exist:
  - `outputs/models/brain_tumor_classifier.h5`
  - `Lung/models/ct_cancer_resnet50_best.h5`

### History not saving
- Check file permissions in the project directory
- Ensure `detection_history.json` and `lung_detection_history.json` are writable

---

## 📞 Support

For issues or questions:
1. Check the medical disclaimer
2. Verify model files exist
3. Check Python/package versions
4. Review console error messages
5. Restart the Streamlit app

---

## ✅ Verification Checklist

- [ ] Home.py loads with two cancer options
- [ ] Brain system accessible
- [ ] Lung system accessible
- [ ] Medical info pages display correctly
- [ ] Image upload works
- [ ] Predictions generate
- [ ] Visualizations display
- [ ] PDF generation works
- [ ] History saves correctly
- [ ] Exports work (CSV, JSON, TXT, PDF)
- [ ] Navigation works seamlessly
- [ ] All disclaimers visible

---

**Last Updated**: 2024
**Status**: ✅ Fully Functional
**Platform**: Unified Multi-Cancer Detection System

