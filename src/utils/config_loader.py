"""
Configuration loader utility
"""
import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Dictionary containing configuration
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def get_data_paths(config: Dict[str, Any]) -> Dict[str, Path]:
    """
    Extract data paths from config
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of Path objects
    """
    data_config = config.get('data', {})
    
    return {
        'raw': Path(data_config.get('raw_data_path', 'data/raw')),
        'processed': Path(data_config.get('processed_data_path', 'data/processed')),
        'models': Path(data_config.get('models_path', 'data/models'))
    }


def get_model_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract model configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Model configuration dictionary
    """
    return config.get('model', {})


if __name__ == "__main__":
    # Test loading config
    config = load_config()
    print("✅ Configuration loaded successfully")
    print(f"Model algorithm: {config['model']['algorithm']}")
    print(f"Train/test split: {config['data']['train_test_split']}")
