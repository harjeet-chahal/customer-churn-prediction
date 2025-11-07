# 🚀 COMPLETE MLOps PROJECT - READY TO USE!

## ✅ What You Have

Your **COMPLETE** end-to-end MLOps project with:
- ✅ Data preprocessing pipeline
- ✅ Feature engineering
- ✅ Model training with MLflow
- ✅ Model evaluation and metrics
- ✅ Prediction module
- ✅ FastAPI REST API
- ✅ Docker containerization  
- ✅ Docker Compose with monitoring
- ✅ Prometheus + Grafana monitoring
- ✅ Drift detection with Evidently
- ✅ Airflow retraining pipeline
- ✅ GitHub Actions CI/CD
- ✅ Complete test suite
- ✅ Makefile for easy commands

**ALL CODE IS COMPLETE AND READY TO RUN!**

---

## 🎯 Quick Start (5 Steps)

### **Step 1: Setup Environment**
```bash
cd ml-churn-prediction
source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt  # Takes 5-10 minutes
```

### **Step 2: Download Data**
```bash
make download-data
# OR
python src/utils/download_data.py
```

### **Step 3: Train Model**
```bash
make all
# This runs: preprocess → train → evaluate
```

### **Step 4: Start API**
```bash
make api
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### **Step 5: Test It!**
```bash
# Open http://localhost:8000/docs in browser
# Try the /predict endpoint with sample data
```

---

## 📚 Complete Command Reference

### **Using Makefile (Easiest)**
```bash
make help              # Show all commands
make install           # Install dependencies
make download-data     # Download dataset
make preprocess        # Preprocess data
make train             # Train models
make evaluate          # Evaluate models
make predict           # Test predictions
make api               # Start API (dev mode)
make api-prod          # Start API (production)
make test              # Run tests
make format            # Format code
make lint              # Lint code
make docker            # Run with Docker Compose
make mlflow            # Start MLflow UI
make clean             # Clean temporary files
make all               # Run complete pipeline
```

### **Direct Python Commands**
```bash
# Data pipeline
python src/utils/download_data.py
python src/features/preprocessing.py
python src/models/train.py
python src/models/evaluate.py
python src/models/predict.py

# API
uvicorn src.api.main:app --reload

# Monitoring
python src/monitoring/drift_detection.py
```

### **Docker Commands**
```bash
# Build image
docker build -t churn-api .

# Run container
docker run -p 8000:8000 churn-api

# Run with compose (includes monitoring)
docker-compose up --build

# Stop containers
docker-compose down
```

### **Testing**
```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_all.py -v

# Run fast tests only
pytest -m "not slow"
```

---

## 🏃 Complete Workflow

### **Development Workflow:**
```bash
# 1. Download data
make download-data

# 2. Run complete pipeline
make all
# This does: preprocess → train → evaluate

# 3. Start API
make api

# 4. Test in browser
# Open: http://localhost:8000/docs

# 5. Make predictions via API
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### **Production Workflow:**
```bash
# 1. Run tests
make test

# 2. Build Docker image
make docker-build

# 3. Run with monitoring
make docker

# 4. Access services:
# - API: http://localhost:8000
# - MLflow: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000
```

---

## 📊 What Each Module Does

### **1. Data Preprocessing** (`src/features/preprocessing.py`)
- Loads raw data
- Cleans missing values
- Encodes categorical variables
- Scales numeric features
- Splits train/test sets
- **Run:** `make preprocess`

### **2. Feature Engineering** (`src/features/feature_engineering.py`)
- Creates tenure buckets
- Calculates charge ratios
- Counts services
- Creates customer segments
- **Used automatically** during preprocessing

### **3. Model Training** (`src/models/train.py`)
- Trains 3 models: Logistic Regression, Random Forest, XGBoost
- Tracks experiments with MLflow
- Saves best model
- **Run:** `make train`
- **View experiments:** `make mlflow` → http://localhost:5000

