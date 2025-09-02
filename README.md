# SoilSense - AI-Powered Soil Fertility Analysis

A comprehensive web application for predicting soil fertility, providing fertilizer recommendations, and suggesting suitable crops using machine learning.

## Features

### 🌱 Core Functionality
- **Soil Fertility Prediction**: Advanced ML algorithms analyze soil composition
- **Fertilizer Recommendations**: Personalized suggestions based on soil deficiencies
- **Crop Suggestions**: Optimal crop recommendations for current soil conditions
- **Detailed Analysis**: Comprehensive reasons behind fertility predictions

### 🤖 AI Assistant
- **Text Chat**: Interactive chatbot for farming advice
- **Voice Input**: Speech recognition for hands-free interaction
- **Expert Knowledge**: Instant answers about soil health and farming

### 🔐 User Management
- **Authentication**: Secure login and registration system
- **User Profiles**: Personalized experience for each farmer
- **Session Management**: Persistent login state

### 🎨 Modern UI/UX
- **Clean Design**: White-themed, professional interface
- **Responsive Layout**: Works perfectly on all devices
- **Smooth Animations**: Engaging micro-interactions
- **Accessibility**: Built with accessibility best practices

## Technology Stack

### Frontend
- **React 18** with JavaScript
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Web Speech API** for voice recognition
- **Vite** for development and building

### Backend Structure (Ready for Django Integration)
- Modular service architecture
- Authentication service layer
- Soil analysis prediction service
- RESTful API structure preparation

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Demo Login**
   - Email: demo@example.com
   - Password: password

## Django Backend Integration

The frontend is structured to easily integrate with Django APIs:

### Required Django Endpoints

```python
# Authentication
POST /api/auth/login/
POST /api/auth/register/
POST /api/auth/logout/
GET /api/auth/user/

# Soil Analysis
POST /api/soil/analyze/
GET /api/soil/history/

# Chat
POST /api/chat/message/
```

### Django Models Structure

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class SoilAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    ph = models.FloatField()
    organic_matter = models.FloatField()
    moisture = models.FloatField()
    temperature = models.FloatField()
    location = models.CharField(max_length=255, blank=True)
    fertility_level = models.CharField(max_length=10)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class FertilizerRecommendation(models.Model):
    analysis = models.ForeignKey(SoilAnalysis, on_delete=models.CASCADE)
    fertilizer_name = models.CharField(max_length=255)
    
class CropRecommendation(models.Model):
    analysis = models.ForeignKey(SoilAnalysis, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=255)

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Django Views Structure

```python
# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
import joblib  # For loading ML model

# Load your trained ML model
model = joblib.load('path/to/your/model.pkl')

@api_view(['POST'])
def analyze_soil(request):
    """
    Analyze soil fertility using ML model
    """
    data = request.data
    
    # Extract soil parameters
    features = [
        data['nitrogen'],
        data['phosphorus'], 
        data['potassium'],
        data['ph'],
        data['organicMatter'],
        data['moisture'],
        data['temperature']
    ]
    
    # Make prediction using your ML model
    prediction = model.predict([features])[0]
    
    # Save to database
    analysis = SoilAnalysis.objects.create(
        user=request.user,
        **data,
        fertility_level=prediction['fertility_level'],
        score=prediction['score']
    )
    
    return Response({
        'fertilityLevel': prediction['fertility_level'],
        'score': prediction['score'],
        'reasons': prediction['reasons'],
        'recommendations': prediction['recommendations']
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message(request):
    """
    Handle chat messages and provide AI responses
    """
    message = request.data['message']
    
    # Process with your AI/NLP model
    response = generate_farming_advice(message)
    
    # Save chat history
    ChatMessage.objects.create(
        user=request.user,
        message=message,
        response=response
    )
    
    return Response({'response': response})
```

## Machine Learning Integration

The app is designed to integrate with your ML model:

1. **Replace** `src/services/soilAnalysis.js` with actual API calls
2. **Update** the prediction logic to use your trained model
3. **Enhance** the analysis with more sophisticated algorithms

## Project Structure

```
src/
├── components/          # React components
│   ├── AuthModal.jsx   # Authentication modal
│   ├── ChatBot.jsx     # AI chatbot interface
│   ├── Dashboard.jsx   # Main dashboard
│   ├── FertilityResults.jsx  # Results display
│   ├── Header.jsx      # Navigation header
│   └── SoilInputForm.jsx     # Soil data input
├── hooks/              # Custom React hooks
│   ├── useAuth.js      # Authentication logic
│   └── useSpeechRecognition.js  # Voice input
├── services/           # API service layers
│   ├── auth.js         # Authentication service
│   └── soilAnalysis.js # Soil prediction service
└── App.jsx            # Main application component
```

## API Integration Guide

To connect with your Django backend:

1. **Update API Base URL**: Change the base URL in service files
2. **Add Authentication Headers**: Include JWT tokens in requests
3. **Handle CORS**: Configure Django CORS settings
4. **Error Handling**: Implement proper error responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details