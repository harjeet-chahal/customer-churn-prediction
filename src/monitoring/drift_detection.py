"""
Monitoring and drift detection
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from typing import Dict, Any
from datetime import datetime
import json

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger import setup_logger
from src.utils.config_loader import load_config

logger = setup_logger(__name__)


# Prometheus metrics
prediction_counter = Counter('predictions_total', 'Total number of predictions')
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration')
churn_predictions = Counter('churn_predictions_total', 'Total churn predictions', ['label'])
model_accuracy = Gauge('model_accuracy', 'Model accuracy')
data_drift_score = Gauge('data_drift_score', 'Data drift score')


class ModelMonitor:
    """Monitor model performance and data drift"""
    
    def __init__(self, reference_data: pd.DataFrame = None):
        """
        Initialize monitor
        
        Args:
            reference_data: Reference dataset for drift detection
        """
        self.reference_data = reference_data
        self.predictions_log = []
        
    def log_prediction(
        self,
        features: Dict[str, Any],
        prediction: int,
        probability: float,
        duration: float = None
    ):
        """Log a prediction for monitoring"""
        
        # Update Prometheus metrics
        prediction_counter.inc()
        churn_predictions.labels(label=str(prediction)).inc()
        
        if duration:
            prediction_duration.observe(duration)
        
        # Store prediction
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'prediction': prediction,
            'probability': probability,
            'duration': duration
        }
        
        self.predictions_log.append(log_entry)
        
        logger.debug(f"Logged prediction: churn={prediction}, prob={probability:.3f}")
    
    def check_data_drift(
        self,
        current_data: pd.DataFrame,
        save_report: bool = True,
        output_dir: str = 'monitoring/reports'
    ) -> Dict[str, Any]:
        """
        Check for data drift
        
        Args:
            current_data: Current production data
            save_report: Whether to save HTML report
            output_dir: Directory to save reports
            
        Returns:
            Drift detection results
        """
        if self.reference_data is None:
            logger.warning("No reference data provided. Cannot detect drift.")
            return {}
        
        logger.info("Checking for data drift...")
        
        # Create drift report
        report = Report(metrics=[
            DataDriftPreset(),
            DataQualityPreset()
        ])
        
        report.run(
            reference_data=self.reference_data,
            current_data=current_data
        )
        
        # Save report
        if save_report:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = output_path / f'drift_report_{timestamp}.html'
            report.save_html(str(report_file))
            
            logger.info(f"Saved drift report to {report_file}")
        
        # Extract metrics
        report_dict = report.as_dict()
        
        # Get drift score
        drift_detected = False
        drift_score = 0.0
        
        try:
            metrics = report_dict.get('metrics', [])
            for metric in metrics:
                if 'DatasetDriftMetric' in str(metric):
                    drift_detected = metric.get('result', {}).get('dataset_drift', False)
                    drift_score = metric.get('result', {}).get('drift_score', 0.0)
                    break
        except Exception as e:
            logger.error(f"Error extracting drift metrics: {e}")
        
        # Update Prometheus metric
        data_drift_score.set(drift_score)
        
        result = {
            'drift_detected': drift_detected,
            'drift_score': drift_score,
            'timestamp': datetime.now().isoformat(),
            'report_path': str(report_file) if save_report else None
        }
        
        if drift_detected:
            logger.warning(f"⚠️  Data drift detected! Score: {drift_score:.4f}")
        else:
            logger.info(f"✅ No significant drift detected. Score: {drift_score:.4f}")
        
        return result
    
    def calculate_performance_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict[str, float]:
        """Calculate current model performance"""
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score, 
            f1_score, roc_auc_score
        )
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1_score': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_pred_proba)
        }
        
        # Update Prometheus
        model_accuracy.set(metrics['accuracy'])
        
        logger.info("Performance metrics:")
        for name, value in metrics.items():
            logger.info(f"  {name}: {value:.4f}")
        
        return metrics
    
    def save_monitoring_log(self, filepath: str):
        """Save predictions log to file"""
        with open(filepath, 'w') as f:
            json.dump(self.predictions_log, f, indent=2)
        
        logger.info(f"Saved monitoring log to {filepath}")
    
    def load_monitoring_log(self, filepath: str):
        """Load predictions log from file"""
        with open(filepath, 'r') as f:
            self.predictions_log = json.load(f)
        
        logger.info(f"Loaded monitoring log from {filepath}")


def start_metrics_server(port: int = 8001):
    """Start Prometheus metrics server"""
    try:
        start_http_server(port)
        logger.info(f"✅ Metrics server started on port {port}")
        logger.info(f"Metrics available at http://localhost:{port}/metrics")
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")


def main():
    """Test monitoring"""
    config = load_config()
    
    # Load reference data
    processed_dir = Path(config['data']['processed_data_path']).parent
    train_df = pd.read_csv(processed_dir / 'train.csv')
    test_df = pd.read_csv(processed_dir / 'test.csv')
    
    # Initialize monitor
    monitor = ModelMonitor(reference_data=train_df.drop('Churn', axis=1))
    
    # Check drift
    drift_result = monitor.check_data_drift(
        test_df.drop('Churn', axis=1),
        output_dir='monitoring/reports'
    )
    
    logger.info(f"Drift detection result: {drift_result}")
    
    # Start metrics server (in background)
    # start_metrics_server(port=8001)
    
    logger.info("✅ Monitoring test complete!")


if __name__ == "__main__":
    main()
