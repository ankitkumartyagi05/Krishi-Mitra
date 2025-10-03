import requests
import json
import requests
import json
import os
from typing import Dict, List, Any, Optional
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta   
# models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    email: Optional[str] = None

@dataclass
class FarmProfile:
    user_id: int
    farm_size: float
    location: str


class ValueChainService_old:
    def __init__(self):
        self.base_url = "https://api.kisanmitra.in"  # Example API URL

...

def get_buyers(self, crop: str, state: str, district: Optional[str] = None) -> List[Dict[str, Any]]:

        """Get list of buyers for a crop"""
        # In a real implementation, this would fetch from a database
        # For demo, we'll return mock data
        buyers = [
            {
                'id': 1,
                'name': 'ABC Traders',
                'type': 'trader',
                'location': 'Delhi',
                'contact': 'contact@abctraders.com',
                'phone': '+91-9876543210',
                'preferred_crops': ['wheat', 'rice', 'maize'],
                'price_range': [2000, 2200],
                'rating': 4.5
            },
            {
                'id': 2,
                'name': 'XYZ Foods',
                'type': 'processor',
                'location': 'Mumbai',
                'contact': 'contact@xyzfoods.com',
                'phone': '+91-9876543211',
                'preferred_crops': ['rice', 'sugarcane'],
                'price_range': [2100, 2300],
                'rating': 4.2
            },
            {
                'id': 3,
                'name': 'Agri Exports Ltd',
                'type': 'exporter',
                'location': 'Chennai',
                'contact': 'contact@agriexports.com',
                'phone': '+91-9876543212',
                'preferred_crops': ['rice', 'cotton'],
                'price_range': [2200, 2500],
                'rating': 4.7
            }
        ]
        
        # Filter by crop
        filtered_buyers = [buyer for buyer in buyers if crop.lower() in [c.lower() for c in buyer['preferred_crops']]]
        
        return filtered_buyers
    
