from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    soil_analyses = db.relationship('SoilAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class SoilAnalysis(db.Model):
    __tablename__ = 'soil_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
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
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'ph': self.ph,
            'organic_matter': self.organic_matter,
            'moisture': self.moisture,
            'temperature': self.temperature,
            'location': self.location,
            'fertility_level': self.fertility_level,
            'score': self.score,
            'reasons': json.loads(self.reasons) if self.reasons else [],
            'recommendations': json.loads(self.recommendations) if self.recommendations else {},
            'created_at': self.created_at.isoformat()
        }

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'response': self.response,
            'created_at': self.created_at.isoformat()
        }