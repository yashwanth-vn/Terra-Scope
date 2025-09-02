import pytest
import json
from run import create_app
from models import db, User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Create test user
        user = User(
            name='Test User',
            email='test@example.com',
            password_hash=generate_password_hash('testpassword')
        )
        db.session.add(user)
        db.session.commit()
        
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    response = client.post('/api/auth/login',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'testpassword'
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    return data['access_token']

def test_soil_analysis_success(client, auth_token):
    soil_data = {
        'nitrogen': 25,
        'phosphorus': 20,
        'potassium': 150,
        'ph': 6.5,
        'organic_matter': 3,
        'moisture': 45,
        'temperature': 22,
        'location': 'Test Field'
    }
    
    response = client.post('/api/soil/analyze',
        data=json.dumps(soil_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'fertility_level' in data
    assert 'score' in data
    assert 'reasons' in data
    assert 'recommendations' in data

def test_soil_analysis_missing_fields(client, auth_token):
    incomplete_data = {
        'nitrogen': 25,
        'phosphorus': 20
        # Missing other required fields
    }
    
    response = client.post('/api/soil/analyze',
        data=json.dumps(incomplete_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Missing field' in data['error']

def test_soil_analysis_unauthorized(client):
    soil_data = {
        'nitrogen': 25,
        'phosphorus': 20,
        'potassium': 150,
        'ph': 6.5,
        'organic_matter': 3,
        'moisture': 45,
        'temperature': 22
    }
    
    response = client.post('/api/soil/analyze',
        data=json.dumps(soil_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401

def test_get_soil_history(client, auth_token):
    response = client.get('/api/soil/history',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'history' in data
    assert isinstance(data['history'], list)