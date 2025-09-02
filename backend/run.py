from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.soil import soil_bp
from routes.chat import chat_bp
from config import config
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=['http://localhost:5173'])  # Vite dev server
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(soil_bp, url_prefix='/api/soil')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create demo user if it doesn't exist
        from models import User
        from werkzeug.security import generate_password_hash
        
        demo_user = User.query.filter_by(email='demo@example.com').first()
        if not demo_user:
            demo_user = User(
                name='Demo User',
                email='demo@example.com',
                password_hash=generate_password_hash('password')
            )
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created: demo@example.com / password")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)