import pytest
import json
from run import create_app
from models import db, User

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_success(client):
    response = client.post('/api/auth/register', 
        data=json.dumps({
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'

def test_register_duplicate_email(client):
    # Register first user
    client.post('/api/auth/register',
        data=json.dumps({
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        }),
        content_type='application/json'
    )
    
    # Try to register with same email
    response = client.post('/api/auth/register',
        data=json.dumps({
            'name': 'Another User',
            'email': 'test@example.com',
            'password': 'anotherpassword'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'already registered' in data['error']

def test_login_success(client):
    # Register user first
    client.post('/api/auth/register',
        data=json.dumps({
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword'
        }),
        content_type='application/json'
    )
    
    # Login
    response = client.post('/api/auth/login',
        data=json.dumps({
            'email': 'test@example.com',
            'password': 'testpassword'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'

def test_login_invalid_credentials(client):
    response = client.post('/api/auth/login',
        data=json.dumps({
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Invalid credentials' in data['error']