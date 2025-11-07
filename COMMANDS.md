# 📋 Quick Command Reference

## 🚀 Initial Setup

```bash
# 1. Navigate to project
cd ~/path/to/ml-churn-prediction

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies (first time only)
pip install -r requirements.txt

# 4. Download dataset
python src/utils/download_data.py

# 5. Create .env file
cp .env.example .env
# Then edit .env with your settings
```

---

## 💻 Development Commands

### Jupyter Notebook
```bash
# Start Jupyter
jupyter notebook

# Or Jupyter Lab
jupyter lab
```

### Python Scripts
```bash
# Run from project root
python src/utils/download_data.py
python src/models/train.py
python -m pytest tests/
```

### Configuration
```bash
# Test config loading
python -c "from src.utils.config_loader import load_config; print(load_config())"

# Test logger
python src/utils/logger.py
```

---

## 📦 Package Management

```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Upgrade pip
python -m pip install --upgrade pip
```

---

## 🔧 Git Commands

```bash
# Initialize repo (if not done)
git init

# Check status
git status

# Add files
git add .

# Commit
git commit -m "Your message"

# Create .gitignore
# Already created for you!

# View history
git log --oneline
```

---

## 🧪 Testing (Later)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_features.py

# Verbose output
pytest -v
```

---

## 🐳 Docker (Phase 2+)

```bash
# Build image
docker build -t ml-churn-api .

# Run container
docker run -p 8000:8000 ml-churn-api

# Run with docker-compose
docker-compose up

# Stop containers
docker-compose down
```

---

## 🚀 MLflow (Phase 1)

```bash
# Start MLflow UI
mlflow ui

# Access at: http://localhost:5000

# Start with specific port
mlflow ui --port 5001

# Start tracking server
mlflow server --host 0.0.0.0 --port 5000
```

---

## 🔍 API Commands (Phase 2)

```bash
# Start FastAPI server
uvicorn src.api.main:app --reload

# Access at: http://localhost:8000
# Docs at: http://localhost:8000/docs

# With custom port
uvicorn src.api.main:app --port 8001 --reload

# Test endpoint
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"tenure": 12, "monthly_charges": 50.0}'
```

---

## 📊 Data Commands

```bash
# View first few lines of CSV
head -n 5 data/raw/telco_churn.csv

# Count lines
wc -l data/raw/telco_churn.csv

# Check file size
ls -lh data/raw/telco_churn.csv
```

---

## 🛠️ Troubleshooting

```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Check if package is installed
pip show pandas

# Find Python location
which python

# Check environment variables
echo $VIRTUAL_ENV
```

---

## 📈 Monitoring (Phase 5)

```bash
# Start Prometheus
prometheus --config.file=prometheus.yml

# Start Grafana
grafana-server

# View logs
tail -f logs/app.log
```

---

## 🔄 Airflow (Phase 4)

```bash
# Initialize Airflow DB
airflow db init

# Create user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Start webserver
airflow webserver --port 8080

# Start scheduler
airflow scheduler

# List DAGs
airflow dags list

# Trigger DAG
airflow dags trigger churn_retraining
```

---

## ⚡ Quick Checks

```bash
# Is venv activated?
echo $VIRTUAL_ENV

# Check current directory
pwd

# Check Python path
python -c "import sys; print(sys.executable)"

# Import test
python -c "import pandas; print('✅ pandas works')"

# Check GPU (if needed)
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 🎯 Most Common Workflow

```bash
# Every time you start working:

# 1. Navigate to project
cd ~/path/to/ml-churn-prediction

# 2. Activate environment
source venv/bin/activate

# 3. Pull latest changes (if team project)
git pull

# 4. Start Jupyter or run scripts
jupyter notebook
# OR
python src/models/train.py

# 5. Commit your work
git add .
git commit -m "Added feature X"
git push
```

---

## 💡 Pro Tips

- **Always activate venv first!**
- **Run Python from project root** (where README.md is)
- **Use relative paths** in code (e.g., `data/raw/...`)
- **Check logs/** for debugging
- **Commit often, push regularly**

---

## 🆘 Emergency Fixes

```bash
# Package conflicts
pip install --force-reinstall package-name

# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Clear Jupyter kernel
jupyter kernelspec list
jupyter kernelspec uninstall kernel-name

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

---

**Keep this file handy for quick reference!** 📌
