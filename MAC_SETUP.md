# 🍎 Mac Setup Instructions

## 📥 Step 1: Download Your Project

The complete project structure is ready in the `ml-churn-prediction` folder.

**On your Mac:**

```bash
# Navigate to where you want the project
cd ~/Documents  # or wherever you prefer

# The project folder is already in your Downloads or wherever you saved it
# If you need to copy it from Downloads:
# cp -r ~/Downloads/ml-churn-prediction ~/Documents/
```

---

## 🔧 Step 2: Set Up Virtual Environment

```bash
# Navigate into your project
cd ml-churn-prediction

# Your venv should already exist, but verify:
ls -la venv/

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
# Example: (venv) (base) harjeetschahal@Harjeets-MacBook-Pro ml-churn-prediction %
```

---

## 📦 Step 3: Install Dependencies

**This will take 5-10 minutes** - it's installing 50+ packages!

```bash
# Make sure venv is activated (you should see (venv) in prompt)
source venv/bin/activate

# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# You'll see a lot of downloading and installation messages
# Wait for it to complete...

# Verify installation
pip list | head -20
```

**What you're installing:**
- pandas, numpy, scikit-learn (ML basics)
- XGBoost (gradient boosting)
- MLflow (experiment tracking)
- FastAPI (API framework)
- Jupyter (notebooks)
- And 40+ more packages!

---

## 📊 Step 4: Download the Dataset

```bash
# Still in your project directory with venv activated
python src/utils/download_data.py
```

**Expected output:**
```
INFO - Downloading Telco Customer Churn dataset...
✅ Dataset downloaded successfully!
📊 Shape: (7043, 21)
💾 Saved to: data/raw/telco_churn.csv
```

**If you see this, you're good!** The dataset is now in `data/raw/telco_churn.csv`

---

## 🔐 Step 5: Set Up Environment Variables

```bash
# Create your .env file from the template
cp .env.example .env

# Open it in your text editor
open -a TextEdit .env

# You don't need to fill everything now
# Just having the file is enough for now
```

---

## 📓 Step 6: Start Jupyter Notebook

```bash
# From your project root, start Jupyter
jupyter notebook

# This will open in your browser automatically
# If not, look for a URL like: http://localhost:8888/
```

**In Jupyter:**
1. Navigate to the `notebooks/` folder
2. Click "New" → "Python 3"
3. Name it `01_exploration.ipynb`
4. Start coding!

---

## ✅ Verification Checklist

Run these commands to verify everything works:

```bash
# 1. Check Python version (should be 3.12.7)
python --version

# 2. Check venv is activated
echo $VIRTUAL_ENV
# Should show: /path/to/ml-churn-prediction/venv

# 3. Test imports
python -c "import pandas; import sklearn; import mlflow; print('✅ All imports work!')"

# 4. Check dataset exists
ls -lh data/raw/telco_churn.csv
# Should show: ~1MB file

# 5. Test config loading
python -c "from src.utils.config_loader import load_config; config = load_config(); print('✅ Config loaded!')"

# 6. Test logger
python src/utils/logger.py
```

**If all of these work, you're 100% ready to start!** 🎉

---

## 🚨 Common Mac Issues & Solutions

### Issue 1: "command not found: python"
**Solution:** Use `python3` instead of `python`
```bash
python3 --version
python3 -m venv venv
```

### Issue 2: "Permission denied"
**Solution:** Use your user directory, not system directories
```bash
# Don't do: sudo pip install
# Instead, make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Issue 3: "pip is not recognized"
**Solution:** Ensure venv is activated and use python -m pip
```bash
source venv/bin/activate
python -m pip install --upgrade pip
```

### Issue 4: "No module named 'pandas'"
**Solution:** Venv not activated or requirements not installed
```bash
# Check if venv is activated (should see (venv) in prompt)
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 5: Jupyter kernel issues
**Solution:** Install ipykernel in your venv
```bash
source venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=venv
```

