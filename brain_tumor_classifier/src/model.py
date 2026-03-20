"""
Model Architecture Module
Responsible for:
- Defining CNN architecture
- Softmax output layer (4 classes)
- Model summary and visualization
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import numpy as np


def build_model(input_shape=(224, 224, 1), num_classes=4):
    """
    Build CNN model for brain tumor classification
    
    Architecture:
    - Conv2D blocks: 32→64→128→256 filters
    - MaxPooling after each block (dimensionality reduction)
    - Dropout for regularization
    - Dense layers for decision making
    - Softmax output for probabilities
    
    Args:
        input_shape: Input image shape
        num_classes: Number of output classes
    
    Returns:
        Compiled Keras model
    """
    
    model = Sequential([
        # Block 1: Learn edges
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        
        # Block 2: Learn shapes
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Block 3: Learn patterns
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Block 4: Learn complex patterns
        Conv2D(256, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        
        # Flatten: Convert 3D to 1D
        Flatten(),
        
        # Dense layers: Make decision
        Dense(256, activation='relu'),
        Dropout(0.5),
        
        Dense(128, activation='relu'),
        Dropout(0.3),
        
        # Output layer: 4 classes with softmax
        Dense(num_classes, activation='softmax')
    ])
    
    return model


def print_model_info(model):
    """
    Print model information and architecture
    
    Args:
        model: Keras model
    """
    print("\n" + "="*60)
    print("MODEL ARCHITECTURE")
    print("="*60)
    model.summary()
    print("="*60)
    print("\nModel Parameters:")
    print(f"  Total Parameters: {model.count_params():,}")
    print(f"  Trainable Parameters: {sum([np.prod(w.shape) for w in model.trainable_weights]):,}")
