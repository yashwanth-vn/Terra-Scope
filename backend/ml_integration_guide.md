# Machine Learning Model Integration Guide

This guide explains how to integrate your trained machine learning model with the Flask backend.

## 1. Model Training Requirements

Your ML model should be trained to predict soil fertility based on these 7 features:

```python
features = [
    'nitrogen',      # ppm (0-100)
    'phosphorus',    # ppm (0-100) 
    'potassium',     # ppm (0-500)
    'ph',           # 0-14
    'organic_matter', # percentage (0-10)
    'moisture',      # percentage (0-100)
    'temperature'    # Celsius (-10 to 50)
]
```

## 2. Model Output Format

Your model should output one of these formats:

### Option A: Classification Model
```python
# Output: categorical prediction
prediction = model.predict(features)  # Returns: 'High', 'Medium', or 'Low'
probabilities = model.predict_proba(features)  # Returns: [0.1, 0.2, 0.7]
```

### Option B: Regression Model
```python
# Output: numerical score (0-1 or 0-100)
prediction = model.predict(features)  # Returns: 0.85 (85% fertility)
```

## 3. Save Your Trained Model

```python
import joblib
from sklearn.preprocessing import StandardScaler

# Save your trained model
joblib.dump(your_trained_model, 'models/soil_fertility_model.pkl')

# Save scaler if you used feature scaling
joblib.dump(your_scaler, 'models/soil_fertility_scaler.pkl')
```

## 4. Integration Steps

### Step 1: Place Model Files
```
backend/
├── models/
│   ├── soil_fertility_model.pkl
│   └── soil_fertility_scaler.pkl (optional)
├── ml_predictor.py
└── ...
```

### Step 2: Update ml_predictor.py

```python
# In ml_predictor.py, update the __init__ method:
def __init__(self, model_path='models/soil_fertility_model.pkl'):
    self.model = None
    self.scaler = None
    
    if os.path.exists(model_path):
        self.load_model(model_path)
```

### Step 3: Customize Prediction Logic

Update the `_ml_prediction` method in `ml_predictor.py` based on your model type:

```python
def _ml_prediction(self, soil_data):
    features = self.preprocess_features(soil_data)
    
    # For classification models:
    prediction = self.model.predict(features)[0]
    probabilities = self.model.predict_proba(features)[0]
    
    # For regression models:
    # score = self.model.predict(features)[0]
    # prediction = 'High' if score > 0.8 else 'Medium' if score > 0.6 else 'Low'
    
    # Continue with your logic...
```

## 5. Model Training Example

Here's a sample structure for training your model:

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

# Load your dataset
df = pd.read_csv('soil_data.csv')

# Features and target
features = ['nitrogen', 'phosphorus', 'potassium', 'ph', 
           'organic_matter', 'moisture', 'temperature']
X = df[features]
y = df['fertility_level']  # 'High', 'Medium', 'Low'

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features (optional but recommended)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model
predictions = model.predict(X_test_scaled)
print(classification_report(y_test, predictions))

# Save model and scaler
joblib.dump(model, 'models/soil_fertility_model.pkl')
joblib.dump(scaler, 'models/soil_fertility_scaler.pkl')
```

## 6. Advanced Features

### Feature Importance Analysis
```python
def get_feature_importance(self):
    if hasattr(self.model, 'feature_importances_'):
        importance = dict(zip(self.feature_names, self.model.feature_importances_))
        return sorted(importance.items(), key=lambda x: x[1], reverse=True)
    return None
```

### Prediction Confidence
```python
def get_prediction_confidence(self, features):
    if hasattr(self.model, 'predict_proba'):
        probabilities = self.model.predict_proba(features)[0]
        return max(probabilities)
    return None
```

## 7. Testing Your Integration

```python
# Test script
from ml_predictor import SoilFertilityPredictor

predictor = SoilFertilityPredictor('models/soil_fertility_model.pkl')

test_data = {
    'nitrogen': 25,
    'phosphorus': 20,
    'potassium': 150,
    'ph': 6.5,
    'organic_matter': 3,
    'moisture': 45,
    'temperature': 22
}

result = predictor.predict_fertility(test_data)
print(result)
```

## 8. Production Considerations

- **Model Versioning**: Keep track of model versions
- **Model Monitoring**: Log predictions for model drift detection
- **Error Handling**: Graceful fallback when model fails
- **Performance**: Cache model in memory for faster predictions
- **Security**: Validate all input data before prediction

Replace the rule-based logic with your actual ML model following this guide!