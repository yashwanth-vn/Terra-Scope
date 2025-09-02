from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ChatMessage

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def chat_message():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message'].strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Generate AI response
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

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(
            ChatMessage.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        history = []
        for msg in messages.items:
            history.append(msg.to_dict())
        
        return jsonify({
            'history': history,
            'total': messages.total,
            'pages': messages.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_farming_advice(message):
    """
    Generate farming advice based on user message
    Replace this with your AI/NLP model or integrate with OpenAI API
    """
    message_lower = message.lower()
    
    # Soil nutrients advice
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
    
    # Crop and farming advice
    elif 'crop' in message_lower or 'plant' in message_lower:
        return 'Crop selection depends on soil fertility and conditions. High fertility soils support demanding crops like corn, tomatoes, and peppers. Medium fertility works for beans, carrots, and leafy greens. Low fertility suits legumes and cover crops that improve soil.'
    
    elif 'fertilizer' in message_lower:
        return 'Choose fertilizers based on soil test results. NPK numbers show nitrogen-phosphorus-potassium ratios. Organic options include compost and manure. Synthetic options provide quick nutrient release. Always follow application rates to avoid over-fertilization.'
    
    elif 'moisture' in message_lower or 'water' in message_lower:
        return 'Proper soil moisture is essential for nutrient uptake. Most crops need 40-60% soil moisture. Too little causes stress; too much can cause root rot. Improve water retention with organic matter and proper mulching.'
    
    elif 'temperature' in message_lower:
        return 'Soil temperature affects root growth and nutrient availability. Optimal range is 18-24°C for most crops. Cold soils slow nutrient uptake. Use mulch to moderate temperature and protect roots from extreme conditions.'
    
    # Pest and disease advice
    elif 'pest' in message_lower or 'insect' in message_lower:
        return 'Integrated Pest Management (IPM) combines biological, cultural, and chemical controls. Monitor regularly, encourage beneficial insects, rotate crops, and use targeted treatments only when necessary. Healthy soil often means fewer pest problems.'
    
    elif 'disease' in message_lower:
        return 'Plant diseases often indicate soil imbalances or poor drainage. Improve soil health with organic matter, ensure proper spacing for air circulation, rotate crops annually, and choose disease-resistant varieties when possible.'
    
    # Seasonal advice
    elif 'spring' in message_lower:
        return 'Spring preparation: Test soil pH and nutrients, add compost or aged manure, prepare seedbeds when soil is workable (not too wet), and plan crop rotations. Start with cool-season crops before warm-season planting.'
    
    elif 'fall' in message_lower or 'autumn' in message_lower:
        return 'Fall activities: Plant cover crops to protect soil, add organic matter, collect soil samples for testing, clean up crop residues, and plan next year\'s garden layout. Fall is ideal for soil amendments.'
    
    # General farming advice
    elif 'organic' in message_lower:
        return 'Organic farming focuses on soil health through natural methods. Use compost, cover crops, beneficial insects, and crop rotation. Avoid synthetic chemicals and build long-term soil fertility through biological processes.'
    
    elif 'irrigation' in message_lower:
        return 'Efficient irrigation conserves water and prevents disease. Water deeply but less frequently to encourage deep roots. Use drip irrigation or soaker hoses when possible. Water early morning to reduce evaporation and disease risk.'
    
    else:
        return 'I can help you with soil fertility questions, fertilizer recommendations, crop selection, pH management, organic matter improvement, pest control, seasonal planning, and general farming advice. What specific aspect would you like to know more about?'