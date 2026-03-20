"""
Utility Functions Module
Responsible for:
- Helper functions
- Plotting utilities
- Label mapping
- Common operations
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns


class_names_mapping = {
    0: 'glioma',
    1: 'meningioma',
    2: 'notumor',
    3: 'pituitary'
}

idx_to_name = {v: k for k, v in enumerate(class_names_mapping.values())}


def load_and_preprocess_image(image_path, img_size=224):
    """
    Load and preprocess a single image
    
    Args:
        image_path: Path to image
        img_size: Target size
    
    Returns:
        Preprocessed image array
    """
    
    img = Image.open(image_path).convert('L')  # Grayscale
    img_resized = img.resize((img_size, img_size))
    img_array = np.array(img_resized) / 255.0
    img_batch = np.expand_dims(np.expand_dims(img_array, axis=0), axis=-1)
    
    return img_batch


def get_class_counts(dataset_path, classes):
    """
    Count images per class
    
    Args:
        dataset_path: Path to dataset
        classes: List of class names
    
    Returns:
        Dictionary with counts
    """
    
    counts_train = {}
    counts_test = {}
    
    for cls in classes:
        train_path = os.path.join(dataset_path, 'Train', cls)
        test_path = os.path.join(dataset_path, 'Test', cls)
        
        if os.path.exists(train_path):
            counts_train[cls] = len(os.listdir(train_path))
        if os.path.exists(test_path):
            counts_test[cls] = len(os.listdir(test_path))
    
    return counts_train, counts_test


def plot_sample_images(dataset_path, classes, num_per_class=2, figsize=(16, 8)):
    """
    Plot sample images from each class
    
    Args:
        dataset_path: Path to dataset
        classes: List of class names
        num_per_class: Number of samples per class
        figsize: Figure size
    """
    
    fig, axes = plt.subplots(num_per_class, len(classes), figsize=figsize)
    fig.suptitle('Sample Images by Tumor Type', fontsize=16, fontweight='bold')
    
    for cls_idx, cls in enumerate(classes):
        cls_path = os.path.join(dataset_path, 'Train', cls)
        
        if os.path.exists(cls_path):
            images = os.listdir(cls_path)[:num_per_class]
            
            for img_idx, img_name in enumerate(images):
                img_path = os.path.join(cls_path, img_name)
                
                try:
                    img = Image.open(img_path)
                    ax = axes[img_idx, cls_idx]
                    ax.imshow(img, cmap='gray')
                    ax.set_title(f'{cls.upper()}\n{img_name[:20]}...', 
                                fontsize=10, fontweight='bold')
                    ax.axis('off')
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
    
    plt.tight_layout()
    plt.show()


def create_results_directory(results_path):
    """
    Create results directory structure
    
    Args:
        results_path: Path to results directory
    """
    
    os.makedirs(os.path.join(results_path, 'models'), exist_ok=True)
    os.makedirs(os.path.join(results_path, 'plots'), exist_ok=True)
    print(f"✅ Results directory created at: {results_path}")


def format_class_name(class_name):
    """
    Format class name for display
    
    Args:
        class_name: Raw class name
    
    Returns:
        Formatted class name
    """
    
    return class_name.replace('_', ' ').title()


def get_confidence_level(confidence):
    """
    Interpret confidence level
    
    Args:
        confidence: Confidence score (0-1)
    
    Returns:
        Confidence level description
    """
    
    if confidence > 0.9:
        return "Very High"
    elif confidence > 0.7:
        return "High"
    elif confidence > 0.5:
        return "Medium"
    else:
        return "Low"
