from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from utils.database import db
from config import Config
from auth import auth_bp
from api.cswhat import chat_bp
from api.weather import weather_bp
from api.market import market_bp
from api.soil import soil_bp
from api.pest import pest_bp
import os

def create_app():
    app = Flask(__name__, static_folder='../frontend')
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(soil_bp, url_prefix='/api/soil')
    app.register_blueprint(pest_bp, url_prefix='/api/pest')
    
    # Enable CORS
    CORS(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Serve frontend
    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../frontend', path)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)