#!/usr/bin/env python3
"""
Complete training and deployment script for soil fertility ML model
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"{description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main training and deployment pipeline"""
    print("🌱 Soil Fertility ML Model Training & Deployment Pipeline")
    print("=" * 60)
    
    # Check if we're in the backend directory
    if not os.path.exists('requirements.txt'):
        print("Please run this script from the backend directory")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Step 2: Train the ML model
    if not run_command("python ml_model/train_model.py", "Training ML model"):
        print("❌ Failed to train ML model")
        sys.exit(1)
    
    # Step 3: Test the trained model
    if not run_command("python ml_model/test_model.py", "Testing trained ML model"):
        print("❌ Failed to test ML model")
        sys.exit(1)
    
    # Step 4: Start the Flask server
    print("\n🚀 Starting Flask server with trained ML model...")
    print("The server will run on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run("python run.py", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()