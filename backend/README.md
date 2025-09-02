# SoilSense Flask Backend

A Flask-based backend API for soil fertility prediction with machine learning integration.

## Features

- **User Authentication**: JWT-based authentication system
- **Soil Analysis**: ML-powered fertility prediction
- **Chat System**: AI assistant for farming advice
- **Data Persistence**: SQLite database with SQLAlchemy ORM
- **CORS Support**: Ready for React frontend integration

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=development
DATABASE_URL=sqlite:///soilsense.db
```

### 3. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/user` - Get current user
- `POST /api/auth/logout` - User logout

### Soil Analysis
- `POST /api/soil/analyze` - Analyze soil fertility
- `GET /api/soil/history` - Get user's analysis history
- `GET /api/soil/analysis/<id>` - Get specific analysis
- `GET /api/soil/statistics` - Get user statistics

### Chat
- `POST /api/chat/message` - Send chat message
- `GET /api/chat/history` - Get chat history

### Health Check
- `GET /api/health` - API health status

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Soil Analyses Table
```sql
CREATE TABLE soil_analyses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    nitrogen FLOAT NOT NULL,
    phosphorus FLOAT NOT NULL,
    potassium FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    organic_matter FLOAT NOT NULL,
    moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    location VARCHAR(255),
    fertility_level VARCHAR(10) NOT NULL,
    score INTEGER NOT NULL,
    reasons TEXT NOT NULL,
    recommendations TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Chat Messages Table
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Machine Learning Integration

### Current Status
- Rule-based prediction system (placeholder)
- Ready for ML model integration
- Feature preprocessing pipeline

### Integration Steps
1. Train your ML model with the 7 soil features
2. Save model using joblib: `joblib.dump(model, 'models/soil_fertility_model.pkl')`
3. Update `ml_predictor.py` to load your model
4. Replace rule-based logic with ML predictions

### Required Model Input
```python
features = [nitrogen, phosphorus, potassium, ph, organic_matter, moisture, temperature]
```

### Expected Model Output
- Classification: 'High', 'Medium', 'Low'
- Or Regression: Score 0-100

## Frontend Integration

Update your React frontend services to use these API endpoints:

```javascript
// In src/services/auth.js
const API_BASE_URL = 'http://localhost:5000/api';

// In src/services/soilAnalysis.js
const response = await fetch(`${API_BASE_URL}/soil/analyze`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(soilData)
});
```

## Demo Credentials

- **Email**: demo@example.com
- **Password**: password

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## Security Considerations

- Change default secret keys in production
- Use environment variables for sensitive data
- Implement rate limiting for API endpoints
- Add input validation and sanitization
- Use HTTPS in production
- Implement proper logging and monitoring

## Testing

```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request