import numpy as np
import joblib
import os
import json
import json
from typing import Dict, Any

class SoilFertilityPredictor:
    """
    Machine Learning predictor for soil fertility analysis
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.feature_names = None
        self.feature_names = [
            'nitrogen', 'phosphorus', 'potassium', 'ph', 
            'organic_matter', 'moisture', 'temperature'
        ]
        
        # Try to load trained model
        model_path = model_path or 'models/soil_fertility_model.pkl'
        if os.path.exists(model_path):
        model_path = model_path or 'models/soil_fertility_model.pkl'
        if os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print("No trained model found. Using rule-based predictions.")
        else:
            print("No trained model found. Using rule-based predictions.")
    
    def load_model(self, model_path: str):
        """
        Load trained ML model and scaler
        """
        try:
            # Load your trained model
            self.model = joblib.load(model_path)
            
            # Load scaler if available
            scaler_path = model_path.replace('.pkl', '_scaler.pkl')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
            
            # Load feature names if available
            feature_path = os.path.join(os.path.dirname(model_path), 'feature_names.pkl')
            if os.path.exists(feature_path):
                self.feature_names = joblib.load(feature_path)
            
            # Load feature names if available
            feature_path = os.path.join(os.path.dirname(model_path), 'feature_names.pkl')
            if os.path.exists(feature_path):
                self.feature_names = joblib.load(feature_path)
                
            print(f"Model loaded successfully from {model_path}")
            print(f"Model type: {type(self.model).__name__}")
            if hasattr(self.model, 'n_estimators'):
                print(f"Number of estimators: {self.model.n_estimators}")
            print(f"Model type: {type(self.model).__name__}")
            if hasattr(self.model, 'n_estimators'):
                print(f"Number of estimators: {self.model.n_estimators}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def preprocess_features(self, soil_data: Dict[str, float]) -> np.ndarray:
        """
        Preprocess soil data for ML model input
        """
        # Extract features in the correct order
        features = np.array([[
            soil_data['nitrogen'],
            soil_data['phosphorus'],
            soil_data['potassium'],
            soil_data['ph'],
            soil_data['organic_matter'],
            soil_data['moisture'],
            soil_data['temperature']
        ]])
        
        # Apply scaling if scaler is available
        if self.scaler:
            features = self.scaler.transform(features)
        
        return features
    
    def predict_fertility(self, soil_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict soil fertility using ML model or fallback to rule-based logic
        """
        if self.model:
            return self._ml_prediction(soil_data)
        else:
            return self._rule_based_prediction(soil_data)
    
    def _ml_prediction(self, soil_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make prediction using trained ML model
        """
        try:
            # Preprocess features
            features = self.preprocess_features(soil_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Get prediction probabilities if available
            confidence = 0.85  # Default confidence
            confidence = 0.85  # Default confidence
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features)[0]
                confidence = max(probabilities)
                
                # Get class probabilities for detailed analysis
                classes = self.model.classes_
                prob_dict = dict(zip(classes, probabilities))
                classes = self.model.classes_
                prob_dict = dict(zip(classes, probabilities))
            
            # The prediction is already a fertility level from our trained model
            fertility_level = str(prediction)
            
            # The prediction is already a fertility level from our trained model
            fertility_level = str(prediction)
            
            # Calculate score based on confidence and fertility level
            if isinstance(prediction, (int, float)):
                # If model returns numeric score
                # If model returns numeric score
                if prediction > 0.8:
                    fertility_level = 'High'
                    score = int(prediction * 100)
                elif prediction > 0.6:
                    fertility_level = 'Medium'
                    score = int(prediction * 100)
                else:
                    fertility_level = 'Low'
                    score = int(prediction * 100)
            else:
                # If prediction is categorical (our case)
                fertility_level = str(prediction)
                if fertility_level == 'High':
                    score = int(75 + confidence * 25)  # 75-100
                elif fertility_level == 'Medium':
                    score = int(50 + confidence * 25)  # 50-75
                else:
                    score = int(confidence * 50)       # 0-50
                    score = int(75 + confidence * 25)  # 75-100
                elif fertility_level == 'Medium':
                    score = int(50 + confidence * 25)  # 50-75
                else:
                    score = int(confidence * 50)       # 0-50
            
            # Generate explanations based on ML prediction
            reasons = self._generate_ml_explanations(soil_data, fertility_level, confidence)
            recommendations = self._generate_recommendations(soil_data, fertility_level)
            
            return {
                'fertility_level': fertility_level,
                'score': score,
                'confidence': confidence,
                'reasons': reasons,
                'recommendations': recommendations
            }
            
        except Exception as e:
            print(f"ML prediction error: {e}")
            # Fallback to rule-based prediction
            return self._rule_based_prediction(soil_data)
    
    def _generate_ml_explanations(self, soil_data: Dict[str, Any], fertility_level: str, confidence: float = 0.85) -> list:
        """
        Generate explanations based on ML model insights and feature importance
        """
        reasons = []
        
        # Add confidence-based explanation
        if confidence > 0.9:
            reasons.append(f'ML model predicts {fertility_level.lower()} fertility with very high confidence ({confidence:.1%})')
        elif confidence > 0.8:
            reasons.append(f'ML model predicts {fertility_level.lower()} fertility with high confidence ({confidence:.1%})')
        else:
            reasons.append(f'ML model predicts {fertility_level.lower()} fertility with moderate confidence ({confidence:.1%})')
        
        # Feature importance analysis (if available)
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
            
            reasons.append(f'Key factors: {", ".join([f.replace("_", " ") for f, _ in top_features])}')
        
        # Analyze each parameter and provide insights based on soil science
        if soil_data['nitrogen'] < 20:
            reasons.append('Nitrogen deficiency detected - critical for plant growth and leaf development')
        elif soil_data['nitrogen'] > 50:
            reasons.append('Excellent nitrogen levels support vigorous plant growth')
        else:
        # Add confidence-based explanation
        if confidence > 0.9:
            reasons.append(f'ML model predicts {fertility_level.lower()} fertility with very high confidence ({confidence:.1%})')
        elif confidence > 0.8:
            reasons.append(f'ML model predicts {fertility_level.lower()} fertility with high confidence ({confidence:.1%})')
        else:
            reasons.append(f'ML model predicts {fertility_level.lower()} fertility with moderate confidence ({confidence:.1%})')
        
        # Feature importance analysis (if available)
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
            top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
            
            reasons.append(f'Key factors: {", ".join([f.replace("_", " ") for f, _ in top_features])}')
        
        # Analyze each parameter and provide insights based on soil science
        
            reasons.append('Nitrogen deficiency detected - critical for plant growth and leaf development')
            reasons.append('Low phosphorus may limit root development and flowering')
            reasons.append('Excellent nitrogen levels support vigorous plant growth')
        else:
            reasons.append('Nitrogen levels are adequate for most crops')
            reasons.append('Optimal phosphorus levels promote strong root systems')
        else:
            reasons.append('Low phosphorus may limit root development and flowering')
        
            reasons.append('Optimal phosphorus levels promote strong root systems')
        else:
            reasons.append('Phosphorus levels support normal plant development')
            reasons.append('Potassium deficiency may reduce disease resistance and stress tolerance')
        elif soil_data['potassium'] > 200:
            reasons.append('Potassium deficiency may reduce disease resistance and stress tolerance')
        else:
            reasons.append('Excellent potassium levels enhance plant resilience')
        else:
            reasons.append('Potassium levels are sufficient for plant health')
        
        if soil_data['ph'] < 6.0 or soil_data['ph'] > 8.0:
            reasons.append('pH levels outside optimal range may limit nutrient uptake')
        else:
            reasons.append('pH levels are ideal for maximum nutrient availability')
        
        if soil_data['organic_matter'] < 2:
            reasons.append('Low organic matter limits soil structure and water retention')
        elif soil_data['organic_matter'] > 4:
            reasons.append('Rich organic matter content enhances soil biology')
        else:
            reasons.append('Organic matter levels support healthy soil ecosystem')
        
        # Environmental factors
        if soil_data['moisture'] < 30 or soil_data['moisture'] > 80:
            reasons.append('pH levels outside optimal range may limit nutrient uptake')
        else:
            reasons.append('pH levels are ideal for maximum nutrient availability')
        
        if soil_data['temperature'] < 15 or soil_data['temperature'] > 30:
            reasons.append('Low organic matter limits soil structure and water retention')
        else:
            reasons.append('Rich organic matter content enhances soil biology')
        else:
            reasons.append('Organic matter levels support healthy soil ecosystem')
        
        # Environmental factors
        if soil_data['moisture'] < 30 or soil_data['moisture'] > 80:
            reasons.append('Moisture levels may stress plants - optimal range is 30-70%')
        else:
            reasons.append('Soil moisture is within ideal range for plant growth')
        
        if soil_data['temperature'] < 15 or soil_data['temperature'] > 30:
            reasons.append('Soil temperature outside optimal range may slow nutrient uptake')
        else:
            reasons.append('Soil temperature supports active root growth and nutrient absorption')
        
        return reasons
    
    def _generate_recommendations(self, soil_data: Dict[str, Any], fertility_level: str) -> Dict[str, list]:
        """
        Generate fertilizer and crop recommendations
        """
        fertilizers = []
        crops = []
        improvements = []
        
        # Fertilizer recommendations based on deficiencies
        if soil_data['nitrogen'] < 20:
            fertilizers.extend(['Urea (46-0-0)', 'Ammonium Sulfate (21-0-0)'])
            improvements.append('Apply nitrogen-rich fertilizers during growing season')
        
        if soil_data['phosphorus'] < 15:
            fertilizers.extend(['Triple Superphosphate (0-46-0)', 'Bone Meal (4-12-0)'])
            improvements.append('Increase phosphorus for better root development')
        
        if soil_data['potassium'] < 100:
            fertilizers.extend(['Muriate of Potash (0-0-60)', 'Potassium Sulfate (0-0-50)'])
            improvements.append('Apply potassium fertilizers for stress tolerance')
        
        if soil_data['ph'] < 6.0:
            fertilizers.append('Dolomitic Lime')
            improvements.append('Apply lime to increase pH')
        elif soil_data['ph'] > 8.0:
            fertilizers.append('Elemental Sulfur')
            improvements.append('Apply sulfur to decrease pH')
        
        if soil_data['organic_matter'] < 2:
            fertilizers.extend(['Compost', 'Well-aged Manure'])
            improvements.append('Add organic matter to improve soil structure')
        
        # Crop recommendations based on fertility level
        if fertility_level == 'High':
            crops.extend(['Corn', 'Soybeans', 'Wheat', 'Tomatoes', 'Peppers', 'Cucumbers'])
        elif fertility_level == 'Medium':
            crops.extend(['Beans', 'Carrots', 'Lettuce', 'Spinach', 'Radishes', 'Onions'])
        else:
            crops.extend(['Clover', 'Alfalfa', 'Buckwheat', 'Rye Grass', 'Cover Crops'])
        
        return {
            'fertilizers': list(set(fertilizers)),
            'crops': crops,
            'improvements': improvements
        }
    
    def _rule_based_prediction(self, soil_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback rule-based prediction when ML model is not available
        """
        score = 0
        reasons = []
        
        # Nitrogen analysis
        if soil_data['nitrogen'] < 20:
            reasons.append('Low nitrogen levels detected - affects plant growth')
            score += 10
        elif soil_data['nitrogen'] > 50:
            reasons.append('Optimal nitrogen levels support healthy growth')
            score += 30
        else:
            reasons.append('Moderate nitrogen levels - adequate for most crops')
            score += 20
        
        # Phosphorus analysis
        if soil_data['phosphorus'] < 15:
            reasons.append('Phosphorus deficiency limits root development')
            score += 10
        elif soil_data['phosphorus'] > 30:
            reasons.append('Good phosphorus availability')
            score += 25
        else:
            reasons.append('Adequate phosphorus levels')
            score += 20
        
        # Potassium analysis
        if soil_data['potassium'] < 100:
            reasons.append('Low potassium affects disease resistance')
            score += 10
        elif soil_data['potassium'] > 200:
            reasons.append('Excellent potassium levels')
            score += 25
        else:
            reasons.append('Moderate potassium availability')
            score += 20
        
        # pH analysis
        if soil_data['ph'] < 6.0 or soil_data['ph'] > 8.0:
            reasons.append('pH outside optimal range affects nutrients')
            score += 5
        else:
            reasons.append('pH within optimal range')
            score += 20
        
        # Organic matter analysis
        if soil_data['organic_matter'] < 2:
            reasons.append('Low organic matter reduces soil health')
            score += 5
        elif soil_data['organic_matter'] > 4:
            reasons.append('Rich organic matter improves soil')
            score += 20
        else:
            reasons.append('Adequate organic matter')
            score += 15
        
        # Determine fertility level
        if score > 80:
            fertility_level = 'High'
        elif score > 60:
            fertility_level = 'Medium'
        else:
            fertility_level = 'Low'
        
        recommendations = self._generate_recommendations(soil_data, fertility_level)
        
        return {
            'fertility_level': fertility_level,
            'score': min(score, 100),
            'reasons': reasons,
            'recommendations': recommendations
        }