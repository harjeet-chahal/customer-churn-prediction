"""
Model training with MLflow experiment tracking
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib
from typing import Dict, Any, Tuple

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import mlflow
import mlflow.sklearn
import mlflow.xgboost

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_loader import load_config
from src.features.preprocessing import DataPreprocessor

logger = setup_logger(__name__)


class ChurnModelTrainer:
    """Train and evaluate churn prediction models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.model_type = config['model']['algorithm']
        
    def get_model(self, model_type: str = None):
        """Get model instance based on type"""
        if model_type is None:
            model_type = self.model_type
            
        hyperparams = self.config['model']['hyperparameters']
        
        if model_type == 'xgboost':
            return XGBClassifier(**hyperparams['xgboost'])
        elif model_type == 'random_forest':
            return RandomForestClassifier(**hyperparams['random_forest'])
        elif model_type == 'logistic_regression':
            return LogisticRegression(max_iter=1000, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """Train the model"""
        logger.info(f"Training {self.model_type} model...")
        
        self.model = self.get_model()
        self.model.fit(X_train, y_train)
        
        logger.info("Training complete")
        return self.model
    
    def evaluate(
        self, 
        X_test: pd.DataFrame, 
        y_test: pd.Series
    ) -> Dict[str, float]:
        """Evaluate model performance"""
        logger.info("Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        logger.info("Evaluation metrics:")
        for metric, value in metrics.items():
            logger.info(f"  {metric}: {value:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        logger.info(f"\nConfusion Matrix:\n{cm}")
        
        # Classification report
        logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
        
        return metrics
    
    def save_model(self, filepath: str):
        """Save trained model"""
        logger.info(f"Saving model to {filepath}")
        joblib.dump(self.model, filepath)
    
    def load_model(self, filepath: str):
        """Load trained model"""
        logger.info(f"Loading model from {filepath}")
        self.model = joblib.load(filepath)


def train_with_mlflow(config: Dict[str, Any]):
    """Train model with MLflow tracking"""
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
    mlflow.set_experiment(config['mlflow']['experiment_name'])
    
    # Load processed data
    processed_dir = Path(config['data']['processed_data_path']).parent
    train_df = pd.read_csv(processed_dir / 'train.csv')
    test_df = pd.read_csv(processed_dir / 'test.csv')
    
    target_col = config['features']['target']
    X_train = train_df.drop(target_col, axis=1)
    y_train = train_df[target_col]
    X_test = test_df.drop(target_col, axis=1)
    y_test = test_df[target_col]
    
    logger.info(f"Loaded training data: {X_train.shape}")
    logger.info(f"Loaded test data: {X_test.shape}")
    
    # Train models
    model_types = ['logistic_regression', 'random_forest', 'xgboost']
    best_model = None
    best_score = 0
    best_model_type = None
    
    for model_type in model_types:
        logger.info(f"\n{'='*60}")
        logger.info(f"Training {model_type}")
        logger.info(f"{'='*60}")
        
        with mlflow.start_run(run_name=f"churn_{model_type}"):
            # Log parameters
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("train_samples", len(X_train))
            mlflow.log_param("test_samples", len(X_test))
            
            # Train
            trainer = ChurnModelTrainer(config)
            trainer.model_type = model_type
            trainer.train(X_train, y_train)
            
            # Evaluate
            metrics = trainer.evaluate(X_test, y_test)
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log model
            if model_type == 'xgboost':
                mlflow.xgboost.log_model(trainer.model, "model")
            else:
                mlflow.sklearn.log_model(trainer.model, "model")
            
            # Track best model
            if metrics['roc_auc'] > best_score:
                best_score = metrics['roc_auc']
                best_model = trainer.model
                best_model_type = model_type
            
            logger.info(f"✅ {model_type} training complete")
    
    # Save best model
    logger.info(f"\n{'='*60}")
    logger.info(f"Best model: {best_model_type} (ROC-AUC: {best_score:.4f})")
    logger.info(f"{'='*60}")
    
    models_dir = Path(config['data']['models_path'])
    models_dir.mkdir(parents=True, exist_ok=True)
    best_model_path = models_dir / 'best_model.pkl'
    joblib.dump(best_model, best_model_path)
    
    # Save model metadata
    metadata = {
        'model_type': best_model_type,
        'roc_auc': best_score,
        'features': list(X_train.columns)
    }
    import json
    with open(models_dir / 'model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Saved best model to {best_model_path}")
    logger.info("✅ Training pipeline complete!")
    
    return best_model, best_model_type, best_score


def main():
    """Main training pipeline"""
    config = load_config()
    
    # Check if processed data exists
    processed_dir = Path(config['data']['processed_data_path']).parent
    if not (processed_dir / 'train.csv').exists():
        logger.info("Processed data not found. Running preprocessing first...")
        from src.features.preprocessing import main as preprocess_main
        preprocess_main()
    
    # Train with MLflow
    train_with_mlflow(config)


if __name__ == "__main__":
    main()
