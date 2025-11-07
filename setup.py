#!/usr/bin/env python3
"""
Quick setup script for the ML Churn Prediction project
"""
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a shell command and print status"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - DONE")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED: {e}")
        return False


def main():
    """Run all setup steps"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        ML CHURN PREDICTION - PROJECT SETUP              ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    steps = [
        ("git init", "Initialize git repository"),
        ("python -m pip install --upgrade pip", "Upgrade pip"),
        # Note: Don't install requirements here as it takes long
        # User should do: pip install -r requirements.txt
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            print(f"\n⚠️  Setup incomplete. Please fix errors and try again.")
            sys.exit(1)
    
    print(f"""
    
    ╔══════════════════════════════════════════════════════════╗
    ║                  SETUP COMPLETE! 🎉                      ║
    ╚══════════════════════════════════════════════════════════╝
    
    📋 Next Steps:
    
    1️⃣  Install dependencies:
       pip install -r requirements.txt
    
    2️⃣  Download the dataset:
       python src/utils/download_data.py
    
    3️⃣  Create your .env file:
       cp .env.example .env
       # Then edit .env with your settings
    
    4️⃣  Start exploring in Jupyter:
       jupyter notebook notebooks/
    
    5️⃣  Train your first model:
       python src/models/train.py
    
    📚 Documentation: See README.md for detailed instructions
    
    🚀 Happy coding!
    """)


if __name__ == "__main__":
    main()
