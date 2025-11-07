"""
Feature engineering for churn prediction
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class FeatureEngineer:
    """Create and transform features"""
    
    def __init__(self):
        pass
    
    def create_tenure_buckets(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create tenure categories"""
        df = df.copy()
        if 'tenure' in df.columns:
            df['tenure_bucket'] = pd.cut(
                df['tenure'],
                bins=[0, 12, 24, 48, 72],
                labels=['0-1yr', '1-2yr', '2-4yr', '4yr+']
            )
            logger.info("Created tenure buckets")
        return df
    
    def create_charge_ratios(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create charge-related features"""
        df = df.copy()
        
        if 'MonthlyCharges' in df.columns and 'tenure' in df.columns:
            # Average charges per month
            df['avg_monthly_charges'] = df['MonthlyCharges'] / (df['tenure'] + 1)
            
        if 'TotalCharges' in df.columns and 'MonthlyCharges' in df.columns:
            # Ratio of total to monthly
            df['charge_ratio'] = df['TotalCharges'] / (df['MonthlyCharges'] + 1)
            
        logger.info("Created charge ratio features")
        return df
    
    def create_service_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features from service columns"""
        df = df.copy()
        
        # Count of services
        service_cols = [
            'PhoneService', 'MultipleLines', 'InternetService',
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
            'TechSupport', 'StreamingTV', 'StreamingMovies'
        ]
        
        available_services = [col for col in service_cols if col in df.columns]
        if available_services:
            df['total_services'] = df[available_services].apply(
                lambda row: sum(row.astype(str).str.contains('Yes|DSL|Fiber')), axis=1
            )
            logger.info("Created service count features")
        
        return df
    
    def create_customer_segments(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create customer segments"""
        df = df.copy()
        
        if 'MonthlyCharges' in df.columns and 'tenure' in df.columns:
            # High value customers
            df['high_value'] = (
                (df['MonthlyCharges'] > df['MonthlyCharges'].median()) &
                (df['tenure'] > df['tenure'].median())
            ).astype(int)
            
            # New high spenders (churn risk)
            df['new_high_spender'] = (
                (df['MonthlyCharges'] > df['MonthlyCharges'].quantile(0.75)) &
                (df['tenure'] < 12)
            ).astype(int)
            
            logger.info("Created customer segments")
        
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features"""
        df = df.copy()
        
        if 'Contract' in df.columns and 'MonthlyCharges' in df.columns:
            # Contract-charge interaction
            df['contract_charge'] = df['Contract'].astype(str) + '_' + \
                pd.cut(df['MonthlyCharges'], bins=3, labels=['low', 'med', 'high']).astype(str)
        
        logger.info("Created interaction features")
        return df
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run complete feature engineering pipeline"""
        logger.info("Running feature engineering pipeline...")
        
        df = self.create_tenure_buckets(df)
        df = self.create_charge_ratios(df)
        df = self.create_service_features(df)
        df = self.create_customer_segments(df)
        df = self.create_interaction_features(df)
        
        logger.info(f"Feature engineering complete. Final shape: {df.shape}")
        return df


def main():
    """Test feature engineering"""
    from src.utils.config_loader import load_config
    
    config = load_config()
    
    # Load raw data
    raw_data_path = config['data']['raw_data_path']
    df = pd.read_csv(raw_data_path)
    
    # Engineer features
    engineer = FeatureEngineer()
    df_engineered = engineer.engineer_features(df)
    
    logger.info(f"Original columns: {len(df.columns)}")
    logger.info(f"Engineered columns: {len(df_engineered.columns)}")
    logger.info(f"New features: {set(df_engineered.columns) - set(df.columns)}")
    
    logger.info("✅ Feature engineering test complete!")


if __name__ == "__main__":
    main()
