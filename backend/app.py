"""
Flask API Backend for Cancer Detection Platform
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import cv2
import io
import base64
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

# Configuration
BRAIN_MODEL_PATH = r"d:\PROJECTS\cancer\brain_tumor_classifier\outputs\models\brain_tumor_classifier.h5"
LUNG_MODEL_PATH = r"d:\PROJECTS\cancer\Lung\models\ct_cancer_resnet50_best.h5"
UPLOAD_FOLDER = 'temp_uploads'
HISTORY_FOLDER = 'detection_history'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HISTORY_FOLDER, exist_ok=True)

# Class names
BRAIN_CLASSES = {
    0: 'Glioma',
    1: 'Meningioma',
    2: 'No Tumor',
    3: 'Pituitary'
}

LUNG_CLASSES = {
    0: 'Normal',
    1: 'Benign',
    2: 'Malignant'
}

# Load models
brain_model = None
lung_model = None

def load_models():
    """Load both models at startup"""
    global brain_model, lung_model
    try:
        if os.path.exists(BRAIN_MODEL_PATH):
            brain_model = keras.models.load_model(BRAIN_MODEL_PATH)
            print("✓ Brain tumor model loaded")
        else:
            print(f"✗ Brain model not found at: {BRAIN_MODEL_PATH}")
    except Exception as e:
        print(f"✗ Error loading brain model: {e}")
    
    try:
        if os.path.exists(LUNG_MODEL_PATH):
            lung_model = keras.models.load_model(LUNG_MODEL_PATH)
            print("✓ Lung cancer model loaded")
        else:
            print(f"✗ Lung model not found at: {LUNG_MODEL_PATH}")
            print(f"   Looking in: {os.path.dirname(LUNG_MODEL_PATH)}")
            if os.path.exists(os.path.dirname(LUNG_MODEL_PATH)):
                print(f"   Available files: {os.listdir(os.path.dirname(LUNG_MODEL_PATH))}")
    except Exception as e:
        print(f"✗ Error loading lung model: {e}")

# Utility functions
def preprocess_brain_image(image):
    """Preprocess image for brain tumor model"""
    img_resized = image.resize((224, 224))
    if img_resized.mode != 'L':
        img_resized = img_resized.convert('L')
    
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=-1)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array, img_resized

def preprocess_lung_image(image):
    """Preprocess image for lung cancer model"""
    img_resized = image.resize((224, 224))
    if img_resized.mode != 'RGB':
        img_resized = img_resized.convert('RGB')
    
    img_array = np.array(img_resized)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array, img_resized

def create_heatmap(image_array, is_lung=False):
    """Create heatmap overlay for visualization"""
    if is_lung:
        # For RGB images
        gray = cv2.cvtColor(np.array(image_array), cv2.IMREAD_GRAYSCALE) if len(image_array.shape) == 3 else np.array(image_array)
    else:
        gray = np.array(image_array)
    
    # Normalize
    if gray.dtype != np.uint8:
        gray = (gray * 255).astype(np.uint8)
    
    # Create heatmap using Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.abs(laplacian)
    
    # Normalize to 0-255
    heatmap = ((laplacian - laplacian.min()) / (laplacian.max() - laplacian.min() + 1e-8) * 255).astype(np.uint8)
    
    # Apply colormap
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Convert to PIL Image
    return Image.fromarray(heatmap_color)

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def save_to_history(detection_type, result_data):
    """Save detection result to history"""
    history_file = os.path.join(HISTORY_FOLDER, f"{detection_type}_history.json")
    
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        history.append(result_data)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving history: {e}")
        return False

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'brain_model_loaded': brain_model is not None,
        'lung_model_loaded': lung_model is not None
    })

@app.route('/api/brain/detect', methods=['POST'])
def detect_brain_tumor():
    """Brain tumor detection endpoint"""
    if brain_model is None:
        return jsonify({'error': 'Brain tumor model not loaded'}), 500
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    try:
        # Load and preprocess image
        image = Image.open(file.stream)
        processed_img, resized_img = preprocess_brain_image(image)
        
        # Make prediction
        predictions = brain_model.predict(processed_img)
        predicted_class = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class] * 100)
        tumor_type = BRAIN_CLASSES[predicted_class]
        
        # Create visualizations
        heatmap = create_heatmap(resized_img, is_lung=False)
        
        # Prepare response
        result = {
            'success': True,
            'tumor_type': tumor_type,
            'confidence': round(confidence, 2),
            'all_predictions': {
                BRAIN_CLASSES[i]: round(float(predictions[0][i] * 100), 2)
                for i in range(len(BRAIN_CLASSES))
            },
            'original_image': image_to_base64(resized_img),
            'heatmap': image_to_base64(heatmap),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to history
        save_to_history('brain', {
            'tumor_type': tumor_type,
            'confidence': confidence,
            'timestamp': result['timestamp']
        })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lung/detect', methods=['POST'])
def detect_lung_cancer():
    """Lung cancer detection endpoint"""
    if lung_model is None:
        return jsonify({'error': 'Lung cancer model not loaded'}), 500
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    try:
        # Load and preprocess image
        image = Image.open(file.stream)
        processed_img, resized_img = preprocess_lung_image(image)
        
        # Make prediction
        predictions = lung_model.predict(processed_img)
        predicted_class = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class] * 100)
        diagnosis = LUNG_CLASSES[predicted_class]
        
        # Create visualizations
        heatmap = create_heatmap(resized_img, is_lung=True)
        
        # Prepare response
        result = {
            'success': True,
            'diagnosis': diagnosis,
            'confidence': round(confidence, 2),
            'all_predictions': {
                LUNG_CLASSES[i]: round(float(predictions[0][i] * 100), 2)
                for i in range(len(LUNG_CLASSES))
            },
            'original_image': image_to_base64(resized_img),
            'heatmap': image_to_base64(heatmap),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to history
        save_to_history('lung', {
            'diagnosis': diagnosis,
            'confidence': confidence,
            'timestamp': result['timestamp']
        })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<detection_type>', methods=['GET'])
def get_history(detection_type):
    """Get detection history"""
    history_file = os.path.join(HISTORY_FOLDER, f"{detection_type}_history.json")
    
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
            return jsonify({'history': history})
        else:
            return jsonify({'history': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        brain_history_file = os.path.join(HISTORY_FOLDER, 'brain_history.json')
        lung_history_file = os.path.join(HISTORY_FOLDER, 'lung_history.json')
        
        brain_count = 0
        lung_count = 0
        
        if os.path.exists(brain_history_file):
            with open(brain_history_file, 'r') as f:
                brain_count = len(json.load(f))
        
        if os.path.exists(lung_history_file):
            with open(lung_history_file, 'r') as f:
                lung_count = len(json.load(f))
        
        return jsonify({
            'total_scans': brain_count + lung_count,
            'brain_scans': brain_count,
            'lung_scans': lung_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Loading models...")
    load_models()
    print("\nStarting Flask API server...")
    print("Backend running at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
