"""
FastAPI application for churn prediction
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
import joblib
import json
from datetime import datetime

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_loader import load_config
from src.models.predict import ChurnPredictor

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Churn Prediction API",
    description="API for predicting customer churn",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and config
predictor = None
config = None


# Pydantic models (keep all your existing models here)
class CustomerFeatures(BaseModel):
    """Customer features for prediction"""
    gender: str = Field(..., description="Customer gender")
    SeniorCitizen: int = Field(..., ge=0, le=1, description="Senior citizen flag")
    Partner: str = Field(..., description="Has partner")
    Dependents: str = Field(..., description="Has dependents")
    tenure: int = Field(..., ge=0, description="Months as customer")
    PhoneService: str = Field(..., description="Has phone service")
    MultipleLines: str = Field(..., description="Has multiple lines")
    InternetService: str = Field(..., description="Internet service type")
    OnlineSecurity: str = Field(..., description="Has online security")
    OnlineBackup: str = Field(..., description="Has online backup")
    DeviceProtection: str = Field(..., description="Has device protection")
    TechSupport: str = Field(..., description="Has tech support")
    StreamingTV: str = Field(..., description="Has streaming TV")
    StreamingMovies: str = Field(..., description="Has streaming movies")
    Contract: str = Field(..., description="Contract type")
    PaperlessBilling: str = Field(..., description="Has paperless billing")
    PaymentMethod: str = Field(..., description="Payment method")
    MonthlyCharges: float = Field(..., ge=0, description="Monthly charges")
    TotalCharges: float = Field(..., ge=0, description="Total charges")
    
    class Config:
        schema_extra = {
            "example": {
                "gender": "Female",
                "SeniorCitizen": 0,
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 12,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "DSL",
                "OnlineSecurity": "Yes",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "No",
                "StreamingMovies": "No",
                "Contract": "One year",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 50.5,
                "TotalCharges": 600.0
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    churn_prediction: int = Field(..., description="0 for no churn, 1 for churn")
    churn_probability: float = Field(..., description="Probability of churn")
    risk_level: str = Field(..., description="Risk level: low, medium, high, very_high")
    timestamp: str = Field(..., description="Prediction timestamp")


class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    customers: List[CustomerFeatures]


class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    predictions: List[PredictionResponse]
    total_customers: int
    high_risk_count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_type: Optional[str]
    model_version: Optional[str]
    timestamp: str


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global predictor, config
    
    logger.info("Starting API...")
    
    try:
        # Load config
        config = load_config()
        
        # Load model
        models_dir = Path(config['data']['models_path'])
        model_path = models_dir / 'best_model.pkl'
        preprocessor_path = models_dir / 'preprocessor.pkl'
        
        if not model_path.exists():
            logger.error("Model not found!")
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        predictor = ChurnPredictor(str(model_path), str(preprocessor_path))
        logger.info("✅ Model loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Churn Prediction API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_loaded = predictor is not None
    
    model_info = {}
    if model_loaded and predictor.metadata:
        model_info = {
            "model_type": predictor.metadata.get('model_type'),
            "model_version": predictor.metadata.get('roc_auc')
        }
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        model_type=model_info.get('model_type'),
        model_version=str(model_info.get('model_version')),
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(customer: CustomerFeatures):
    """Predict churn for a single customer"""
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        features = customer.dict()
        result = predictor.predict_single(features)
        
        return PredictionResponse(
            churn_prediction=result['churn_prediction'],
            churn_probability=result['churn_probability'],
            risk_level=result['risk_level'],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Predict churn for multiple customers"""
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        features_list = [customer.dict() for customer in request.customers]
        results = predictor.predict_batch(features_list)
        
        predictions = []
        high_risk_count = 0
        
        for result in results:
            predictions.append(PredictionResponse(
                churn_prediction=result['churn_prediction'],
                churn_probability=result['churn_probability'],
                risk_level=result['risk_level'],
                timestamp=datetime.now().isoformat()
            ))
            
            if result['risk_level'] in ['high', 'very_high']:
                high_risk_count += 1
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_customers=len(predictions),
            high_risk_count=high_risk_count
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/model/info")
async def model_info():
    """Get model information"""
    if predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return {
        "model_type": predictor.metadata.get('model_type', 'unknown'),
        "roc_auc": predictor.metadata.get('roc_auc', 'N/A'),
        "features": predictor.metadata.get('features', []),
        "loaded_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting server on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
