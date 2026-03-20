"""
Data Loader Module
Responsible for:
- Loading images from folder structure
- Resizing to fixed dimensions
- Normalization
- Data augmentation
- Train/validation/test generators
"""

import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from sklearn.utils.class_weight import compute_class_weight


class DataLoader:
    """Handles all data loading operations for brain tumor classification"""
    
    def __init__(self, dataset_path, img_size=224, batch_size=32):
        """
        Initialize data loader
        
        Args:
            dataset_path: Path to dataset folder
            img_size: Target image size (img_size × img_size)
            batch_size: Batch size for generators
        """
        self.dataset_path = dataset_path
        self.img_size = img_size
        self.batch_size = batch_size
        self.classes = ['glioma', 'meningioma', 'notumor', 'pituitary']
        
    def get_class_counts(self):
        """Count images per class"""
        counts = {}
        for cls in self.classes:
            cls_path = os.path.join(self.dataset_path, 'Train', cls)
            if os.path.exists(cls_path):
                counts[cls] = len(os.listdir(cls_path))
        return counts
    
    def compute_class_weights(self):
        """Compute class weights to handle imbalance"""
        train_classes = []
        class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        
        for cls in self.classes:
            cls_path = os.path.join(self.dataset_path, 'Train', cls)
            if os.path.exists(cls_path):
                count = len(os.listdir(cls_path))
                train_classes.extend([class_to_idx[cls]] * count)
        
        train_classes = np.array(train_classes)
        class_weights = compute_class_weight('balanced', 
                                             classes=np.unique(train_classes), 
                                             y=train_classes)
        return {i: w for i, w in enumerate(class_weights)}
    
    def create_generators(self):
        """
        Create ImageDataGenerators for training, validation, and testing
        
        Returns:
            train_gen, val_gen, test_gen
        """
        # Training generator WITH augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Validation/Test generator WITHOUT augmentation
        val_test_datagen = ImageDataGenerator(
            rescale=1./255
        )
        
        train_path = os.path.join(self.dataset_path, 'Train')
        test_path = os.path.join(self.dataset_path, 'Test')
        
        # Load generators
        train_gen = train_datagen.flow_from_directory(
            train_path,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            color_mode='grayscale',
            shuffle=True,
            seed=42
        )
        
        val_gen = val_test_datagen.flow_from_directory(
            train_path,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            color_mode='grayscale',
            shuffle=True,
            seed=42
        )
        
        test_gen = val_test_datagen.flow_from_directory(
            test_path,
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            color_mode='grayscale',
            shuffle=False
        )
        
        return train_gen, val_gen, test_gen
