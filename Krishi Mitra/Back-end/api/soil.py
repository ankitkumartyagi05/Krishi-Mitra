from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, FarmProfile
from services.agronomic_service import AgronomicService

soil_bp = Blueprint('soil', __name__)

@soil_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_soil_recommendations():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get agronomic service
    agronomic_service = AgronomicService()
    
    # Get crop recommendations
    recommendations = agronomic_service.get_crop_recommendations(user)
    
    return jsonify(recommendations)

@soil_bp.route('/advisory', methods=['GET'])
@jwt_required()
def get_crop_advisory():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get crop name from request
    crop_name = request.args.get('crop', 'rice')
    
    # Get agronomic service
    agronomic_service = AgronomicService()
    
    # Get crop advisory
    advisory = agronomic_service.get_crop_advisory(user, crop_name)
    
    return jsonify(advisory)