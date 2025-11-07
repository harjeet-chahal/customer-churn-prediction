"""
Model prediction module
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import joblib
from typing import Dict, Any, List
import json

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_loader import load_config

logger = setup_logger(__name__)


class ChurnPredictor:
    """Make predictions using trained model"""
    
    def __init__(self, model_path: str, preprocessor_path: str = None):
        self.model = joblib.load(model_path)
        
        # Load preprocessor
        if preprocessor_path and Path(preprocessor_path).exists():
            preprocessor_data = joblib.load(preprocessor_path)
            self.scaler = preprocessor_data['scaler']
            self.label_encoders = preprocessor_data['label_encoders']
        else:
            self.scaler = None
            self.label_encoders = {}
        
        # Load model metadata
        metadata_path = Path(model_path).parent / 'model_metadata.json'
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
        
        logger.info(f"Loaded model: {self.metadata.get('model_type', 'unknown')}")
        logger.info(f"Model ROC-AUC: {self.metadata.get('roc_auc', 'N/A')}")
    
    def preprocess_features(self, features: Dict[str, Any]) -> pd.DataFrame:
        """Preprocess raw features before prediction"""
        df = pd.DataFrame([features])
        
        # Encode categorical features
        for col, le in self.label_encoders.items():
            if col in df.columns:
                try:
                    # Handle unseen categories
                    if df[col].iloc[0] not in le.classes_:
                        # Use most common class
                        df[col] = le.transform([le.classes_[0]])
                    else:
                        df[col] = le.transform(df[col])
                except Exception as e:
                    logger.warning(f"Error encoding {col}: {e}")
                    df[col] = 0
        
        # Scale numeric features if scaler exists
        if self.scaler:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        
        return df
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict churn labels"""
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict churn probabilities"""
        return self.model.predict_proba(X)[:, 1]
    
    def predict_single(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict for a single customer"""
        # Preprocess features
        df = self.preprocess_features(features)
        
        # Predict
        prediction = self.predict(df)[0]
        probability = self.predict_proba(df)[0]
        
        result = {
            'churn_prediction': int(prediction),
            'churn_probability': float(probability),
            'risk_level': self._get_risk_level(probability),
            'features': features
        }
        
        return result
    
    def _get_risk_level(self, probability: float) -> str:
        """Categorize risk level based on probability"""
        if probability < 0.3:
            return 'low'
        elif probability < 0.6:
            return 'medium'
        elif probability < 0.8:
            return 'high'
        else:
            return 'very_high'
