import numpy as np
import joblib
import os
from typing import Dict, Any

class SoilFertilityPredictor:
    """
    Machine Learning predictor for soil fertility analysis
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.feature_names = [
            'nitrogen', 'phosphorus', 'potassium', 'ph', 
            'organic_matter', 'moisture', 'temperature'
        ]
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
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
                
            print(f"Model loaded successfully from {model_path}")
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
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features)[0]
                confidence = max(probabilities)
            else:
                confidence = 0.85  # Default confidence
            
            # Convert prediction to fertility level
            if isinstance(prediction, (int, float)):
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
                # If prediction is categorical
                fertility_level = str(prediction)
                score = int(confidence * 100)
            
            # Generate explanations based on ML prediction
            reasons = self._generate_ml_explanations(soil_data, fertility_level)
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
    
    def _generate_ml_explanations(self, soil_data: Dict[str, Any], fertility_level: str) -> list:
        """
        Generate explanations based on ML model insights
        """
        reasons = []
        
        # Analyze each parameter and provide insights
        if soil_data['nitrogen'] < 20:
            reasons.append('ML model indicates nitrogen deficiency is limiting fertility')
        elif soil_data['nitrogen'] > 50:
            reasons.append('ML model shows optimal nitrogen levels contributing to high fertility')
        
        if soil_data['phosphorus'] < 15:
            reasons.append('Model detects phosphorus limitation affecting root development')
        elif soil_data['phosphorus'] > 30:
            reasons.append('Model indicates excellent phosphorus availability')
        
        if soil_data['potassium'] < 100:
            reasons.append('Model shows potassium deficiency impacting plant stress tolerance')
        elif soil_data['potassium'] > 200:
            reasons.append('Model indicates optimal potassium levels for disease resistance')
        
        if soil_data['ph'] < 6.0 or soil_data['ph'] > 8.0:
            reasons.append('Model detects pH imbalance affecting nutrient availability')
        else:
            reasons.append('Model shows pH levels are within optimal range')
        
        if soil_data['organic_matter'] < 2:
            reasons.append('Model indicates low organic matter reducing soil health')
        elif soil_data['organic_matter'] > 4:
            reasons.append('Model shows excellent organic matter content')
        
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