import joblib
import numpy as np
import pandas as pd
from ml_predictor import SoilFertilityPredictor

def test_trained_model():
    """
    Test the trained ML model with sample data
    """
    print("Testing trained ML model...")
    
    # Initialize predictor with trained model
    predictor = SoilFertilityPredictor('models/soil_fertility_model.pkl')
    
    # Test cases with different soil conditions
    test_cases = [
        {
            'name': 'High Fertility Soil',
            'data': {
                'nitrogen': 45,
                'phosphorus': 35,
                'potassium': 250,
                'ph': 6.8,
                'organic_matter': 4.5,
                'moisture': 55,
                'temperature': 24
            }
        },
        {
            'name': 'Medium Fertility Soil',
            'data': {
                'nitrogen': 25,
                'phosphorus': 20,
                'potassium': 150,
                'ph': 6.2,
                'organic_matter': 2.8,
                'moisture': 45,
                'temperature': 20
            }
        },
        {
            'name': 'Low Fertility Soil',
            'data': {
                'nitrogen': 10,
                'phosphorus': 8,
                'potassium': 80,
                'ph': 5.2,
                'organic_matter': 1.2,
                'moisture': 30,
                'temperature': 18
            }
        },
        {
            'name': 'Acidic Soil',
            'data': {
                'nitrogen': 30,
                'phosphorus': 25,
                'potassium': 180,
                'ph': 4.8,
                'organic_matter': 3.0,
                'moisture': 50,
                'temperature': 22
            }
        },
        {
            'name': 'Alkaline Soil',
            'data': {
                'nitrogen': 35,
                'phosphorus': 30,
                'potassium': 200,
                'ph': 8.2,
                'organic_matter': 3.5,
                'moisture': 48,
                'temperature': 23
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {test_case['name']}")
        print(f"{'='*50}")
        
        # Print input parameters
        print("Input Parameters:")
        for param, value in test_case['data'].items():
            print(f"  {param}: {value}")
        
        # Make prediction
        try:
            result = predictor.predict_fertility(test_case['data'])
            
            print(f"\nPrediction Results:")
            print(f"  Fertility Level: {result['fertility_level']}")
            print(f"  Score: {result['score']}")
            if 'confidence' in result:
                print(f"  Confidence: {result['confidence']:.3f}")
            
            print(f"\nReasons:")
            for reason in result['reasons']:
                print(f"  • {reason}")
            
            print(f"\nRecommendations:")
            print(f"  Fertilizers: {', '.join(result['recommendations']['fertilizers'])}")
            print(f"  Crops: {', '.join(result['recommendations']['crops'][:5])}")  # Show first 5 crops
            print(f"  Improvements: {', '.join(result['recommendations']['improvements'])}")
            
        except Exception as e:
            print(f"Error making prediction: {e}")

def load_and_inspect_model():
    """
    Load and inspect the trained model
    """
    try:
        print("Loading trained model...")
        model = joblib.load('models/soil_fertility_model.pkl')
        scaler = joblib.load('models/soil_fertility_scaler.pkl')
        feature_names = joblib.load('models/feature_names.pkl')
        
        print(f"Model type: {type(model).__name__}")
        print(f"Model parameters: {model.get_params()}")
        print(f"Feature names: {feature_names}")
        print(f"Number of features: {len(feature_names)}")
        
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\nFeature Importance:")
            for _, row in importance_df.iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
        
        print("\nModel loaded successfully!")
        return True
        
    except FileNotFoundError as e:
        print(f"Model files not found: {e}")
        print("Please run train_model.py first to train the model.")
        return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

if __name__ == "__main__":
    if load_and_inspect_model():
        test_trained_model()