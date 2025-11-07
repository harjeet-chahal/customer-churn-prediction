"""
Script to download the Telco Customer Churn dataset
"""
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def download_dataset(output_path: str = "data/raw/telco_churn.csv"):
    """
    Download Telco Customer Churn dataset from public source
    
    Args:
        output_path: Where to save the dataset
    """
    logger.info("Downloading Telco Customer Churn dataset...")
    
    # URL for the dataset (from Kaggle's public datasets)
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    
    try:
        # Download dataset
        df = pd.read_csv(url)
        
        # Create output directory if it doesn't exist
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        logger.info(f"✅ Dataset downloaded successfully!")
        logger.info(f"📊 Shape: {df.shape}")
        logger.info(f"💾 Saved to: {output_file}")
        logger.info(f"\nFirst few rows:")
        print(df.head())
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error downloading dataset: {e}")
        raise


if __name__ == "__main__":
    download_dataset()
