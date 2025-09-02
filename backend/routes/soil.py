from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, SoilAnalysis
from ml_predictor import SoilFertilityPredictor
import json

soil_bp = Blueprint('soil', __name__)

# Initialize ML predictor
predictor = SoilFertilityPredictor()

@soil_bp.route('/analyze', methods=['POST'])
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
            
            # Validate numeric values
            try:
                float(data[field])
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid value for {field}'}), 400
        
        # Make ML prediction
        prediction = predictor.predict_fertility(data)
        
        # Save analysis to database
        analysis = SoilAnalysis(
            user_id=user_id,
            nitrogen=float(data['nitrogen']),
            phosphorus=float(data['phosphorus']),
            potassium=float(data['potassium']),
            ph=float(data['ph']),
            organic_matter=float(data['organic_matter']),
            moisture=float(data['moisture']),
            temperature=float(data['temperature']),
            location=data.get('location', ''),
            fertility_level=prediction['fertility_level'],
            score=prediction['score'],
            reasons=json.dumps(prediction['reasons']),
            recommendations=json.dumps(prediction['recommendations'])
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify(prediction), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@soil_bp.route('/history', methods=['GET'])
@jwt_required()
def get_soil_history():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        analyses = SoilAnalysis.query.filter_by(user_id=user_id).order_by(
            SoilAnalysis.created_at.desc()
        ).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        history = []
        for analysis in analyses.items:
            history.append(analysis.to_dict())
        
        return jsonify({
            'history': history,
            'total': analyses.total,
            'pages': analyses.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@soil_bp.route('/analysis/<int:analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis_detail(analysis_id):
    try:
        user_id = get_jwt_identity()
        analysis = SoilAnalysis.query.filter_by(
            id=analysis_id, 
            user_id=user_id
        ).first()
        
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        return jsonify({'analysis': analysis.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@soil_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_user_statistics():
    try:
        user_id = get_jwt_identity()
        
        total_analyses = SoilAnalysis.query.filter_by(user_id=user_id).count()
        
        # Get fertility level distribution
        high_fertility = SoilAnalysis.query.filter_by(
            user_id=user_id, fertility_level='High'
        ).count()
        medium_fertility = SoilAnalysis.query.filter_by(
            user_id=user_id, fertility_level='Medium'
        ).count()
        low_fertility = SoilAnalysis.query.filter_by(
            user_id=user_id, fertility_level='Low'
        ).count()
        
        # Get average score
        analyses = SoilAnalysis.query.filter_by(user_id=user_id).all()
        avg_score = sum(a.score for a in analyses) / len(analyses) if analyses else 0
        
        return jsonify({
            'total_analyses': total_analyses,
            'fertility_distribution': {
                'high': high_fertility,
                'medium': medium_fertility,
                'low': low_fertility
            },
            'average_score': round(avg_score, 1)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500