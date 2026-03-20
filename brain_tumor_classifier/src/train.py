"""
Training Module
Responsible for:
- Compiling the model
- Training with proper callbacks
- Saving model
- Plotting training history
"""

import os
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.metrics import Recall


def compile_model(model, learning_rate=0.001):
    """
    Compile model with appropriate loss, optimizer, and metrics
    
    Args:
        model: Keras model
        learning_rate: Learning rate for Adam optimizer
    """
    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(learning_rate=learning_rate),
        metrics=['accuracy', Recall()]
    )
    
    print("✅ Model compiled!")
    print(f"Loss: categorical_crossentropy")
    print(f"Optimizer: Adam (lr={learning_rate})")
    print(f"Metrics: accuracy, recall")


def train_model(model, train_gen, val_gen, epochs=20, class_weight_dict=None):
    """
    Train the model
    
    Args:
        model: Compiled Keras model
        train_gen: Training data generator
        val_gen: Validation data generator
        epochs: Number of epochs
        class_weight_dict: Dictionary of class weights
    
    Returns:
        Training history
    """
    
    # Early stopping callback
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    print(f"\n🚀 Starting training for {epochs} epochs...")
    
    history = model.fit(
        train_gen,
        epochs=epochs,
        validation_data=val_gen,
        callbacks=[early_stop],
        class_weight=class_weight_dict,
        verbose=1
    )
    
    print("\n✅ Training complete!")
    return history


def plot_training_history(history, save_path=None):
    """
    Plot training and validation loss/accuracy
    
    Args:
        history: Training history object
        save_path: Optional path to save figure
    """
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss
    axes[0].plot(history.history['loss'], label='Training Loss', linewidth=2, marker='o')
    axes[0].plot(history.history['val_loss'], label='Validation Loss', linewidth=2, marker='s')
    axes[0].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Loss', fontsize=12)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)
    
    # Accuracy
    axes[1].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2, marker='o')
    axes[1].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2, marker='s')
    axes[1].set_title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Accuracy', fontsize=12)
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Training plot saved to: {save_path}")
    
    plt.show()


def save_model(model, save_path):
    """
    Save trained model
    
    Args:
        model: Trained Keras model
        save_path: Path to save model
    """
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    model.save(save_path)
    file_size_mb = os.path.getsize(save_path) / (1024*1024)
    
    print(f"\n✅ Model saved to: {save_path}")
    print(f"File size: {file_size_mb:.2f} MB")
