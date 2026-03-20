# 🏥 Cancer Detection Platform

**AI-Powered Medical Imaging Analysis with Interactive React Frontend**

Modern, full-stack web application for brain tumor and lung cancer detection using deep learning models with an intuitive, interactive user interface.

![Platform](https://img.shields.io/badge/Platform-Web-blue)
![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB)
![Backend](https://img.shields.io/badge/Backend-Flask-000000)
![ML](https://img.shields.io/badge/ML-TensorFlow-FF6F00)

## ✨ Features

### 🧠 Brain Tumor Detection
- Upload MRI scans
- Detect 4 classes: **Glioma**, **Meningioma**, **Pituitary**, **No Tumor**
- **93.29% accuracy** using custom CNN architecture
- Real-time heatmap visualization

### 🫁 Lung Cancer Detection  
- Upload CT scans
- Classify: **Normal**, **Benign**, **Malignant**
- **99.36% recall** using ResNet50 transfer learning
- High-sensitivity cancer detection

### 🎨 Modern UI/UX
- ✅ Drag & drop image upload
- ✅ Real-time analysis with loading states
- ✅ Interactive heatmap visualization
- ✅ Fullscreen image viewer
- ✅ Smooth animations and transitions
- ✅ Mobile-responsive design
- ✅ History tracking with statistics
- ✅ Beautiful gradient themes

### 📊 Analytics & History
- Track all scans with timestamps
- View confidence trends
- Classification distribution charts
- Export-ready results

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- 4GB+ RAM (for models)

### Installation (Automated)

**Windows PowerShell:**
```powershell
cd cancer
.\setup.ps1
```

This will:
1. ✅ Check prerequisites
2. ✅ Install frontend dependencies
3. ✅ Install backend dependencies
4. ✅ Create Python virtual environment
5. ✅ Verify installation

### Running the Application

**Option 1: Automated Start (Windows)**
```powershell
.\start.ps1
```

**Option 2: Manual Start**

Terminal 1 - Backend:
```bash
cd backend
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

python app.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

**Open Browser:** http://localhost:3000

## 📁 Project Structure

```
cancer/
├── frontend/                    # React Application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   └── ResultsVisualization.jsx
│   │   ├── pages/              # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── BrainDetection.jsx
│   │   │   ├── LungDetection.jsx
│   │   │   ├── History.jsx
│   │   │   └── About.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # Flask API
│   ├── app.py                  # Main server
│   └── requirements.txt
│
├── brain_tumor_classifier/      # Brain models & training
│   └── outputs/models/
│       └── brain_tumor_classifier.h5
│
├── Lung/                        # Lung models & training
│   └── models/
│       └── ct_cancer_resnet50_best.h5
│
├── setup.ps1                    # Automated setup script
├── start.ps1                    # Quick start script
├── SETUP_GUIDE.md              # Detailed setup guide
└── README.md                    # This file
```

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **Vite** | Build tool & dev server |
| **Tailwind CSS** | Utility-first styling |
| **Framer Motion** | Smooth animations |
| **React Router** | Client-side routing |
| **Axios** | HTTP client |
| **React Dropzone** | File upload |
| **Lucide React** | Icon library |

### Backend
| Technology | Purpose |
|------------|---------|
| **Flask** | Web framework |
| **TensorFlow/Keras** | Deep learning |
| **OpenCV** | Image processing |
| **NumPy** | Numerical operations |
| **Pillow** | Image manipulation |
| **Flask-CORS** | Cross-origin support |

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/brain/detect` | POST | Brain tumor analysis |
| `/api/lung/detect` | POST | Lung cancer analysis |
| `/api/history/brain` | GET | Brain scan history |
| `/api/history/lung` | GET | Lung scan history |
| `/api/stats` | GET | Platform statistics |

## 📸 Screenshots

### Home Page
Interactive landing page with system selection

### Brain Detection
- Drag & drop MRI upload
- Real-time classification
- Heatmap visualization
- Confidence scores

### Lung Detection
- CT scan analysis
- Malignant/Benign/Normal classification
- Clinical interpretation
- Visual overlays

### History
- Scan tracking
- Statistics dashboard
- Classification analytics

## 🔧 Configuration

### Backend (`backend/app.py`)
```python
BRAIN_MODEL_PATH = "path/to/brain_model.h5"
LUNG_MODEL_PATH = "path/to/lung_model.h5"
PORT = 5000
```

### Frontend (`frontend/vite.config.js`)
```javascript
server: {
  port: 3000,
  proxy: {
    '/api': 'http://localhost:5000'
  }
}
```

## 📊 Model Performance

### Brain Tumor Model
- **Architecture:** Custom CNN
- **Training Images:** 3,000+ MRI scans
- **Accuracy:** 93.29%
- **Classes:** 4 (Glioma, Meningioma, Pituitary, No Tumor)

### Lung Cancer Model
- **Architecture:** ResNet50 (Transfer Learning)
- **Training Images:** 1,933 CT scans
- **Recall:** 99.36% (cancer detection)
- **Classes:** 3 (Normal, Benign, Malignant)

## 🚀 Building for Production

### Frontend
```bash
cd frontend
npm run build
# Output in dist/
```

### Backend
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deployment Options
- **Frontend:** Netlify, Vercel, GitHub Pages
- **Backend:** Heroku, AWS, Google Cloud, Azure
- **Full Stack:** Docker, Kubernetes

## 🔒 Security & Privacy

- ✅ Images processed in memory
- ✅ No permanent data storage
- ✅ CORS configured properly
- ✅ No user authentication required
- ⚠️ Not for production medical use

## ⚠️ Medical Disclaimer

This platform is for **EDUCATIONAL AND RESEARCH PURPOSES ONLY**.

**NOT intended for clinical use without:**
- Regulatory approval (FDA, CE, etc.)
- Clinical validation studies
- Professional medical oversight
- Integration with medical workflows
- Proper risk management

**Always consult qualified healthcare professionals for medical diagnosis and treatment.**

## 🧪 Development

### Adding New Features
1. Create components in `frontend/src/components/`
2. Add pages in `frontend/src/pages/`
3. Update routing in `App.jsx`
4. Add API endpoints in `backend/app.py`

### Running Tests
```bash
# Frontend (if tests added)
cd frontend
npm test

# Backend (if tests added)
cd backend
pytest
```

### Code Style
- **Frontend:** ESLint + Prettier
- **Backend:** Black + Flake8

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Kill process on port 5000
npx kill-port 5000
```

### Model Loading Errors
- Verify model file paths
- Check TensorFlow version compatibility
- Ensure sufficient RAM

### CORS Issues
- Verify Flask-CORS installed
- Check proxy configuration in vite.config.js

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more troubleshooting.

## 📚 Documentation

- [Setup Guide](SETUP_GUIDE.md) - Detailed installation instructions
- [Frontend README](frontend/README.md) - Frontend documentation
- [API Documentation](#-api-endpoints) - REST API reference

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [Tailwind CSS](https://tailwindcss.com/docs)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is for educational purposes. For commercial use, consult legal counsel and ensure regulatory compliance.

## 🙏 Acknowledgments

- Training data providers
- Open-source community
- Medical professionals who provided guidance
- TensorFlow and React teams

## 📞 Support

For issues or questions:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Review [Issues](#) section
3. Consult documentation
4. Contact maintainers

## 🎯 Roadmap

- [ ] PDF report generation
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Batch processing
- [ ] User authentication
- [ ] Database integration
- [ ] Mobile app
- [ ] DICOM file support
- [ ] 3D visualization
- [ ] Clinical trial mode

## 🌟 Star History

If you find this project helpful, please consider giving it a star! ⭐

---

**Built with ❤️ for advancing medical AI research**

**Version:** 2.0.0 (React Frontend)  
**Last Updated:** 2026

