import requests
import numpy as np
from typing import Dict, List, Any, TypedDict, Optional
from datetime import datetime, timedelta
from models import MarketCache, db


# ---------- TypedDicts for structured data ----------

class MarketData(TypedDict):
    crop: str
    state: str
    district: str
    current_price: float
    previous_price: float
    trend: str
    change_percent: float
    unit: str
    market: str
    timestamp: str


class HistoricalPrice(TypedDict):
    date: str   # YYYY-MM
    price: float
    month: int
    year: int


class ForecastPrice(TypedDict):
    date: str   # YYYY-MM
    price: float
    month: int
    year: int
    lower_bound: float
    upper_bound: float


class MarketComparison(TypedDict):
    crop: str
    state: str
    markets: List[Dict[str, Any]]
    min_price: Dict[str, Any]
    max_price: Dict[str, Any]
    price_range: float


class PriceForecast(TypedDict):
    crop: str
    state: str
    historical_data: List[HistoricalPrice]
    forecast: List[ForecastPrice]
    confidence: float


# ---------- Service Class ----------

class MarketService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.agmarknet.gov.in"  # Example API URL
    
    # ----------------- Market Prices -----------------
    def get_market_prices(self, crop: str, state: str, district: Optional[str] = None) -> MarketData:
        """Get current market prices for a crop"""
        # Check cache first
        cache_key = f"{crop}_{state}_{district or 'all'}"
        cached_data = MarketCache.query.filter(
            MarketCache.crop == crop,
            MarketCache.location == cache_key,
            MarketCache.expires_at > datetime.utcnow()
        ).first()
        
        if cached_data:
            return cached_data.data
        
        # Make API request
        params: Dict[str, str] = {
            'crop': crop,
            'state': state,
            'api_key': self.api_key
        }
        if district:
            params['district'] = district
        
        response = requests.get(f"{self.base_url}/prices", params=params)
        data = response.json()
        
        # Process data
        processed_data: MarketData = self._process_market_data(data)
        
        # Cache the data (expires in 6 hours)
        cache_entry = MarketCache(
            crop=crop,
            location=cache_key,
            data=processed_data,
            expires_at=datetime.utcnow() + timedelta(hours=6)
        )
        db.session.add(cache_entry)
        db.session.commit()
        
        return processed_data
    
    def _process_market_data(self, data: Dict[str, Any]) -> MarketData:
        """Process market price data"""
        current_price = float(data.get('current_price', 2100))
        previous_price = float(data.get('previous_price', 2050))
        
        if current_price > previous_price:
            trend = 'up'
            change_percent = ((current_price - previous_price) / previous_price) * 100
        else:
            trend = 'down'
            change_percent = ((previous_price - current_price) / previous_price) * 100
        
        return {
            'crop': data.get('crop', 'wheat'),
            'state': data.get('state', 'Delhi'),
            'district': data.get('district', 'All Districts'),
            'current_price': current_price,
            'previous_price': previous_price,
            'trend': trend,
            'change_percent': round(float(change_percent), 2),
            'unit': data.get('unit', 'quintal'),
            'market': data.get('market', 'Delhi Mandi'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    # ----------------- Forecast -----------------
    def get_price_forecast(self, crop: str, state: str, months: int = 12) -> PriceForecast:
        """Get price forecast for a crop"""
        historical_data = self._get_historical_prices(crop, state)
        forecast = self._generate_forecast(historical_data, months)
        
        return {
            'crop': crop,
            'state': state,
            'historical_data': historical_data,
            'forecast': forecast,
            'confidence': self._calculate_forecast_confidence(historical_data)
        }
    
    def _get_historical_prices(self, crop: str, state: str) -> List[HistoricalPrice]:
        """Get historical price data for a crop"""
        base_price = 2000.0
        prices: List[HistoricalPrice] = []
        
        for i in range(24):  # 24 months of historical data
            month = datetime.now() - timedelta(days=30 * i)
            seasonal_factor = 1 + 0.1 * float(np.sin(2 * np.pi * (month.month - 1) / 12))
            random_factor = 1 + 0.05 * float(np.random.randn())
            price = float(base_price * seasonal_factor * random_factor)
            
            prices.append({
                'date': month.strftime('%Y-%m'),
                'price': round(price, 2),
                'month': month.month,
                'year': month.year
            })
        
        return prices[::-1]
    
    def _generate_forecast(self, historical_data: List[HistoricalPrice], months: int) -> List[ForecastPrice]:
        """Generate price forecast"""
        prices = [item['price'] for item in historical_data]
        forecast: List[ForecastPrice] = []
        
        if len(prices) >= 2:
            trend = (prices[-1] - prices[0]) / len(prices)
        else:
            trend = 0.0
        
        last_price = float(prices[-1])
        last_date = datetime.strptime(historical_data[-1]['date'], '%Y-%m')
        
        for i in range(1, months + 1):
            forecast_date = last_date + timedelta(days=30 * i)
            forecast_month = forecast_date.month
            
            seasonal_factor = 1 + 0.1 * float(np.sin(2 * np.pi * (forecast_month - 1) / 12))
            forecast_price = last_price + trend * i
            forecast_price = float(forecast_price * seasonal_factor)
            forecast_price = float(forecast_price * (1 + 0.03 * np.random.randn()))
            
            forecast.append({
                'date': forecast_date.strftime('%Y-%m'),
                'price': round(forecast_price, 2),
                'month': forecast_month,
                'year': forecast_date.year,
                'lower_bound': round(forecast_price * 0.9, 2),
                'upper_bound': round(forecast_price * 1.1, 2)
            })
        
        return forecast
    
    def _calculate_forecast_confidence(self, historical_data: List[HistoricalPrice]) -> float:
        """Calculate confidence level for forecast"""
        if len(historical_data) < 6:
            return 0.5
        
        prices = [item['price'] for item in historical_data]
        mean_price = float(np.mean(prices))
        std_price = float(np.std(prices))
        cv = std_price / mean_price if mean_price > 0 else 1.0
        
        confidence = max(0.3, 1 - cv)
        return float(round(confidence, 2))
    
    # ----------------- Market Comparison -----------------
    def get_market_comparison(self, crop: str, state: str) -> MarketComparison:
        """Compare market prices across different markets"""
        market_data = [
            {'market': 'Delhi Mandi', 'price': 2100},
            {'market': 'Kolkata Mandi', 'price': 2050},
            {'market': 'Mumbai Mandi', 'price': 2150},
            {'market': 'Chennai Mandi', 'price': 2200},
            {'market': 'Bangalore Mandi', 'price': 2250}
        ]
        
        min_price = min(market_data, key=lambda x: x['price'])
        max_price = max(market_data, key=lambda x: x['price'])
        
        return {
            'crop': crop,
            'state': state,
            'markets': market_data,
            'min_price': min_price,
            'max_price': max_price,
            'price_range': max_price['price'] - min_price['price']
        }