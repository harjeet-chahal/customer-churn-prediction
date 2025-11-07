# 🚀 Getting Started with ML Churn Prediction Project

## ✅ What We've Built So Far

Your MLOps project structure is ready! Here's what's been created:

### 📁 Project Structure
```
ml-churn-prediction/
├── 📄 README.md                    # Complete project documentation
├── 📄 requirements.txt             # All Python dependencies
├── 📄 setup.py                     # Quick setup script
├── 📄 .gitignore                   # Git ignore rules
├── 📄 .env.example                 # Environment variables template
│
├── config/
│   └── config.yaml                 # Central configuration file
│
├── data/
│   ├── raw/                        # Original datasets
│   ├── processed/                  # Cleaned data
│   └── models/                     # Saved models
│
├── notebooks/                      # Jupyter notebooks (to create)
│
├── src/
│   ├── features/                   # Feature engineering (to build)
│   ├── models/                     # Model training (to build)
│   ├── api/                        # FastAPI service (to build)
│   ├── monitoring/                 # Drift detection (to build)
│   └── utils/
│       ├── config_loader.py        # ✅ Config loading utility
│       ├── logger.py               # ✅ Logging setup
│       └── download_data.py        # ✅ Dataset downloader
│
├── tests/                          # Unit tests (to write)
├── airflow_dags/                   # Workflow orchestration (to build)
├── terraform/                      # Infrastructure code (to build)
└── .github/workflows/              # CI/CD pipelines (to build)
```

---

## 🎯 Next Steps - Let's Build Phase 1!

### **STEP 1: Set Up Your Local Environment** (On Your Mac)

Open Terminal and navigate to your project:

```bash
cd ~/path/to/ml-churn-prediction  # Your actual project location

# Activate your virtual environment (you already have this)
source venv/bin/activate

# Install all dependencies (this will take 5-10 minutes)
pip install -r requirements.txt
```

---

### **STEP 2: Download the Dataset**

```bash
# Run the download script
python src/utils/download_data.py
```

This will download the Telco Customer Churn dataset (7,043 customers) and save it to `data/raw/telco_churn.csv`.

**Expected output:**
```
✅ Dataset downloaded successfully!
📊 Shape: (7043, 21)
💾 Saved to: data/raw/telco_churn.csv
```

---

### **STEP 3: Create Your First Jupyter Notebook**

Let's do some exploratory data analysis (EDA)!

```bash
# Start Jupyter
jupyter notebook
```

In Jupyter, create a new notebook in the `notebooks/` folder called `01_exploration.ipynb`.

**Here's starter code for your notebook:**

```python
# Cell 1: Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Cell 2: Load data
data_path = Path("../data/raw/telco_churn.csv")
df = pd.read_csv(data_path)

print(f"Dataset shape: {df.shape}")
df.head()

# Cell 3: Basic info
print("Dataset Info:")
print(df.info())
print("\nMissing values:")
print(df.isnull().sum())

# Cell 4: Target distribution
print("\nChurn distribution:")
print(df['Churn'].value_counts())
print(f"\nChurn rate: {df['Churn'].value_counts(normalize=True)['Yes']:.2%}")

# Cell 5: Visualize churn
plt.figure(figsize=(8, 5))
df['Churn'].value_counts().plot(kind='bar')
plt.title('Churn Distribution')
plt.xlabel('Churn')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

# Cell 6: Numeric features
numeric_cols = df.select_dtypes(include=[np.number]).columns
print(f"Numeric columns: {list(numeric_cols)}")

df[numeric_cols].describe()

# Cell 7: Correlations
plt.figure(figsize=(10, 8))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlations')
plt.show()
```

---

### **STEP 4: What You'll Learn from EDA**

After running the notebook, you should discover:

1. **Dataset has 7,043 customers with 21 features**
2. **Target variable:** "Churn" (Yes/No)
3. **Churn rate:** ~26% (imbalanced dataset)
4. **Features include:**
   - Demographics: gender, SeniorCitizen, Partner, Dependents
   - Services: PhoneService, InternetService, OnlineSecurity, etc.
   - Account: tenure, Contract, PaymentMethod, MonthlyCharges
5. **Missing values:** Possibly in TotalCharges (needs cleaning)
6. **Data types:** Mix of categorical and numeric

---

## 🎯 After EDA - What's Next?

Once you've explored the data, we'll build:

### **Phase 1: Model Development** (Next session)
1. **Data preprocessing** - Clean & transform data
2. **Feature engineering** - Create new features
3. **Model training** - Train multiple algorithms
4. **Experiment tracking** - Use MLflow to track everything
5. **Model evaluation** - Compare models and pick the best

### **Phase 2: API Development**
Build FastAPI service to serve predictions

### **Phase 3-6: Production MLOps**
CI/CD, deployment, monitoring, retraining

---

## 🛠️ Useful Commands

```bash
# Activate environment
source venv/bin/activate

# Run Jupyter
jupyter notebook

# Test config loading
python -c "from src.utils.config_loader import load_config; print(load_config())"

# Test logger
python src/utils/logger.py

# Check installed packages
pip list

# Run setup script
python setup.py
```

---

## 📚 Key Files to Review

1. **README.md** - Complete project overview
2. **config/config.yaml** - All settings (you can modify these)
3. **requirements.txt** - All dependencies
4. **.env.example** - Create `.env` from this for secrets

---

## ⚡ Pro Tips

1. **Always activate your venv** before working
2. **Git commit frequently** as you build
3. **Read the config.yaml** - it controls everything
4. **Check logs/** folder for debugging
5. **Start simple** - get basic model working first

---

## 🚨 Common Issues & Solutions

**Issue:** `ModuleNotFoundError`
- **Solution:** Make sure venv is activated and requirements installed

**Issue:** Can't find dataset
- **Solution:** Run `python src/utils/download_data.py`

**Issue:** Import errors from src/
- **Solution:** Make sure you're running from project root

---

## 🎓 Learning Path

1. ✅ **Today:** Project setup + EDA
2. **Next:** Data preprocessing & feature engineering
3. **Then:** Model training with MLflow
4. **Later:** API development
5. **Finally:** Full production deployment

---

## 📞 When You're Ready for Phase 1

Tell me when you've:
1. ✅ Installed requirements
2. ✅ Downloaded dataset
3. ✅ Completed EDA notebook
4. ✅ Understood the data

Then we'll build the **data preprocessing pipeline** and **train our first model**!

---

## 🎯 Your Goal for Today

**Complete the EDA and understand:**
- What the data looks like
- What features we have
- What preprocessing is needed
- Which features might be important for prediction

Take your time exploring - good EDA is the foundation of great ML!

---

**Questions?** Just ask! I'm here to help you build this step by step.

**Remember:** This is a marathon, not a sprint. We're building production-quality ML infrastructure! 🚀
