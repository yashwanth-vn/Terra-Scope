from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import joblib
import numpy as np
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soilsense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    soil_analyses = db.relationship('SoilAnalysis', backref='user', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True)

class SoilAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Soil parameters
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    organic_matter = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    
    # Results
    fertility_level = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    reasons = db.Column(db.Text, nullable=False)  # JSON string
    recommendations = db.Column(db.Text, nullable=False)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ML Model Class (placeholder for your actual model)
class SoilFertilityPredictor:
    def __init__(self):
        # Load your trained ML model here
        # self.model = joblib.load('path/to/your/model.pkl')
        self.model = None  # Placeholder
    
    def predict_fertility(self, soil_data):
        """
        Predict soil fertility using ML model
        Replace this with your actual ML model prediction
        """
        # Extract features for ML model
        features = np.array([[
            soil_data['nitrogen'],
            soil_data['phosphorus'],
            soil_data['potassium'],
            soil_data['ph'],
            soil_data['organic_matter'],
            soil_data['moisture'],
            soil_data['temperature']
        ]])
        
        # If you have a trained model, use it like this:
        # prediction = self.model.predict(features)[0]
        # probability = self.model.predict_proba(features)[0]
        
        # For now, using rule-based logic (replace with your ML model)
        return self._rule_based_prediction(soil_data)
    
    def _rule_based_prediction(self, data):
        """
        Rule-based prediction logic (replace with ML model)
        """
        score = 0
        reasons = []
        fertilizers = []
        crops = []
        improvements = []
        
        # Nitrogen analysis
        if data['nitrogen'] < 20:
            reasons.append('Low nitrogen levels detected - affects plant growth and leaf development')
            fertilizers.extend(['Urea (46-0-0)', 'Ammonium Sulfate (21-0-0)'])
            improvements.append('Apply nitrogen-rich fertilizers during growing season')
            score += 10
        elif data['nitrogen'] > 50:
            reasons.append('Optimal nitrogen levels support healthy plant growth')
            score += 30
        else:
            reasons.append('Moderate nitrogen levels - adequate for most crops')
            score += 20
        
        # Phosphorus analysis
        if data['phosphorus'] < 15:
            reasons.append('Phosphorus deficiency can limit root development and flowering')
            fertilizers.extend(['Triple Superphosphate (0-46-0)', 'Bone Meal (4-12-0)'])
            improvements.append('Increase phosphorus content for better root systems')
            score += 10
        elif data['phosphorus'] > 30:
            reasons.append('Good phosphorus availability promotes strong root development')
            score += 25
        else:
            reasons.append('Adequate phosphorus levels for normal plant development')
            score += 20
        
        # Potassium analysis
        if data['potassium'] < 100:
            reasons.append('Low potassium affects disease resistance and water regulation')
            fertilizers.extend(['Muriate of Potash (0-0-60)', 'Potassium Sulfate (0-0-50)'])
            improvements.append('Apply potassium fertilizers to improve plant stress tolerance')
            score += 10
        elif data['potassium'] > 200:
            reasons.append('Excellent potassium levels enhance disease resistance')
            score += 25
        else:
            reasons.append('Moderate potassium availability supports plant health')
            score += 20
        
        # pH analysis
        if data['ph'] < 6.0 or data['ph'] > 8.0:
            reasons.append('pH levels outside optimal range affect nutrient availability')
            if data['ph'] < 6.0:
                improvements.append('Apply agricultural lime to increase pH')
                fertilizers.append('Dolomitic Lime')
            else:
                improvements.append('Apply elemental sulfur to decrease pH')
                fertilizers.append('Elemental Sulfur')
            score += 5
        else:
            reasons.append('pH levels within optimal range for nutrient uptake')
            score += 20
        
        # Organic matter analysis
        if data['organic_matter'] < 2:
            reasons.append('Low organic matter reduces soil structure and water retention')
            improvements.append('Add compost, manure, or organic fertilizers')
            fertilizers.extend(['Compost', 'Well-aged Manure'])
            score += 5
        elif data['organic_matter'] > 4:
            reasons.append('Rich organic matter content improves soil health')
            score += 20
        else:
            reasons.append('Adequate organic matter supports soil biology')
            score += 15
        
        # Crop recommendations based on conditions
        if score > 80:
            crops.extend(['Corn', 'Soybeans', 'Wheat', 'Tomatoes', 'Peppers', 'Cucumbers'])
        elif score > 60:
            crops.extend(['Beans', 'Carrots', 'Lettuce', 'Spinach', 'Radishes', 'Onions'])
        else:
            crops.extend(['Clover', 'Alfalfa', 'Buckwheat', 'Rye Grass', 'Cover Crops'])
        
        # Determine fertility level
        if score > 80:
            fertility_level = 'High'
        elif score > 60:
            fertility_level = 'Medium'
        else:
            fertility_level = 'Low'
        
        return {
            'fertility_level': fertility_level,
            'score': min(score, 100),
            'reasons': reasons,
            'recommendations': {
                'fertilizers': list(set(fertilizers)),
                'crops': crops,
                'improvements': improvements
            }
        }