### **4. Model Evaluation** (`src/models/evaluate.py`)
- Calculates metrics (accuracy, precision, recall, F1, ROC-AUC)
- Creates confusion matrix
- Plots ROC curve
- Shows feature importance
- **Run:** `make evaluate`
- **Results:** `data/models/evaluation/`

### **5. Model Prediction** (`src/models/predict.py`)
- Makes predictions on new data
- Returns probability and risk level
- Explains top influential features
- **Run:** `make predict`

### **6. FastAPI Application** (`src/api/main.py`)
- REST API for predictions
- Endpoints: `/predict`, `/predict/batch`, `/health`, `/model/info`
- Interactive docs at `/docs`
- **Run:** `make api`
- **Access:** http://localhost:8000/docs

### **7. Monitoring** (`src/monitoring/drift_detection.py`)
- Detects data drift with Evidently
- Prometheus metrics
- Performance tracking
- **Run:** `python src/monitoring/drift_detection.py`

### **8. Airflow DAG** (`airflow_dags/retraining_pipeline.py`)
- Automated retraining workflow
- Scheduled weekly (Sundays)
- Fetches → Validates → Trains → Evaluates → Deploys
- **Setup Airflow separately** (instructions below)

### **9. CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
- Runs tests on every push
- Builds Docker image
- Deploys to staging/production
- **Activates** when you push to GitHub

---

## 🧪 Testing Your Project

### **1. Unit Tests**
```bash
make test
```

### **2. API Tests**
```bash
# Start API first
make api

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/model/info

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

### **3. Integration Test (Full Pipeline)**
```bash
# Run complete pipeline
make clean              # Clean old files
make download-data      # Download data
make all                # Preprocess, train, evaluate
make test               # Run tests
make api                # Start API

# Everything should work!
```

---

## 🐳 Docker Deployment

### **Option 1: Simple Docker**
```bash
# Build
docker build -t churn-api .

# Run
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e ENVIRONMENT=production \
  churn-api

# Test
curl http://localhost:8000/health
```

### **Option 2: Docker Compose (with Monitoring)**
```bash
# Start everything
docker-compose up --build

# Services available:
# - API: http://localhost:8000
# - MLflow: http://localhost:5000  
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)

# Stop
docker-compose down
```

---

## 📈 Monitoring Setup

### **1. View MLflow Experiments**
```bash
make mlflow
# Open: http://localhost:5000
```

### **2. Check Prometheus Metrics**
```bash
# Start with docker-compose
docker-compose up prometheus

# Open: http://localhost:9090
```

### **3. View Grafana Dashboards**
```bash
# Start with docker-compose
docker-compose up grafana

# Open: http://localhost:3000
# Login: admin / admin
```

### **4. Drift Detection**
```bash
python src/monitoring/drift_detection.py
# Reports saved to: monitoring/reports/
```

---

## ☁️ Cloud Deployment (Optional)

### **AWS Deployment**
1. Build and push Docker image to ECR
2. Deploy to ECS/EKS
3. Use Terraform (in `terraform/` folder)

### **GCP Deployment**
1. Build and push to Container Registry
2. Deploy to Cloud Run
3. Use Terraform

### **DigitalOcean/Heroku**
Simpler options for quick deployment

---

## 🔄 Airflow Setup (Optional)

```bash
# Install Airflow
pip install apache-airflow

# Initialize database
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Start webserver
airflow webserver --port 8080

# Start scheduler (in another terminal)
airflow scheduler