### Issue 6: "Cannot import name 'config_loader'"
**Solution:** Run Python from project root, not subdirectories
```bash
# Always run from here:
cd ~/path/to/ml-churn-prediction

# Not from here:
# cd ~/path/to/ml-churn-prediction/src
```

---

## 📁 Where Everything Is

```
Your Mac:
├── Documents/                    # Or wherever you chose
    └── ml-churn-prediction/      # Your project
        ├── venv/                 # Virtual environment (don't touch)
        ├── data/
        │   └── raw/
        │       └── telco_churn.csv  # Dataset
        ├── notebooks/            # Create Jupyter notebooks here
        ├── src/                  # Python code
        ├── requirements.txt      # Dependencies
        └── config/
            └── config.yaml       # Settings
```

---

## 🎯 Your Workflow (Daily)

**Every time you work on the project:**

```bash
# 1. Open Terminal
# Press Cmd+Space, type "Terminal", press Enter

# 2. Navigate to project
cd ~/Documents/ml-churn-prediction  # Your actual path

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start working!
jupyter notebook
# OR
python src/your_script.py
# OR
git status  # Check what changed
```

**When you're done:**

```bash
# Deactivate venv (optional)
deactivate

# Or just close Terminal
```

---

## 🔄 Git Setup (Recommended)

```bash
# Initialize git (if not done)
git init

# Check status
git status

# Add all files
git add .

# First commit
git commit -m "Initial project setup"

# Create GitHub repo (on github.com)
# Then connect:
git remote add origin https://github.com/yourusername/ml-churn-prediction.git
git branch -M main
git push -u origin main
```

---

## 🎨 Recommended Mac Tools

### Terminal Apps
- **iTerm2** - Better than default Terminal (optional)
- **Oh My Zsh** - Prettier terminal (optional)

### Code Editors
- **VS Code** - Best for Python development
- **PyCharm** - Python-specific IDE
- **Sublime Text** - Lightweight option

### VS Code Extensions (if using VS Code)
- Python
- Jupyter
- Docker
- GitLens
- YAML

---

## 📚 Mac Terminal Tips

```bash
# Clear screen
clear
# Or: Cmd+K

# Previous command
↑ arrow key

# Search command history
Ctrl+R

# Cancel current command
Ctrl+C

# Tab completion
Type "python sr" then press Tab → "python src/"

# Open file in default app
open data/raw/telco_churn.csv

# Open current directory in Finder
open .

# Copy output to clipboard
python script.py | pbcopy
```

---

## ✅ You're Ready When...

- [ ] Terminal opens successfully
- [ ] Can navigate to project directory
- [ ] Virtual environment activates (see `(venv)` in prompt)
- [ ] `python --version` shows Python 3.12.7
- [ ] All imports work (pandas, sklearn, mlflow)
- [ ] Dataset exists in `data/raw/`
- [ ] Jupyter notebook starts
- [ ] Can create and run cells in Jupyter

**Once all checked, you're ready to start building!** 🚀

---

## 🆘 Need Help?

If you get stuck:
1. Check the error message carefully
2. Google the exact error
3. Check Stack Overflow
4. Ask me - I'm here to help!

**Common error patterns:**
- "ModuleNotFoundError" → venv not activated or requirements not installed
- "Permission denied" → Don't use sudo, use venv
- "No such file" → Wrong directory, navigate to project root
- Import errors → Running from wrong location

---

## 🎓 Learning Resources for Mac/Terminal

- **Terminal basics:** Open Terminal and type `man intro`
- **Python on Mac:** https://docs.python.org/3/using/mac.html
- **Jupyter tips:** Press `H` in Jupyter for keyboard shortcuts

---

## 🚀 Next Steps

After setup is complete:

1. ✅ Verify everything works (checklist above)
2. 📖 Read `GETTING_STARTED.md`
3. 📊 Start Jupyter and begin EDA
4. 💬 Come back when ready for Phase 1

---

**You've got everything you need! Let's build something awesome! 🎉**
