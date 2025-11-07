"""
Data preprocessing module for churn prediction
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_loader import load_config

logger = setup_logger(__name__)


class DataPreprocessor:
    """Handle all data preprocessing tasks"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_raw_data(self, filepath: str) -> pd.DataFrame:
        """Load raw data from CSV"""
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and fix data quality issues"""
        logger.info("Cleaning data...")
        df = df.copy()
        
        # Remove customer ID (not useful for prediction)
        if 'customerID' in df.columns:
            df = df.drop('customerID', axis=1)
        
        # Fix TotalCharges - convert to numeric
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            # Fill missing TotalCharges with 0 (new customers)
            df['TotalCharges'].fillna(0, inplace=True)
        
        # Convert target to binary
        if 'Churn' in df.columns:
            df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
        # Convert SeniorCitizen to categorical
        if 'SeniorCitizen' in df.columns:
            df['SeniorCitizen'] = df['SeniorCitizen'].astype(str)
        
        logger.info(f"Data cleaned. Shape: {df.shape}")
        return df
    
    def encode_categorical(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Encode categorical variables"""
        logger.info("Encoding categorical variables...")
        df = df.copy()
        
        # Get categorical columns (exclude target)
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if 'Churn' in categorical_cols:
            categorical_cols.remove('Churn')
        
        for col in categorical_cols:
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    # Handle unseen labels
                    le = self.label_encoders[col]
                    df[col] = df[col].map(lambda x: x if x in le.classes_ else 'Unknown')
                    df[col] = le.transform(df[col].astype(str))
        
        logger.info(f"Encoded {len(categorical_cols)} categorical columns")
        return df
    
    def scale_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Scale numeric features"""
        logger.info("Scaling numeric features...")
        df = df.copy()
        
        # Get numeric columns (exclude target)
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if 'Churn' in numeric_cols:
            numeric_cols.remove('Churn')
        
        if fit:
            df[numeric_cols] = self.scaler.fit_transform(df[numeric_cols])
        else:
            df[numeric_cols] = self.scaler.transform(df[numeric_cols])
        
        logger.info(f"Scaled {len(numeric_cols)} numeric columns")
        return df
    
    def preprocess(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Run complete preprocessing pipeline"""
        logger.info("Running preprocessing pipeline...")
        df = self.clean_data(df)
        df = self.encode_categorical(df, fit=fit)
        df = self.scale_features(df, fit=fit)
        logger.info("Preprocessing complete")
        return df
    
    def save_preprocessor(self, filepath: str):
        """Save scaler and encoders"""
        logger.info(f"Saving preprocessor to {filepath}")
        joblib.dump({
            'scaler': self.scaler,
            'label_encoders': self.label_encoders
        }, filepath)
    
    def load_preprocessor(self, filepath: str):
        """Load scaler and encoders"""
        logger.info(f"Loading preprocessor from {filepath}")
        data = joblib.load(filepath)
        self.scaler = data['scaler']
        self.label_encoders = data['label_encoders']


def prepare_train_test_split(
    df: pd.DataFrame,
    target_col: str = 'Churn',
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into train and test sets"""
    logger.info("Splitting data into train and test sets...")
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Train set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    logger.info(f"Churn rate in train: {y_train.mean():.2%}")
    logger.info(f"Churn rate in test: {y_test.mean():.2%}")
    
    return X_train, X_test, y_train, y_test


def main():
    """Main preprocessing pipeline"""
    # Load config
    config = load_config()
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor(config)
    
    # Load raw data
    raw_data_path = config['data']['raw_data_path']
    df = preprocessor.load_raw_data(raw_data_path)
    
    # Preprocess
    df_processed = preprocessor.preprocess(df, fit=True)
    
    # Split data
    X_train, X_test, y_train, y_test = prepare_train_test_split(
        df_processed,
        target_col=config['features']['target'],
        test_size=config['data']['train_test_split'],
        random_state=config['data']['random_state']
    )
    
    # Save processed data
    processed_dir = Path(config['data']['processed_data_path']).parent
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_path = processed_dir / 'train.csv'
    test_path = processed_dir / 'test.csv'
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    logger.info(f"Saved training data to {train_path}")
    logger.info(f"Saved test data to {test_path}")
    
    # Save preprocessor
    models_dir = Path(config['data']['models_path'])
    models_dir.mkdir(parents=True, exist_ok=True)
    preprocessor_path = models_dir / 'preprocessor.pkl'
    preprocessor.save_preprocessor(preprocessor_path)
    
    logger.info("✅ Preprocessing pipeline complete!")


if __name__ == "__main__":
    main()