# Access: http://localhost:8080
# Enable the "churn_model_retraining" DAG
```

---

## 🎓 Project Structure Explained

```
ml-churn-prediction/
├── src/
│   ├── features/          # Data preprocessing & feature engineering
│   │   ├── preprocessing.py      ← Clean and transform data
│   │   └── feature_engineering.py ← Create new features
│   ├── models/            # Model training and prediction
│   │   ├── train.py              ← Train models with MLflow
│   │   ├── evaluate.py           ← Evaluate and visualize
│   │   └── predict.py            ← Make predictions
│   ├── api/               # FastAPI application
│   │   └── main.py               ← REST API endpoints
│   ├── monitoring/        # Monitoring and drift detection
│   │   └── drift_detection.py    ← Monitor performance
│   └── utils/             # Utilities
│       ├── config_loader.py      ← Load config
│       ├── logger.py             ← Logging
│       └── download_data.py      ← Download dataset
├── tests/                 # Test suite
│   └── test_all.py               ← All tests
├── airflow_dags/          # Airflow workflows
│   └── retraining_pipeline.py    ← Automated retraining
├── .github/workflows/     # CI/CD
│   └── ci-cd.yml                 ← GitHub Actions
├── config/                # Configuration
│   └── config.yaml               ← All settings
├── data/                  # Data directories
│   ├── raw/                      ← Original data
│   ├── processed/                ← Processed data
│   └── models/                   ← Saved models
├── Dockerfile                    ← Container definition
├── docker-compose.yml            ← Multi-container setup
├── prometheus.yml                ← Monitoring config
├── Makefile                      ← Easy commands
├── requirements.txt              ← Dependencies
└── README.md                     ← Main documentation
```

---

## 🎯 Common Tasks

### **Retrain Model**
```bash
make download-data  # Get fresh data
make all            # Retrain everything
```

### **Deploy New Version**
```bash
make test           # Ensure tests pass
make docker-build   # Build image
make docker         # Deploy locally
# OR push to cloud
```

### **Check Model Performance**
```bash
make evaluate
# Check: data/models/evaluation/
```

### **Monitor Drift**
```bash
python src/monitoring/drift_detection.py
# Check: monitoring/reports/
```

---

## 🐛 Troubleshooting

### **Issue: "Model not found"**
```bash
# Train the model first
make train
```

### **Issue: "Processed data not found"**
```bash
# Run preprocessing
make preprocess
```

### **Issue: "Module not found"**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### **Issue: "Port already in use"**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process or use different port
uvicorn src.api.main:app --port 8001
```

---

## 🎉 Next Steps

### **For Learning:**
1. ✅ Run complete pipeline: `make all`
2. ✅ Start API: `make api`
3. ✅ Explore MLflow: `make mlflow`
4. ✅ Run tests: `make test`
5. ✅ Try Docker: `make docker`

### **For Production:**
1. ✅ Set up monitoring (Prometheus + Grafana)
2. ✅ Configure Airflow for retraining
3. ✅ Set up GitHub Actions
4. ✅ Deploy to cloud
5. ✅ Add custom business logic

### **For Resume:**
1. ✅ Push to GitHub
2. ✅ Add screenshots/demo video
3. ✅ Write blog post explaining architecture
4. ✅ Showcase in portfolio

---

## 📊 Success Checklist

- [ ] Data downloaded
- [ ] Model trained (check `data/models/best_model.pkl`)
- [ ] Tests passing (`make test`)
- [ ] API running (`http://localhost:8000/docs`)
- [ ] Can make predictions via API
- [ ] MLflow tracking works
- [ ] Docker image builds
- [ ] Monitoring works

---

## 💡 Key Files to Understand

**Start with these:**
1. `config/config.yaml` - All settings
2. `src/models/train.py` - Model training logic
3. `src/api/main.py` - API endpoints
4. `Makefile` - Available commands
5. `README.md` - Main documentation

**Advanced:**
6. `airflow_dags/retraining_pipeline.py` - Automation
7. `.github/workflows/ci-cd.yml` - CI/CD
8. `src/monitoring/drift_detection.py` - Monitoring
9. `docker-compose.yml` - Container orchestration

---

## 🚀 YOU'RE READY!

Everything is built and ready to use. Just run:

```bash
make all  # Complete pipeline
make api  # Start API
```

**🎊 Congratulations! You have a production-ready MLOps system! 🎊**

---

Questions? Issues? Check the README.md or ask for help!
