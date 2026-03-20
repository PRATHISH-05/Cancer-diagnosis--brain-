"""
Evaluation Module
Responsible for:
- Evaluating model on test data
- Generating confusion matrix
- Computing precision, recall, accuracy
- Class-wise performance analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (confusion_matrix, classification_report, 
                             accuracy_score, precision_score, recall_score, f1_score)


def evaluate_model(model, test_gen):
    """
    Evaluate model on test data
    
    Args:
        model: Trained Keras model
        test_gen: Test data generator
    
    Returns:
        loss, accuracy, recall
    """
    
    print("\n" + "="*60)
    print("EVALUATING MODEL ON TEST DATA")
    print("="*60)
    
    loss, accuracy, recall = model.evaluate(test_gen, verbose=0)
    
    print(f"Test Loss:          {loss:.4f}")
    print(f"Test Accuracy:      {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Test Recall:        {recall:.4f} ({recall*100:.2f}%)")
    print("="*60)
    
    return loss, accuracy, recall


def get_predictions(model, test_gen):
    """
    Get predictions on entire test set
    
    Args:
        model: Trained Keras model
        test_gen: Test data generator
    
    Returns:
        predictions, true_labels
    """
    
    print("\n🔄 Getting predictions on all test images...")
    predictions = model.predict(test_gen, verbose=0)
    predicted_classes = np.argmax(predictions, axis=1)
    true_labels = test_gen.classes
    
    print(f"✅ Predictions ready. Total samples: {len(true_labels)}")
    
    return predictions, predicted_classes, true_labels


def print_classification_report(true_labels, predicted_classes, class_names):
    """
    Print detailed classification report
    
    Args:
        true_labels: Ground truth labels
        predicted_classes: Predicted labels
        class_names: List of class names
    """
    
    print("\n" + "="*60)
    print("DETAILED CLASSIFICATION REPORT")
    print("="*60 + "\n")
    
    report = classification_report(true_labels, predicted_classes, 
                                   target_names=class_names,
                                   digits=4)
    print(report)


def print_recall_analysis(true_labels, predicted_classes, class_names):
    """
    Print per-class recall analysis (medical priority)
    
    Args:
        true_labels: Ground truth labels
        predicted_classes: Predicted labels
        class_names: List of class names
    """
    
    recall_per_class = recall_score(true_labels, predicted_classes, 
                                     average=None, 
                                     labels=np.arange(len(class_names)))
    
    print("\n" + "="*60)
    print("RECALL PER CLASS (MEDICAL PRIORITY)")
    print("="*60)
    
    for i, cls_name in enumerate(class_names):
        recall = recall_per_class[i]
        status = "✅ GOOD" if recall > 0.85 else "⚠️ WARNING" if recall > 0.70 else "🚨 CRITICAL"
        print(f"{cls_name.upper():12} Recall: {recall:.4f} ({recall*100:.2f}%) {status}")
    
    print("\n💡 Recall = % of ACTUAL tumors we correctly identified")
    print("   Medical Goal: All recalls > 0.85")


def plot_confusion_matrix(true_labels, predicted_classes, class_names, save_path=None):
    """
    Generate and plot confusion matrix
    
    Args:
        true_labels: Ground truth labels
        predicted_classes: Predicted labels
        class_names: List of class names
        save_path: Optional path to save figure
    """
    
    cm = confusion_matrix(true_labels, predicted_classes)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, 
                yticklabels=class_names,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix - Test Set', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Confusion matrix saved to: {save_path}")
    
    plt.show()
    
    # Print interpretation
    print("\n" + "="*60)
    print("CONFUSION MATRIX INTERPRETATION")
    print("="*60)
    
    for i, true_cls in enumerate(class_names):
        print(f"\n{true_cls.upper()} (Actual):")
        total_actual = cm[i].sum()
        correct = cm[i, i]
        
        print(f"  Total actual {true_cls} samples: {total_actual}")
        print(f"  Correctly identified: {correct} ({correct/total_actual*100:.1f}%)")
        
        confusions = [(class_names[j], cm[i, j]) 
                      for j in range(len(class_names)) if i != j and cm[i, j] > 0]
        
        if confusions:
            confusions.sort(key=lambda x: x[1], reverse=True)
            print(f"  Most confused with: {confusions[0][0]} ({confusions[0][1]} times)")
        else:
            print(f"  ✅ Never confused with other classes!")
    
    return cm
