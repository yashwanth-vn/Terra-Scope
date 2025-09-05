import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

def generate_synthetic_soil_data(n_samples=5000):
    """
    Generate synthetic soil fertility data for training
    In production, replace this with your actual soil dataset
    """
    np.random.seed(42)
    
    data = []
    
    for _ in range(n_samples):
        # Generate correlated soil parameters
        nitrogen = np.random.normal(30, 15)  # ppm
        phosphorus = np.random.normal(25, 10)  # ppm
        potassium = np.random.normal(200, 80)  # ppm
        ph = np.random.normal(6.5, 1.2)  # pH scale
        organic_matter = np.random.normal(3.5, 1.5)  # percentage
        moisture = np.random.normal(50, 20)  # percentage
        temperature = np.random.normal(22, 8)  # Celsius
        
        # Ensure realistic ranges
        nitrogen = max(0, min(100, nitrogen))
        phosphorus = max(0, min(100, phosphorus))
        potassium = max(0, min(500, potassium))
        ph = max(3, min(9, ph))
        organic_matter = max(0, min(10, organic_matter))
        moisture = max(0, min(100, moisture))
        temperature = max(-5, min(45, temperature))
        
        # Calculate fertility based on soil science principles
        fertility_score = 0
        
        # Nitrogen contribution (0-25 points)
        if nitrogen < 15:
            fertility_score += nitrogen * 0.8
        elif nitrogen < 40:
            fertility_score += 12 + (nitrogen - 15) * 0.5
        else:
            fertility_score += 25
            
        # Phosphorus contribution (0-20 points)
        if phosphorus < 10:
            fertility_score += phosphorus * 1.0
        elif phosphorus < 30:
            fertility_score += 10 + (phosphorus - 10) * 0.5
        else:
            fertility_score += 20
            
        # Potassium contribution (0-20 points)
        if potassium < 100:
            fertility_score += potassium * 0.1
        elif potassium < 250:
            fertility_score += 10 + (potassium - 100) * 0.067
        else:
            fertility_score += 20
            
        # pH contribution (0-15 points)
        if 6.0 <= ph <= 7.5:
            fertility_score += 15
        elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:
            fertility_score += 10
        else:
            fertility_score += 5
            
        # Organic matter contribution (0-15 points)
        if organic_matter < 2:
            fertility_score += organic_matter * 3
        elif organic_matter < 5:
            fertility_score += 6 + (organic_matter - 2) * 3
        else:
            fertility_score += 15
            
        # Moisture contribution (0-5 points)
        if 30 <= moisture <= 70:
            fertility_score += 5
        elif 20 <= moisture < 30 or 70 < moisture <= 80:
            fertility_score += 3
        else:
            fertility_score += 1
            
        # Add some randomness
        fertility_score += np.random.normal(0, 3)
        fertility_score = max(0, min(100, fertility_score))
        
        # Classify fertility level
        if fertility_score >= 75:
            fertility_level = 'High'
        elif fertility_score >= 50:
            fertility_level = 'Medium'
        else:
            fertility_level = 'Low'
        
        data.append({
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'ph': ph,
            'organic_matter': organic_matter,
            'moisture': moisture,
            'temperature': temperature,
            'fertility_score': fertility_score,
            'fertility_level': fertility_level
        })
    
    return pd.DataFrame(data)

def train_soil_fertility_model():
    """
    Train machine learning model for soil fertility prediction
    """
    print("Generating synthetic soil fertility dataset...")
    df = generate_synthetic_soil_data(5000)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Fertility distribution:\n{df['fertility_level'].value_counts()}")
    
    # Features and target
    feature_columns = ['nitrogen', 'phosphorus', 'potassium', 'ph', 
                      'organic_matter', 'moisture', 'temperature']
    X = df[feature_columns]
    y = df['fertility_level']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    rf_model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Cross-validation
    cv_scores = cross_val_score(rf_model, X_train_scaled, y_train, cv=5)
    print(f"\nCross-validation scores: {cv_scores}")
    print(f"Average CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Save the model and scaler
    print("\nSaving model and scaler...")
    joblib.dump(rf_model, 'models/soil_fertility_model.pkl')
    joblib.dump(scaler, 'models/soil_fertility_scaler.pkl')
    
    # Save feature names for reference
    joblib.dump(feature_columns, 'models/feature_names.pkl')
    
    print("Model training completed successfully!")
    print("Files saved:")
    print("- models/soil_fertility_model.pkl")
    print("- models/soil_fertility_scaler.pkl")
    print("- models/feature_names.pkl")
    
    return rf_model, scaler, feature_columns

if __name__ == "__main__":
    model, scaler, features = train_soil_fertility_model()