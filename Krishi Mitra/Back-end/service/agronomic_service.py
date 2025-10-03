import json
from typing import Dict, List, Any
from models import User, FarmProfile

class AgronomicService:
    def __init__(self):
        # Load crop database
        self.crop_database = self._load_crop_database()
        self.region_data = self._load_region_data()
    
    def _load_crop_database(self) -> Dict[str, Any]:
        """Load crop database with characteristics and requirements"""
        # In a real implementation, this would be loaded from a database
        return {
            'rice': {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'season': ['kharif'],
                'water_requirement': 'high',
                'temperature_range': [20, 35],
                'soil_ph_range': [5.5, 7.0],
                'nutrient_requirements': {
                    'nitrogen': 'high',
                    'phosphorus': 'medium',
                    'potassium': 'high'
                },
                'major_pests': ['stem_borer', 'leaf_folder', 'brown_plant_hopper'],
                'major_diseases': ['blast', 'bacterial_leaf_blight', 'sheath_blight'],
                'suitable_regions': ['west_bengal', 'uttar_pradesh', 'punjab', 'odisha', 'bihar']
            },
            'wheat': {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'season': ['rabi'],
                'water_requirement': 'medium',
                'temperature_range': [10, 25],
                'soil_ph_range': [6.0, 7.5],
                'nutrient_requirements': {
                    'nitrogen': 'high',
                    'phosphorus': 'medium',
                    'potassium': 'medium'
                },
                'major_pests': ['aphids', 'termites', 'armyworm'],
                'major_diseases': ['rust', 'loose_smut', 'karnal_bunt'],
                'suitable_regions': ['uttar_pradesh', 'punjab', 'haryana', 'madhya_pradesh']
            },
            'maize': {
                'name': 'Maize',
                'scientific_name': 'Zea mays',
                'season': ['kharif', 'rabi'],
                'water_requirement': 'medium',
                'temperature_range': [15, 30],
                'soil_ph_range': [5.5, 7.5],
                'nutrient_requirements': {
                    'nitrogen': 'high',
                    'phosphorus': 'high',
                    'potassium': 'medium'
                },
                'major_pests': ['fall_armyworm', 'stem_borer', 'aphids'],
                'major_diseases': ['turcicum_leaf_blight', 'maize_streak', 'common_rust'],
                'suitable_regions': ['karnataka', 'andhra_pradesh', 'maharashtra', 'bihar']
            },
            'cotton': {
                'name': 'Cotton',
                'scientific_name': 'Gossypium hirsutum',
                'season': ['kharif'],
                'water_requirement': 'medium',
                'temperature_range': [20, 35],
                'soil_ph_range': [5.5, 7.5],
                'nutrient_requirements': {
                    'nitrogen': 'medium',
                    'phosphorus': 'high',
                    'potassium': 'high'
                },
                'major_pests': ['bollworm', 'aphids', 'whitefly'],
                'major_diseases': ['boll_rot', 'alternaria_leaf_spot', 'bacterial_blight'],
                'suitable_regions': ['gujarat', 'maharashtra', 'telangana', 'andhra_pradesh']
            }
        }
    
    def _load_region_data(self) -> Dict[str, Any]:
        """Load region-specific agricultural data"""
        # In a real implementation, this would be loaded from a database
        return {
            'west_bengal': {
                'name': 'West Bengal',
                'climate': 'tropical_wet',
                'predominant_crops': ['rice', 'jute', 'tea'],
                'soil_types': ['alluvial', 'red_loamy'],
                'avg_rainfall': 1500,
                'growing_seasons': ['kharif', 'rabi']
            },
            'uttar_pradesh': {
                'name': 'Uttar Pradesh',
                'climate': 'subtropical',
                'predominant_crops': ['rice', 'wheat', 'sugarcane'],
                'soil_types': ['alluvial', 'red_loamy'],
                'avg_rainfall': 900,
                'growing_seasons': ['kharif', 'rabi', 'zaid']
            },
            'punjab': {
                'name': 'Punjab',
                'climate': 'subtropical',
                'predominant_crops': ['wheat', 'rice', 'cotton'],
                'soil_types': ['alluvial', 'sandy_loam'],
                'avg_rainfall': 600,
                'growing_seasons': ['kharif', 'rabi']
            },
            'bihar': {
                'name': 'Bihar',
                'climate': 'subtropical',
                'predominant_crops': ['rice', 'wheat', 'maize'],
                'soil_types': ['alluvial', 'clay_loam'],
                'avg_rainfall': 1200,
                'growing_seasons': ['kharif', 'rabi']
            },
            'gujarat': {
                'name': 'Gujarat',
                'climate': 'tropical_wet_dry',
                'predominant_crops': ['cotton', 'groundnut', 'sugarcane'],
                'soil_types': ['black_cotton', 'alluvial'],
                'avg_rainfall': 800,
                'growing_seasons': ['kharif', 'rabi']
            },
            'maharashtra': {
                'name': 'Maharashtra',
                'climate': 'tropical_wet_dry',
                'predominant_crops': ['cotton', 'sugarcane', 'jowar'],
                'soil_types': ['black_cotton', 'red_loamy'],
                'avg_rainfall': 800,
                'growing_seasons': ['kharif', 'rabi']
            }
        }
    
    def get_crop_recommendations(self, user: User) -> Dict[str, Any]:
        """Get crop recommendations based on user's location and soil data"""
        # Get user's farm profile
        farm_profile = FarmProfile.query.filter_by(user_id=user.id).first()
        
        # Default values if no profile exists
        location = user.location or 'bihar'  # Default to Bihar
        soil_type = farm_profile.soil_type if farm_profile else 'alluvial'
        
        # Get region data
        region = self.region_data.get(location.lower().replace(' ', '_'), self.region_data['bihar'])
        
        # Get suitable crops for the region
        suitable_crops = []
        for crop_name, crop_data in self.crop_database.items():
            if location.lower().replace(' ', '_') in [r.lower().replace(' ', '_') for r in crop_data['suitable_regions']]:
                suitable_crops.append({
                    'name': crop_data['name'],
                    'scientific_name': crop_data['scientific_name'],
                    'seasons': crop_data['season'],
                    'suitability_score': self._calculate_suitability_score(crop_data, soil_type, region)
                })
        
        # Sort by suitability score
        suitable_crops.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return {
            'region': region['name'],
            'soil_type': soil_type,
            'recommended_crops': suitable_crops[:5],  # Top 5 recommendations
            'predominant_crops': region['predominant_crops']
        }
    
    def _calculate_suitability_score(self, crop_data: Dict, soil_type: str, region_data: Dict) -> float:
        """Calculate a suitability score for a crop in a region"""
        score = 0.0
        
        # Check if soil type is suitable
        if soil_type in ['alluvial', 'red_loamy', 'clay_loam', 'sandy_loam', 'black_cotton']:
            score += 0.3  # Base score for common soil types
        
        # Check climate suitability
        if region_data['climate'] in ['tropical_wet', 'subtropical']:
            score += 0.3
        
        # Check if crop is predominant in the region
        if crop_data['name'].lower() in [c.lower() for c in region_data['predominant_crops']]:
            score += 0.4
        
        return score
    
    def get_crop_advisory(self, user: User, crop_name: str) -> Dict[str, Any]:
        """Get detailed advisory for a specific crop"""
        crop_name = crop_name.lower()
        
        # Get crop data
        crop_data = self.crop_database.get(crop_name)
        if not crop_data:
            return {'error': 'Crop not found'}
        
        # Get user's farm profile
        farm_profile = FarmProfile.query.filter_by(user_id=user.id).first()
        
        # Generate advisory based on current season
        current_month = datetime.datetime.now().month
        current_season = self._get_current_season(current_month)
        
        # Check if crop is suitable for current season
        if current_season not in crop_data['season']:
            return {
                'crop': crop_data['name'],
                'advisory': f"{crop_data['name']} is not suitable for {current_season} season.",
                'suitable_seasons': crop_data['season']
            }
        
        # Generate season-specific advisory
        advisory = {
            'crop': crop_data['name'],
            'scientific_name': crop_data['scientific_name'],
            'current_season': current_season,
            'sowing_time': self._get_sowing_time(crop_data, current_season),
            'nutrient_requirements': crop_data['nutrient_requirements'],
            'water_requirements': {
                'level': crop_data['water_requirement'],
                'irrigation_schedule': self._get_irrigation_schedule(crop_data, current_season)
            },
            'pest_warnings': self._get_pest_warnings(crop_data),
            'disease_warnings': self._get_disease_warnings(crop_data),
            'harvest_time': self._get_harvest_time(crop_data, current_season)
        }
        
        return advisory
    
    def _get_current_season(self, month: int) -> str:
        """Determine current season based on month"""
        if month in [6, 7, 8]:  # June, July, August
            return 'kharif'
        elif month in [10, 11, 12, 1]:  # October to January
            return 'rabi'
        else:  # March to May
            return 'zaid'
    
    def _get_sowing_time(self, crop_data: Dict, season: str) -> str:
        """Get recommended sowing time for a crop in a season"""
        sowing_times = {
            'kharif': {
                'rice': 'June-July',
                'maize': 'June-July',
                'cotton': 'April-May'
            },
            'rabi': {
                'wheat': 'October-November',
                'mustard': 'October-November'
            },
            'zaid': {
                'maize': 'February-March',
                'watermelon': 'March-April'
            }
        }
        
        return sowing_times.get(season, {}).get(crop_data['name'].lower(), 'Check local recommendations')
    
    def _get_irrigation_schedule(self, crop_data: Dict, season: str) -> str:
        """Get irrigation schedule for a crop"""
        if crop_data['water_requirement'] == 'high':
            return 'Irrigate every 3-4 days during dry spells'
        elif crop_data['water_requirement'] == 'medium':
            return 'Irrigate every 7-10 days during dry spells'
        else:
            return 'Irrigate only when necessary'
    
    def _get_pest_warnings(self, crop_data: Dict) -> List[Dict]:
        """Get pest warnings for a crop"""
        warnings = []
        for pest in crop_data['major_pests']:
            warnings.append({
                'pest': pest.replace('_', ' ').title(),
                'symptoms': self._get_pest_symptoms(pest),
                'treatment': self._get_pest_treatment(pest)
            })
        return warnings
    
    def _get_disease_warnings(self, crop_data: Dict) -> List[Dict]:
        """Get disease warnings for a crop"""
        warnings = []
        for disease in crop_data['major_diseases']:
            warnings.append({
                'disease': disease.replace('_', ' ').title(),
                'symptoms': self._get_disease_symptoms(disease),
                'treatment': self._get_disease_treatment(disease)
            })
        return warnings
    
    def _get_pest_symptoms(self, pest: str) -> str:
        """Get symptoms for a pest"""
        symptoms = {
            'stem_borer': 'Dead hearts in young plants, white ears in older plants',
            'leaf_folder': 'Leaves folded and whitish patches',
            'brown_plant_hopper': 'Yellowing and drying of plants',
            'aphids': 'Yellowing and curling of leaves',
            'termites': 'Dead seedlings and damaged roots',
            'armyworm': 'Irregular holes in leaves and stems',
            'fall_armyworm': 'Greasy appearance and skeletonized leaves',
            'bollworm': 'Flower buds and bolls damaged',
            'whitefly': 'Yellowing of leaves and sooty mold'
        }
        return symptoms.get(pest, 'Visible damage to plants')
    
    def _get_pest_treatment(self, pest: str) -> str:
        """Get treatment for a pest"""
        treatments = {
            'stem_borer': 'Apply cartap hydrochloride or fipronil granules',
            'leaf_folder': 'Spray cartap hydrochloride or chlorpyriphos',
            'brown_plant_hopper': 'Spray buprofezin or acephate',
            'aphids': 'Spray dimethoate or imidacloprid',
            'termites': 'Apply chlorpyriphos in soil',
            'armyworm': 'Spray spinosad or emamectin benzoate',
            'fall_armyworm': 'Spray spinosad or indoxacarb',
            'bollworm': 'Spray spinosad or emamectin benzoate',
            'whitefly': 'Spray imidacloprid or thiamethoxam'
        }
        return treatments.get(pest, 'Consult local agricultural extension office')
    
    def _get_disease_symptoms(self, disease: str) -> str:
        """Get symptoms for a disease"""
        symptoms = {
            'blast': 'Diamond-shaped lesions on leaves, neck rot',
            'bacterial_leaf_blight': 'Water-soaked lesions turning yellow',
            'sheath_blight': 'Oval lesions on sheaths, rotting',
            'rust': 'Reddish-brown pustules on leaves',
            'loose_smut': 'Black powdery mass in grains',
            'karnal_bunt': 'Black powdery mass with fishy odor',
            'turcicum_leaf_blight': 'Elliptical grayish-green lesions',
            'maize_streak': 'Chlorotic streaks on leaves',
            'common_rust': 'Reddish-brown pustules on leaves',
            'boll_rot': 'Water-soaked lesions on bolls',
            'alternaria_leaf_spot': 'Brown spots with concentric rings',
            'bacterial_blight': 'Water-soaked lesions with yellow halo'
        }
        return symptoms.get(disease, 'Visible disease symptoms')
    
    def _get_disease_treatment(self, disease: str) -> str:
        """Get treatment for a disease"""
        treatments = {
            'blast': 'Spray tricyclazole or carbendazim',
            'bacterial_leaf_blight': 'Spray streptocycline or validamycin',
            'sheath_blight': 'Spray validamycin or kasugamycin',
            'rust': 'Spray propiconazole or tebuconazole',
            'loose_smut': 'Treat seeds with carboxin or thiram',
            'karnal_bunt': 'Treat seeds with carboxin or thiram',
            'turcicum_leaf_blight': 'Spray mancozeb or azoxystrobin',
            'maize_streak': 'Remove infected plants, control leafhoppers',
            'common_rust': 'Spray mancozeb or propiconazole',
            'boll_rot': 'Spray carbendazim or thiophanate-methyl',
            'alternaria_leaf_spot': 'Spray mancozeb or copper oxychloride',
            'bacterial_blight': 'Spray streptocycline or validamycin'
        }
        return treatments.get(disease, 'Consult local agricultural extension office')
    
    def _get_harvest_time(self, crop_data: Dict, season: str) -> str:
        """Get harvest time for a crop"""
        harvest_times = {
            'kharif': {
                'rice': 'September-October',
                'maize': 'September-October',
                'cotton': 'November-December'
            },
            'rabi': {
                'wheat': 'April-May',
                'mustard': 'March-April'
            },
            'zaid': {
                'maize': 'June-July',
                'watermelon': 'May-June'
            }
        }
        
        return harvest_times.get(season, {}).get(crop_data['name'].lower(), 'Check local recommendations')