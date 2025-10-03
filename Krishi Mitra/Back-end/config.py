import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///kisanmitra.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = {
        'en': 'English',
        'pa': 'Punjabi',
        'hi': 'Hindi',
        'te': 'Telugu',
        'ta': 'Tamil',
        'bn': 'Bengali'
    }
    
    # Weather API Configuration
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'your-weather-api-key'
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"
    
    # Market API Configuration
    MARKET_API_KEY = os.environ.get('MARKET_API_KEY') or 'your-market-api-key'
    MARKET_API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    # ML Model Path
    PEST_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml_models', 'pest_detection.h5')