def get_input_suppliers(self, crop: str, state: str, district: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of input suppliers"""
        # In a real implementation, this would fetch from a database
        # For demo, we'll return mock data
        suppliers = [
            {
                'id': 1,
                'name': 'Green Inputs',
                'type': 'fertilizer',
                'location': 'Delhi',
                'contact': 'contact@greeninputs.com',
                'phone': '+91-9876543210',
                'products': ['urea', 'dap', 'npk'],
                'rating': 4.3
            },
            {
                'id': 2,
                'name': 'Seeds Co',
                'type': 'seed',
                'location': 'Punjab',
                'contact': 'contact@seedsco.com',
                'phone': '+91-9876543211',
                'products': ['wheat', 'rice', 'cotton'],
                'rating': 4.6
            },
            {
                'id': 3,
                'name': 'Crop Protection',
                'type': 'pesticide',
                'location': 'Gujarat',
                'contact': 'contact@cropprotection.com',
                'phone': '+91-9876543212',
                'products': ['insecticides', 'fungicides', 'herbicides'],
                'rating': 4.4
            }
        ]
        
        return suppliers
    

def __init__(self):
    """
    Initialize the API client with base URL configuration.
    The base URL can be configured via KISANMITRA_API_URL environment variable,
    falling back to default URL if not set.
    """
    self.base_url = os.getenv("KISANMITRA_API_URL", "https://api.kisanmitra.in")

    def get_buyers(self, crop: str, state: str, district: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of buyers for a crop"""
        buyers = [
            {
                'id': 1,
                'name': 'ABC Traders',
                'type': 'trader',
                'location': 'Delhi',
                'contact': 'contact@abctraders.com',
                'phone': '+91-9876543210',
                'preferred_crops': ['wheat', 'rice', 'maize'],
                'price_range': [2000, 2200],
                'rating': 4.5
            },
            {
                'id': 2,
                'name': 'XYZ Foods',
                'type': 'processor',
                'location': 'Mumbai',
                'contact': 'contact@xyzfoods.com',
                'phone': '+91-9876543211',
                'preferred_crops': ['rice', 'sugarcane'],
                'price_range': [2100, 2300],
                'rating': 4.2
            },
            {
                'id': 3,
                'name': 'Agri Exports Ltd',
                'type': 'exporter',
                'location': 'Chennai',
                'contact': 'contact@agriexports.com',
                'phone': '+91-9876543212',
                'preferred_crops': ['rice', 'cotton'],
                'price_range': [2200, 2500],
                'rating': 4.7
            }
        ]
        filtered_buyers = [buyer for buyer in buyers if crop.lower() in [c.lower() for c in buyer['preferred_crops']]]
        return filtered_buyers

    def get_input_suppliers(self, crop: str, state: str, district: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of input suppliers"""
        suppliers = [
            {
                'id': 1,
                'name': 'Green Inputs',
                'type': 'fertilizer',
                'location': 'Delhi',
                'contact': 'contact@greeninputs.com',
                'phone': '+91-9876543210',
                'products': ['urea', 'dap', 'npk'],
                'rating': 4.3
            },
            {
                'id': 2,
                'name': 'Seeds Co',
                'type': 'seed',
                'location': 'Punjab',
                'contact': 'contact@seedsco.com',
                'phone': '+91-9876543211',
                'products': ['wheat', 'rice', 'cotton'],
                'rating': 4.6
            },
            {
                'id': 3,
                'name': 'Crop Protection',
                'type': 'pesticide',
                'location': 'Gujarat',
                'contact': 'contact@cropprotection.com',
                'phone': '+91-9876543212',
                'products': ['insecticides', 'fungicides', 'herbicides'],
                'rating': 4.4
            }
        ]
        return suppliers

    def get_logistics_providers(self, state: str, district: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of logistics providers"""
        providers = [
            {
                'id': 1,
                'name': 'Fast Transport',
                'type': 'transport',
                'location': 'Delhi',
                'contact': 'contact@fasttransport.com',
                'phone': '+91-9876543210',
                'services': ['truck', 'tempo', 'tractor'],
                'coverage': ['Delhi', 'NCR'],
                'rating': 4.2
            },
            {
                'id': 2,
                'name': 'Cold Storage',
                'type': 'warehousing',
                'location': 'Mumbai',
                'contact': 'contact@coldstorage.com',
                'phone': '+91 9555174289',
                'services': ['cold storage', 'dry storage'],
                'capacity': '1000 tons',
                'rating': 4.5
            },
            {
                'id': 3,
                'name': 'Agri Finance',
                'type': 'financial',
                'location': 'Bangalore',
                'contact': 'contact@agrifinance.com',
                'phone': '+91-9876543212',
                'services': ['crop loan', 'equipment loan', 'insurance'],
                'rating': 4.4
            }
        ]
        return providers

    def create_market_listing(self, user: User, crop: str, quantity: float, price: float) -> Dict[str, Any]:
        """Create a market listing for a farmer's produce"""
        listing_id = f"LIST_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            'listing_id': listing_id,
            'farmer_id': user.id,
            'farmer_name': user.username,
            'crop': crop,
            'quantity': quantity,
            'price': price,
            'status': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat()
        }

# Also fix these lines similarly:
# - Line where connection_id is created
# - Line where group_id is created
# - All references to datetime.datetime.utcnow() should be datetime.utcnow()
# 
def create_market_listing(self, user: User, crop: str, quantity: float, price: float) -> Dict[str, Any]:
    """Create a market listing for a farmer's produce"""
    # In a real implementation, this would save to a database
    # For demo, we'll return a mock response
    listing_id = f"LIST_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        'listing_id': listing_id,
        'farmer_id': user.id,
        'farmer_name': user.username,
        'crop': crop,
        'quantity': quantity,
        'price': price,
        'status': 'active',
        'created_at': datetime.utcnow().isoformat(),
        'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat()
    }
    def get_market_listings(self, crop: str = None, state: str = None) -> List[Dict[str, Any]]:
        """Get market listings"""
        # In a real implementation, this would fetch from a database
        # For demo, we'll return mock data
        listings = [
            {
                'listing_id': 'LIST_20230101120000',
                'farmer_name': 'Ram Singh',
                'crop': 'wheat',
                'quantity': 50,
                'price': 2100,
                'location': 'Delhi',
                'created_at': '2023-01-01T12:00:00',
                'status': 'active'
            },
            {
                'listing_id': 'LIST_20230102120000',
                'farmer_name': 'Lakshmi Devi',
                'crop': 'rice',
                'quantity': 30,
                'price': 3500,
                'location': 'Kolkata',
                'created_at': '2023-01-02T12:00:00',
                'status': 'active'
            },
            {
                'listing_id': 'LIST_20230103120000',
                'farmer_name': 'Rajesh Kumar',
                'crop': 'cotton',
                'quantity': 20,
                'price': 5800,
                'location': 'Mumbai',
                'created_at': '2023-01-03T12:00:00',
                'status': 'active'
            }
        ]
        
        # Filter by crop and state if provided
        if crop:
            listings = [listing for listing in listings if listing['crop'] == crop]
        
        if state:
            listings = [listing for listing in listings if listing['location'] == state]
        
        return listings
    
    def connect_with_buyer(self, listing_id: str, buyer_id: str, user: User) -> Dict[str, Any]:
        """Connect a farmer with a buyer"""
        # In a real implementation, this would create a connection and notify both parties
        # For demo, we'll return a mock response
        connection_id = f"CONN_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            'connection_id': connection_id,
            'listing_id': listing_id,
            'buyer_id': buyer_id,
            'farmer_id': user.id,
            'status': 'pending',
            'created_at': datetime.datetime.utcnow().isoformat(),
            'message': 'Connection request sent. Waiting for buyer response.'
        }
    
    def create_group_procurement(self, user: User, crop: str, quantity: float) -> Dict[str, Any]:
        """Create a group procurement request"""
        # In a real implementation, this would save to a database
        # For demo, we'll return a mock response
        group_id = f"GROUP_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            'group_id': group_id,
            'organizer_id': user.id,
            'organizer_name': user.username,
            'crop': crop,
            'quantity': quantity,
            'members': [user.id],
            'status': 'open',
            'created_at': datetime.datetime.utcnow().isoformat(),
            'expires_at': (datetime.datetime.utcnow() + timedelta(days=3)).isoformat()
        }
    
    def get_group_procurements(self, crop: str = None, state: str = None) -> List[Dict[str, Any]]:
        """Get group procurement requests"""
        # In a real implementation, this would fetch from a database
        # For demo, we'll return mock data
        groups = [
            {
                'group_id': 'GROUP_20230101120000',
                'organizer_name': 'Ram Singh',
                'crop': 'fertilizer',
                'quantity': 100,
                'members': 5,
                'location': 'Delhi',
                'created_at': '2023-01-01T12:00:00',
                'status': 'open'
            },
            {
                'group_id': 'GROUP_20230102120000',
                'organizer_name': 'Lakshmi Devi',
                'crop': 'seeds',
                'quantity': 50,
                'members': 3,
                'location': 'Kolkata',
                'created_at': '2023-01-02T12:00:00',
                'status': 'open'
            },
            {
                'group_id': 'GROUP_20230103120000',
                'organizer_name': 'Rajesh Kumar',
                'crop': 'pesticides',
                'quantity': 30,
                'members': 7,
                'location': 'Mumbai',
                'created_at': '2023-01-03T12:00:00',
                'status': 'open'
            }
        ]
        
        # Filter by crop and state if provided
        if crop:
            groups = [group for group in groups if group['crop'] == crop]
        
        if state:
            groups = [group for group in groups if group['location'] == state]
        
        return groups
    
    def join_group_procurement(self, group_id: str, user: User) -> Dict[str, Any]:
        """Join a group procurement request"""
        # In a real implementation, this would update the group membership
        # For demo, we'll return a mock response
        return {
            'group_id': group_id,
            'user_id': user.id,
            'status': 'joined',
            'message': 'Successfully joined the group procurement.'
        }