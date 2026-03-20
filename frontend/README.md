# Cancer Detection Platform - React Frontend

Modern, interactive React-based frontend for AI-powered cancer detection system.

## 🎯 Features

- **Interactive UI**: Modern, responsive design with smooth animations
- **Drag & Drop Upload**: Easy image upload with preview
- **Real-time Analysis**: Instant results with confidence scores
- **Visualization**: Heatmap overlays and interactive image viewer
- **History Tracking**: View past scans and statistics
- **Mobile Responsive**: Works on all device sizes

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend)
- Trained models in place

### Installation

1. **Install Frontend Dependencies**
```bash
cd frontend
npm install
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### Running the Application

1. **Start Backend Server** (Terminal 1)
```bash
cd backend
python app.py
```
Backend will run on: http://localhost:5000

2. **Start Frontend Development Server** (Terminal 2)
```bash
cd frontend
npm run dev
```
Frontend will run on: http://localhost:3000

3. **Open Browser**
Navigate to http://localhost:3000

## 📁 Project Structure

```
cancer/
├── frontend/                 # React Frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   └── ResultsVisualization.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── BrainDetection.jsx
│   │   │   ├── LungDetection.jsx
│   │   │   ├── History.jsx
│   │   │   └── About.jsx
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                  # Flask API Backend
│   ├── app.py               # Main API server
│   ├── requirements.txt
│   └── detection_history/   # History storage
│
└── brain_tumor_classifier/   # Models directory
    └── outputs/models/
        └── brain_tumor_classifier.h5
```

## 🛠️ Tech Stack

### Frontend
- **React 18**: Modern UI library
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Smooth animations
- **Axios**: HTTP client
- **React Router**: Navigation
- **Lucide React**: Beautiful icons
- **React Dropzone**: File upload

### Backend
- **Flask**: Lightweight Python web framework
- **TensorFlow/Keras**: Deep learning models
- **OpenCV**: Image processing
- **Pillow**: Image manipulation
- **NumPy**: Numerical operations

## 🎨 Key Features

### 1. Brain Tumor Detection
- Upload MRI scans
- Detect 4 classes: Glioma, Meningioma, Pituitary, No Tumor
- 93.29% accuracy
- Heatmap visualization

### 2. Lung Cancer Detection
- Upload CT scans
- Classify: Normal, Benign, Malignant
- 99.36% recall
- Advanced ResNet50 model

### 3. Interactive Visualization
- Original image view
- Heatmap overlay
- Fullscreen mode
- Side-by-side comparison

### 4. History & Analytics
- Scan history tracking
- Statistics dashboard
- Classification distribution
- Confidence trends

## 🔧 Configuration

### Backend Configuration
Edit `backend/app.py` to configure:
- Model paths
- Upload folder
- History storage location

### Frontend Configuration
Edit `frontend/vite.config.js` for:
- API proxy settings
- Port configuration

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/brain/detect` | POST | Brain tumor detection |
| `/api/lung/detect` | POST | Lung cancer detection |
| `/api/history/brain` | GET | Brain scan history |
| `/api/history/lung` | GET | Lung scan history |
| `/api/stats` | GET | Overall statistics |

## 🚀 Building for Production

### Frontend
```bash
cd frontend
npm run build
```
Output will be in `frontend/dist/`

### Backend
For production deployment:
1. Use gunicorn or uwsgi
2. Set up proper CORS
3. Use environment variables
4. Enable HTTPS

## 🔐 Security Notes

- Images are processed in memory
- No permanent storage of medical data
- CORS configured for development
- For production: implement proper authentication

## ⚠️ Medical Disclaimer

This platform is for **educational and research purposes only**. Not intended for clinical use without:
- Regulatory approval
- Professional medical oversight
- Proper validation studies
- Integration with clinical workflows

## 📝 Development Notes

### Adding New Features
1. Create component in `src/components/`
2. Add route in `App.jsx`
3. Update navigation in `Navbar.jsx`

### Styling
- Uses Tailwind CSS utility classes
- Custom animations in `index.css`
- Gradient themes configurable in `tailwind.config.js`

### State Management
- React hooks for local state
- Axios for API calls
- No global state management (simple app)

## 🐛 Troubleshooting

### Backend Issues
- Ensure models are in correct paths
- Check Python dependencies
- Verify TensorFlow installation

### Frontend Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port availability (3000, 5000)
- Verify API proxy in vite.config.js

### CORS Issues
- Ensure Flask-CORS is installed
- Check allowed origins in backend

## 📞 Support

For issues or questions about:
- Frontend: Check React/Vite documentation
- Backend: Check Flask/TensorFlow documentation
- Models: Refer to original training notebooks

## 🎯 Future Enhancements

- [ ] PDF report generation
- [ ] Export results
- [ ] Batch processing
- [ ] Advanced analytics
- [ ] User authentication
- [ ] Database integration
- [ ] Real-time collaboration
- [ ] Mobile app version

## 📄 License

Educational and research use only. Consult legal counsel for commercial use.

---

**Built with ❤️ for advancing medical AI research**
