from utils.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    language = db.Column(db.String(2), default='en')
    location = db.Column(db.String(128))
    farm_size = db.Column(db.Float)  # in acres
    preferred_crops = db.Column(db.String(256))  # JSON string of crop names
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    precipitation = db.Column(db.Float)
    weather_description = db.Column(db.String(256))
    forecast_date = db.Column(db.Date)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class MarketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(64))
    state = db.Column(db.String(64))
    district = db.Column(db.String(64))
    market = db.Column(db.String(128))
    price = db.Column(db.Float)
    price_unit = db.Column(db.String(32))  # e.g., "Quintal"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class SoilData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    ph_level = db.Column(db.Float)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    organic_matter = db.Column(db.Float)
    texture = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class PestDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_path = db.Column(db.String(256))
    pest_type = db.Column(db.String(128))
    confidence = db.Column(db.Float)
    treatment_recommendation = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
class CropRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128))
    soil_type = db.Column(db.String(64))
    season = db.Column(db.String(32))  # Kharif, Rabi, Zaid
    recommended_crops = db.Column(db.String(256))  # JSON string of crop names
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)