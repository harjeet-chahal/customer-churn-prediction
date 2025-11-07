"""
Model evaluation and analysis
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve, precision_recall_curve
)

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_loader import load_config

logger = setup_logger(__name__)


class ModelEvaluator:
    """Evaluate and analyze model performance"""
    
    def __init__(self, model, X_test: pd.DataFrame, y_test: pd.Series):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.y_pred = None
        self.y_pred_proba = None
        
    def predict(self):
        """Generate predictions"""
        logger.info("Generating predictions...")
        self.y_pred = self.model.predict(self.X_test)
        self.y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
        
    def calculate_metrics(self) -> Dict[str, float]:
        """Calculate all evaluation metrics"""
        if self.y_pred is None:
            self.predict()
        
        metrics = {
            'accuracy': accuracy_score(self.y_test, self.y_pred),
            'precision': precision_score(self.y_test, self.y_pred),
            'recall': recall_score(self.y_test, self.y_pred),
            'f1_score': f1_score(self.y_test, self.y_pred),
            'roc_auc': roc_auc_score(self.y_test, self.y_pred_proba)
        }
        
        return metrics
    
    def plot_confusion_matrix(self, save_path: str = None):
        """Plot confusion matrix"""
        if self.y_pred is None:
            self.predict()
        
        cm = confusion_matrix(self.y_test, self.y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved confusion matrix to {save_path}")
        
        plt.close()
    
    def plot_roc_curve(self, save_path: str = None):
        """Plot ROC curve"""
        if self.y_pred_proba is None:
            self.predict()
        
        fpr, tpr, thresholds = roc_curve(self.y_test, self.y_pred_proba)
        auc = roc_auc_score(self.y_test, self.y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved ROC curve to {save_path}")
        
        plt.close()
    
    def plot_precision_recall_curve(self, save_path: str = None):
        """Plot precision-recall curve"""
        if self.y_pred_proba is None:
            self.predict()
        
        precision, recall, thresholds = precision_recall_curve(
            self.y_test, self.y_pred_proba
        )
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.grid(alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved PR curve to {save_path}")
        
        plt.close()
    
    def plot_feature_importance(self, feature_names: list, save_path: str = None, top_n: int = 20):
        """Plot feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            importances = np.abs(self.model.coef_[0])
        else:
            logger.warning("Model doesn't have feature importance")
            return
        
        # Get top N features
        indices = np.argsort(importances)[-top_n:]
        
        plt.figure(figsize=(10, 8))
        plt.barh(range(len(indices)), importances[indices])
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title(f'Top {top_n} Feature Importances')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved feature importance to {save_path}")
        
        plt.close()
    
    def generate_report(self, output_dir: str):
        """Generate complete evaluation report"""
        logger.info("Generating evaluation report...")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Calculate metrics
        metrics = self.calculate_metrics()
        
        # Save metrics
        import json
        with open(output_path / 'metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Generate plots
        self.plot_confusion_matrix(output_path / 'confusion_matrix.png')
        self.plot_roc_curve(output_path / 'roc_curve.png')
        self.plot_precision_recall_curve(output_path / 'pr_curve.png')
        
        if hasattr(self.model, 'feature_importances_') or hasattr(self.model, 'coef_'):
            self.plot_feature_importance(
                list(self.X_test.columns),
                output_path / 'feature_importance.png'
            )
        
        # Create report text
        report_lines = [
            "=" * 60,
            "MODEL EVALUATION REPORT",
            "=" * 60,
            "",
            "METRICS:",
            "-" * 60
        ]
        
        for metric, value in metrics.items():
            report_lines.append(f"{metric.upper()}: {value:.4f}")
        
        report_lines.extend([
            "",
            "CONFUSION MATRIX:",
            "-" * 60,
            str(confusion_matrix(self.y_test, self.y_pred)),
            "",
            "=" * 60
        ])
        
        report_text = "\n".join(report_lines)
        
        with open(output_path / 'evaluation_report.txt', 'w') as f:
            f.write(report_text)
        
        logger.info(f"✅ Evaluation report saved to {output_dir}")
        logger.info(report_text)


def main():
    """Main evaluation pipeline"""
    config = load_config()
    
    # Load test data
    processed_dir = Path(config['data']['processed_data_path']).parent
    test_df = pd.read_csv(processed_dir / 'test.csv')
    
    target_col = config['features']['target']
    X_test = test_df.drop(target_col, axis=1)
    y_test = test_df[target_col]
    
    # Load best model
    models_dir = Path(config['data']['models_path'])
    model_path = models_dir / 'best_model.pkl'
    
    if not model_path.exists():
        logger.error("Best model not found. Please train a model first.")
        return
    
    model = joblib.load(model_path)
    logger.info(f"Loaded model from {model_path}")
    
    # Evaluate
    evaluator = ModelEvaluator(model, X_test, y_test)
    evaluator.generate_report(models_dir / 'evaluation')
    
    logger.info("✅ Evaluation complete!")


if __name__ == "__main__":
    main()
