"""
Test suite for churn prediction API
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


# Fixtures
@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    data = {
        'gender': ['Male', 'Female'],
        'SeniorCitizen': [0, 1],
        'Partner': ['Yes', 'No'],
        'Dependents': ['No', 'Yes'],
        'tenure': [12, 24],
        'PhoneService': ['Yes', 'Yes'],
        'MultipleLines': ['No', 'Yes'],
        'InternetService': ['DSL', 'Fiber optic'],
        'OnlineSecurity': ['Yes', 'No'],
        'OnlineBackup': ['Yes', 'No'],
        'DeviceProtection': ['No', 'Yes'],
        'TechSupport': ['No', 'Yes'],
        'StreamingTV': ['No', 'Yes'],
        'StreamingMovies': ['No', 'Yes'],
        'Contract': ['One year', 'Month-to-month'],
        'PaperlessBilling': ['Yes', 'Yes'],
        'PaymentMethod': ['Electronic check', 'Credit card'],
        'MonthlyCharges': [50.0, 80.0],
        'TotalCharges': [600.0, 1920.0],
        'Churn': [0, 1]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_features():
    """Create sample features for single prediction"""
    return {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'Yes',
        'Dependents': 'No',
        'tenure': 12,
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'One year',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'MonthlyCharges': 50.5,
        'TotalCharges': 600.0
    }


# Test Data Preprocessing
class TestDataPreprocessing:
    """Test data preprocessing functions"""
    
    def test_load_data(self, sample_data):
        """Test data loading"""
        assert len(sample_data) == 2
        assert 'Churn' in sample_data.columns
    
    def test_clean_data(self, sample_data):
        """Test data cleaning"""
        from src.features.preprocessing import DataPreprocessor
        from src.utils.config_loader import load_config
        
        config = load_config()
        preprocessor = DataPreprocessor(config)
        df_cleaned = preprocessor.clean_data(sample_data)
        
        assert 'customerID' not in df_cleaned.columns
        assert df_cleaned['Churn'].dtype in [int, np.int64]
    
    def test_encoding(self, sample_data):
        """Test categorical encoding"""
        from src.features.preprocessing import DataPreprocessor
        from src.utils.config_loader import load_config
        
        config = load_config()
        preprocessor = DataPreprocessor(config)
        df_cleaned = preprocessor.clean_data(sample_data)
        df_encoded = preprocessor.encode_categorical(df_cleaned, fit=True)
        
        # Check that categorical columns are numeric
        assert df_encoded['gender'].dtype in [int, np.int64]


# Test Feature Engineering
class TestFeatureEngineering:
    """Test feature engineering"""
    
    def test_tenure_buckets(self, sample_data):
        """Test tenure bucket creation"""
        from src.features.feature_engineering import FeatureEngineer
        
        engineer = FeatureEngineer()
        df_engineered = engineer.create_tenure_buckets(sample_data)
        
        assert 'tenure_bucket' in df_engineered.columns
    
    def test_charge_ratios(self, sample_data):
        """Test charge ratio features"""
        from src.features.feature_engineering import FeatureEngineer
        
        engineer = FeatureEngineer()
        df_engineered = engineer.create_charge_ratios(sample_data)
        
        assert 'avg_monthly_charges' in df_engineered.columns or \
               'charge_ratio' in df_engineered.columns


# Test Model Training
class TestModelTraining:
    """Test model training"""
    
    def test_model_initialization(self):
        """Test model initialization"""
        from src.models.train import ChurnModelTrainer
        from src.utils.config_loader import load_config
        
        config = load_config()
        trainer = ChurnModelTrainer(config)
        
        model = trainer.get_model('xgboost')
        assert model is not None
    
    @pytest.mark.skipif(not Path('data/processed/train.csv').exists(),
                       reason="Processed data not available")
    def test_model_training(self):
        """Test model training"""
        from src.models.train import ChurnModelTrainer
        from src.utils.config_loader import load_config
        import pandas as pd
        
        config = load_config()
        train_df = pd.read_csv('data/processed/train.csv')
        
        X_train = train_df.drop('Churn', axis=1)
        y_train = train_df['Churn']
        
        trainer = ChurnModelTrainer(config)
        trainer.model_type = 'logistic_regression'
        model = trainer.train(X_train.head(100), y_train.head(100))
        
        assert model is not None
        assert hasattr(model, 'predict')


# Test Model Prediction
class TestModelPrediction:
    """Test model prediction"""
    
    @pytest.mark.skipif(not Path('data/models/best_model.pkl').exists(),
                       reason="Trained model not available")
    def test_prediction(self, sample_features):
        """Test single prediction"""
        from src.models.predict import ChurnPredictor
        
        predictor = ChurnPredictor(
            'data/models/best_model.pkl',
            'data/models/preprocessor.pkl'
        )
        
        result = predictor.predict_single(sample_features)
        
        assert 'churn_prediction' in result
        assert 'churn_probability' in result
        assert result['churn_prediction'] in [0, 1]
        assert 0 <= result['churn_probability'] <= 1


# Test API
class TestAPI:
    """Test FastAPI endpoints"""
    
    @pytest.mark.skipif(not Path('data/models/best_model.pkl').exists(),
                       reason="Trained model not available")
    def test_health_endpoint(self):
        """Test health check endpoint"""
        from fastapi.testclient import TestClient
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        assert "status" in response.json()
    
    @pytest.mark.skipif(not Path('data/models/best_model.pkl').exists(),
                       reason="Trained model not available")
    def test_predict_endpoint(self, sample_features):
        """Test prediction endpoint"""
        from fastapi.testclient import TestClient
        from src.api.main import app
        
        client = TestClient(app)
        response = client.post("/predict", json=sample_features)
        
        assert response.status_code == 200
        data = response.json()
        assert "churn_prediction" in data
        assert "churn_probability" in data


# Test Monitoring
class TestMonitoring:
    """Test monitoring functions"""
    
    def test_log_prediction(self):
        """Test prediction logging"""
        from src.monitoring.drift_detection import ModelMonitor
        
        monitor = ModelMonitor()
        monitor.log_prediction(
            features={'tenure': 12},
            prediction=1,
            probability=0.75,
            duration=0.1
        )
        
        assert len(monitor.predictions_log) == 1
        assert monitor.predictions_log[0]['prediction'] == 1


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
