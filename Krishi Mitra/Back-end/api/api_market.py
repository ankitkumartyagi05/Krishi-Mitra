from flask import Blueprint, app, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from services.agronomic_service import AgronomicService 
from services.weather_service import WeatherService
from services.ml_service import MLService
from services.market_service import MarketService

market_bp = Blueprint('market', __name__)

@market_bp.route('/prices', methods=['GET'])
@jwt_required()
def get_market_prices():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    crop = request.args.get('crop', 'wheat')
    state = request.args.get('state', user.location or 'Delhi')
    district = request.args.get('district')
    
    # Get market service
    market_service = MarketService(api_key=app.config['MARKET_API_KEY'])
    
    # Get market prices
    prices = market_service.get_market_prices(crop, state, district)
    
    return jsonify(prices)

@market_bp.route('/forecast', methods=['GET'])
@jwt_required()
def get_price_forecast():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    crop = request.args.get('crop', 'wheat')
    state = request.args.get('state', user.location or 'Delhi')
    months = int(request.args.get('months', 12))
    
    # Get market service
    market_service = MarketService(api_key=app.config['MARKET_API_KEY'])
    
    # Get price forecast
    forecast = market_service.get_price_forecast(crop, state, months)
    
    return jsonify(forecast)

@market_bp.route('/comparison', methods=['GET'])
@jwt_required()
def get_market_comparison():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    crop = request.args.get('crop', 'wheat')
    state = request.args.get('state', user.location or 'Delhi')
    
    # Get market service
    market_service = MarketService(api_key=app.config['MARKET_API_KEY'])
    
    # Get market comparison
    comparison = market_service.get_market_comparison(crop, state)
    
    return jsonify(comparison)