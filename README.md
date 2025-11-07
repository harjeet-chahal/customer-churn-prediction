# ML Churn Prediction - MLOps Project

An end-to-end MLOps pipeline for customer churn prediction with automated training, deployment, monitoring, and retraining.

## 🎯 Project Overview

This project demonstrates production-grade ML system architecture including:
- **Automated ML Pipeline**: Training, evaluation, and model registry
- **REST API**: FastAPI-based model serving
- **CI/CD**: Automated testing and deployment
- **Monitoring**: Real-time performance tracking and drift detection
- **Orchestration**: Automated retraining workflows
- **Cloud Deployment**: Production-ready infrastructure

## 📊 Business Problem

Predict customer churn to enable proactive retention strategies. The model identifies customers likely to cancel their subscription in the next 30 days.

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Data      │─────▶│   Training   │─────▶│   Model     │
│   Sources   │      │   Pipeline   │      │   Registry  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            ▼                      ▼
                     ┌──────────────┐      ┌─────────────┐
                     │  Experiment  │      │  API        │
                     │  Tracking    │      │  Service    │
                     └──────────────┘      └─────────────┘
                                                  │
                                                  ▼
                                           ┌─────────────┐
                                           │ Monitoring  │
                                           │ & Alerting  │
                                           └─────────────┘
```

## 🚀 Features

### Phase 1: Model Development ✅
- [x] Data exploration and EDA
- [x] Feature engineering pipeline
- [x] Model training with hyperparameter tuning
- [x] Experiment tracking with MLflow
- [x] Model versioning with DVC

### Phase 2: API Development
- [ ] FastAPI REST endpoints
- [ ] Input validation with Pydantic
- [ ] Batch prediction support
- [ ] Docker containerization

### Phase 3: CI/CD
- [ ] GitHub Actions workflows
- [ ] Automated testing (unit, integration)
- [ ] Code quality checks
- [ ] Automated deployment

### Phase 4: Cloud Deployment
- [ ] Infrastructure as Code (Terraform)
- [ ] Cloud deployment (AWS/GCP)
- [ ] Load balancing
- [ ] Orchestration with Airflow

### Phase 5: Monitoring
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Data drift detection (Evidently)
- [ ] Alerting system

### Phase 6: Automated Retraining
- [ ] Scheduled retraining pipeline
- [ ] Performance-triggered retraining
- [ ] A/B testing framework
- [ ] Model rollback capability

## 📁 Project Structure

```
ml-churn-prediction/
├── data/
│   ├── raw/              # Original data
│   ├── processed/        # Cleaned & transformed data
│   └── models/           # Saved models
├── notebooks/
│   └── exploration.ipynb # EDA and experimentation
├── src/
│   ├── features/         # Feature engineering
│   ├── models/           # Model training & evaluation
│   ├── api/              # FastAPI application
│   ├── monitoring/       # Drift detection & metrics
│   └── utils/            # Helper functions
├── tests/                # Unit and integration tests
├── airflow_dags/         # Airflow workflow definitions
├── terraform/            # Infrastructure as Code
├── .github/workflows/    # CI/CD pipelines
├── config/               # Configuration files
├── requirements.txt      # Python dependencies
└── README.md
```

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Git
- AWS/GCP account (for deployment)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ml-churn-prediction
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate   # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Download dataset**
```bash
# Instructions coming soon
```

## 📊 Dataset

**Telco Customer Churn Dataset**
- **Source**: Kaggle
- **Size**: 7,043 customers
- **Features**: 21 (tenure, contract type, monthly charges, etc.)
- **Target**: Binary churn label

## 🎯 Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | TBD |
| Precision | TBD |
| Recall | TBD |
| F1 Score | TBD |
| ROC AUC | TBD |

## 🔄 Usage

### Training
```bash
python src/models/train.py --config config/config.yaml
```

### API (Local)
```bash
uvicorn src.api.main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"tenure": 12, "monthly_charges": 50.0, ...}'
```

### Run Tests
```bash
pytest tests/ -v --cov=src
```

## 🐳 Docker

```bash
# Build image
docker build -t ml-churn-api .

# Run container
docker run -p 8000:8000 ml-churn-api
```

## 📈 Monitoring

Access monitoring dashboards:
- **MLflow**: http://localhost:5000
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Dataset from Kaggle
- Inspired by production ML systems at leading tech companies
- Built with modern MLOps best practices

## 📚 Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DVC Documentation](https://dvc.org/doc)
- [Evidently AI Documentation](https://docs.evidentlyai.com/)

---

⭐ **Star this repo if you find it helpful!**
