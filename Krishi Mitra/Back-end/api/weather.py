from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, app
from services.weather_service import WeatherService
from datetime import datetime

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/current', methods=['GET'])
@jwt_required()
def get_current_weather():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's location (default to Delhi if not set)
    lat = float(request.args.get('lat', 28.6139))  # Delhi latitude
    lon = float(request.args.get('lon', 77.2090))  # Delhi longitude
    language = user.language or 'en'
    
    # Get weather data
    weather_service = WeatherService(api_key=app.config['WEATHER_API_KEY'])
    weather_data = weather_service.get_weather_data(lat, lon, language)
    
    return jsonify(weather_data)

@weather_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_weather_alerts():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's location
    lat = float(request.args.get('lat', 28.6139))
    lon = float(request.args.get('lon', 77.2090))
    language = user.language or 'en'
    
    # Get weather data
    weather_service = WeatherService(api_key=app.config['WEATHER_API_KEY'])
    weather_data = weather_service.get_weather_data(lat, lon, language)
    
    # Return only alerts
    return jsonify({
        'alerts': weather_data['analysis']['alerts'],
        'location': f"{lat},{lon}",
        'timestamp': datetime.utcnow().isoformat()
    })

@weather_bp.route('/historical', methods=['GET'])
@jwt_required()
def get_historical_weather():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get parameters
    lat = float(request.args.get('lat', 28.6139))
    lon = float(request.args.get('lon', 77.2090))
    days = int(request.args.get('days', 30))
    
    # In a real implementation, this would fetch from a historical weather database
    # For demo, we'll return mock data
    historical_data = {
        'location': f"{lat},{lon}",
        'days': days,
        'data': [
            {
                'date': (datetime.utcnow() - datetime.timedelta(days=i)).strftime('%Y-%m-%d'),
                'temperature': 25 + (i % 10),
                'rainfall': i % 20
            } for i in range(days)
        ]
    }
    
    return jsonify(historical_data)