# Initialize ML predictor
predictor = SoilFertilityPredictor()

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/soil/analyze', methods=['POST'])
@jwt_required()
def analyze_soil():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate soil data
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 
                          'organic_matter', 'moisture', 'temperature']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Make ML prediction
        prediction = predictor.predict_fertility(data)
        
        # Save analysis to database
        analysis = SoilAnalysis(
            user_id=user_id,
            nitrogen=data['nitrogen'],
            phosphorus=data['phosphorus'],
            potassium=data['potassium'],
            ph=data['ph'],
            organic_matter=data['organic_matter'],
            moisture=data['moisture'],
            temperature=data['temperature'],
            location=data.get('location', ''),
            fertility_level=prediction['fertility_level'],
            score=prediction['score'],
            reasons=str(prediction['reasons']),  # Convert to JSON string
            recommendations=str(prediction['recommendations'])  # Convert to JSON string
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify(prediction), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/soil/history', methods=['GET'])
@jwt_required()
def get_soil_history():
    try:
        user_id = get_jwt_identity()
        analyses = SoilAnalysis.query.filter_by(user_id=user_id).order_by(
            SoilAnalysis.created_at.desc()
        ).limit(10).all()
        
        history = []
        for analysis in analyses:
            history.append({
                'id': analysis.id,
                'fertility_level': analysis.fertility_level,
                'score': analysis.score,
                'location': analysis.location,
                'created_at': analysis.created_at.isoformat()
            })
        
        return jsonify({'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/message', methods=['POST'])
@jwt_required()
def chat_message():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        
        # Generate AI response (replace with your AI model)
        response = generate_farming_advice(message)
        
        # Save chat message
        chat = ChatMessage(
            user_id=user_id,
            message=message,
            response=response
        )
        
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({'response': response}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_farming_advice(message):
    """
    Generate farming advice based on user message
    Replace this with your AI/NLP model
    """
    message_lower = message.lower()
    
    if 'nitrogen' in message_lower:
        return 'Nitrogen is crucial for plant growth and leaf development. Signs of deficiency include yellowing leaves (chlorosis). To boost nitrogen: use urea (46-0-0), ammonium sulfate, or organic sources like compost. Apply during active growing seasons for best results.'
    elif 'phosphorus' in message_lower:
        return 'Phosphorus promotes strong root development and flowering. Deficiency shows as purple leaf discoloration and poor root systems. Recommended sources: triple superphosphate (0-46-0), bone meal, or rock phosphate. Apply before planting for root establishment.'
    elif 'potassium' in message_lower:
        return 'Potassium enhances disease resistance and water regulation. Low levels cause leaf edge burning and weak stems. Use muriate of potash (0-0-60), potassium sulfate, or wood ash. Essential during fruit development and stress periods.'
    elif 'ph' in message_lower or 'acid' in message_lower:
        return 'Soil pH affects nutrient availability. Most crops prefer 6.0-7.0 pH. To raise pH: apply agricultural lime. To lower pH: use elemental sulfur or organic matter. Test pH regularly as it changes slowly over time.'
    elif 'organic matter' in message_lower or 'compost' in message_lower:
        return 'Organic matter improves soil structure, water retention, and nutrient cycling. Aim for 3-5% organic matter. Add compost, well-aged manure, cover crops, or crop residues. This is the foundation of healthy soil biology.'
    elif 'crop' in message_lower or 'plant' in message_lower:
        return 'Crop selection depends on soil fertility and conditions. High fertility soils support demanding crops like corn, tomatoes, and peppers. Medium fertility works for beans, carrots, and leafy greens. Low fertility suits legumes and cover crops that improve soil.'
    elif 'fertilizer' in message_lower:
        return 'Choose fertilizers based on soil test results. NPK numbers show nitrogen-phosphorus-potassium ratios. Organic options include compost and manure. Synthetic options provide quick nutrient release. Always follow application rates to avoid over-fertilization.'
    else:
        return 'I can help you with soil fertility questions, fertilizer recommendations, crop selection, pH management, organic matter improvement, and general farming advice. What specific aspect would you like to know more about?'

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Create demo user if it doesn't exist
    demo_user = User.query.filter_by(email='demo@example.com').first()
    if not demo_user:
        demo_user = User(
            name='Demo User',
            email='demo@example.com',
            password_hash=generate_password_hash('password')
        )
        db.session.add(demo_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)