import re
import base64
import io
from typing import Dict, List, Any, Optional
from PIL import Image
from models import User, FarmProfile
from services.ml_service import MLService

# Define INTENTS globally or load from a config file
INTENTS = {
    'fertilizer': {
        'keywords': {
            'en': ['fertilizer', 'nutrient', 'manure', 'grow', 'soil food'],
            'hi': ['उर्वरक', 'पोषक तत्व', 'खाद', 'बढ़ाना', 'मिट्टी का भोजन'],
            'pa': ['ਖਾਦ', 'ਪੋਸ਼ਕ ਤੱਤ', 'ਰੂੜੀ', 'ਵਧਾਉਣਾ', 'ਮਿੱਟੀ ਦਾ ਭੋਜਨ'],
            'te': ['ఎరువు', 'పోషకాలు', 'ఎరువు', 'పెరుగుదల', 'నేల ఆహారం'],
            'ta': ['உரம்', 'ஊட்டச்சத்து', 'எரு', 'வளர', 'மண் உணவு'],
            'bn': ['সার', 'পুষ্টি', 'গোবর', 'বৃদ্ধি', 'মাটির খাবার']
        },
        'responses': {
            'en': "Based on your crop and soil, I recommend: {recommendation}",
            'hi': "आपकी फसल और मिट्टी के आधार पर, मैं सलाह देता हूँ: {recommendation}",
            'pa': "ਤੁਹਾਡੀ ਫਸਲ ਅਤੇ ਮਿੱਟੀ ਦੇ ਆਧਾਰ 'ਤੇ, ਮੈਂ ਸਿਫ਼ਾਰਸ਼ ਕਰਦਾ ਹਾਂ: {recommendation}",
            'te': "మీ పంట మరియు నేల ఆధారంగా, నేను సిఫార్సు చేస్తున్నాను: {recommendation}",
            'ta': "உங்கள் பயிர் மற்றும் மண்ணின் அடிப்படையில், நான் பரிந்துரைக்கிறேன்: {recommendation}",
            'bn': "আপনার ফসল এবং মাটির উপর ভিত্তি করে, আমি সুপারিশ করছি: {recommendation}"
        }
    },
    'pest': {
        'keywords': {
            'en': ['pest', 'insect', 'bug', 'disease', 'infestation'],
            'hi': ['कीट', 'कीड़ा', 'रोग', 'संक्रमण'],
            'pa': ['ਕੀਟ', 'ਕੀੜਾ', 'ਰੋਗ', 'ਲਾਗ'],
            'te': ['తెగులు', 'పురుగు', 'వ్యాధి', 'సంక్రమణ'],
            'ta': ['பூச்சி', 'நோய்', 'தொற்று'],
            'bn': ['পোকা', 'রোগ', 'সংক্রমণ']
        },
        'responses': {
            'en': "For {pest_name}, I recommend: {treatment}",
            'hi': "{pest_name} के लिए, मैं सलाह देता हूँ: {treatment}",
            'pa': "{pest_name} ਲਈ, ਮੈਂ ਸਿਫ਼ਾਰਸ਼ ਕਰਦਾ ਹਾਂ: {treatment}",
            'te': "{pest_name} కోసం, నేను సిఫార్సు చేస్తున్నాను: {treatment}",
            'ta': "{pest_name} க்கு, நான் பரிந்துரைக்கிறேன்: {treatment}",
            'bn': "{pest_name} এর জন্য, আমি সুপারিশ করছি: {treatment}"
        }
    },
    'weather': {
        'keywords': {
            'en': ['weather', 'forecast', 'rain', 'temperature', 'climate'],
            'hi': ['मौसम', 'पूर्वानुमान', 'बारिश', 'तापमान', 'जलवायु'],
            'pa': ['ਮੌਸਮ', 'ਭਵਿੱਖਬਾਣੀ', 'ਮੀਂਹ', 'ਤਾਪਮਾਨ', 'ਜਲਵਾਯੂ'],
            'te': ['వాతావరణం', 'అంచనా', 'వర్షం', 'ఉష్ణోగ్రత', 'శీతోష్ణస్థితి'],
            'ta': ['வானிலை', 'முன்னறிவிப்பு', 'மழை', 'வெப்பநிலை', 'காலநிலை'],
            'bn': ['আবহাওয়া', 'পূর্বাভাস', 'বৃষ্টি', 'তাপমাত্রা', 'জলবায়ু']
        },
        'responses': {
            'en': "The weather in {location} is {condition} with a temperature of {temp}°C.",
            'hi': "{location} में मौसम {condition} है और तापमान {temp}°C है।",
            'pa': "{location} ਵਿੱਚ ਮੌਸਮ {condition} ਹੈ ਅਤੇ ਤਾਪਮਾਨ {temp}°C ਹੈ।",
            'te': "{location} లో వాతావరణం {condition} మరియు ఉష్ణోగ్రత {temp}°C.",
            'ta': "{location} இல் வானிலை {condition} மற்றும் வெப்பநிலை {temp}°C.",
            'bn': "{location} এ আবহাওয়া {condition} এবং তাপমাত্রা {temp}°C।"
        }
    },
    'market': {
        'keywords': {
            'en': ['market', 'price', 'rate', 'sell', 'buy'],
            'hi': ['बाजार', 'कीमत', 'दर', 'बेचना', 'खरीदना'],
            'pa': ['ਬਾਜ਼ਾਰ', 'ਕੀਮਤ', 'ਦਰ', 'ਵੇਚਣਾ', 'ਖਰੀਦਣਾ'],
            'te': ['మార్కెట్', 'ధర', 'రేటు', 'అమ్మకం', 'కొనుగోలు'],
            'ta': ['சந்தை', 'விலை', 'விகிதம்', 'விற்க', 'வாங்க'],
            'bn': ['বাজার', 'দাম', 'হার', 'বিক্রয়', 'কেনা']
        },
        'responses': {
            'en': "The current market price for {crop} is {price} per quintal in {mandi}.",
            'hi': "{crop} का वर्तमान बाजार मूल्य {mandi} में {price} प्रति क्विंटल है।",
            'pa': "{crop} ਦਾ ਮੌਜੂਦਾ ਬਾਜ਼ਾਰ ਮੁੱਲ {mandi} ਵਿੱਚ {price} ਪ੍ਰਤੀ ਕੁਇੰਟਲ ਹੈ।",
            'te': "{crop} యొక్క ప్రస్తుత మార్కెట్ ధర {mandi} లో {price} ప్రతి క్వింటాల్.",
            'ta': "{crop} இன் தற்போதைய சந்தை விலை {mandi} இல் {price} ஒரு குவிண்டால்.",
            'bn': "{crop} এর বর্তমান বাজার মূল্য {mandi} এ {price} প্রতি কুইন্টাল।"
        }
    },
    'soil': {
        'keywords': {
            'en': ['soil', 'health', 'nitrogen', 'phosphorus', 'potassium', 'pH'],
            'hi': ['मिट्टी', 'स्वास्थ्य', 'नाइट्रोजन', 'फास्फोरस', 'पोटेशियम', 'पीएच'],
            'pa': ['ਮਿੱਟੀ', 'ਸਿਹਤ', 'ਨਾਈਟ੍ਰੋਜਨ', 'ਫਾਸਫੋਰਸ', 'ਪੋਟਾਸ਼ੀਅਮ', 'ਪੀਐਚ'],
            'te': ['నేల', 'ఆరోగ్యం', 'నత్రజని', 'ఫాస్ఫరస్', 'పొటాషియం', 'పిహెచ్'],
            'ta': ['மண்', 'ஆரோக்கியம்', 'நைட்ரஜன்', 'பாஸ்பரஸ்', 'பொட்டாசியம்', 'pH'],
            'bn': ['মাটি', 'স্বাস্থ্য', 'নাইট্রোজেন', 'ফসফরাস', 'পটাশিয়াম', 'পিএইচ']
        },
        'responses': {
            'en': "Your soil has Nitrogen: {nitrogen_level}, Phosphorus: {phosphorus_level}, Potassium: {potassium_level}, and pH: {ph_level}.",
            'hi': "आपकी मिट्टी में नाइट्रोजन: {nitrogen_level}, फास्फोरस: {phosphorus_level}, पोटेशियम: {potassium_level}, और पीएच: {ph_level} है।",
            'pa': "ਤੁਹਾਡੀ ਮਿੱਟੀ ਵਿੱਚ ਨਾਈਟ੍ਰੋਜਨ: {nitrogen_level}, ਫਾਸਫੋਰਸ: {phosphorus_level}, ਪੋਟਾਸ਼ੀਅਮ: {potassium_level}, ਅਤੇ ਪੀਐਚ: {ph_level} ਹੈ।",
            'te': "మీ నేలలో నత్రజని: {nitrogen_level}, ఫాస్ఫరస్: {phosphorus_level}, పొటాషియం: {potassium_level}, మరియు పిహెచ్: {ph_level} ఉంది.",
            'ta': "உங்கள் மண்ணில் நைட்ரஜன்: {nitrogen_level}, பாஸ்பரஸ்: {phosphorus_level}, பொட்டாசியம்: {potassium_level}, மற்றும் pH: {ph_level} உள்ளது.",
            'bn': "আপনার মাটিতে নাইট্রোজেন: {nitrogen_level}, ফসফরাস: {phosphorus_level}, পটাশিয়াম: {potassium_level}, এবং পিএইচ: {ph_level} আছে।"
        }
    }
}

class NLPService:
    def __init__(self):
        self.ml_service = MLService()
    
    def process_message(self, message: str, language: str, image_data: Optional[str] = None) -> Dict[str, Any]:
        """Process user message to extract intent and entities"""
        # Process text
        processed_data = self._process_text(message, language)
        
        # Process image if provided
        if image_data:
            image_analysis = self._process_image(image_data)
            processed_data['image_analysis'] = image_analysis
        
        return processed_data
    
    def _process_text(self, message: str, language: str) -> Dict[str, Any]:
        """Process text message to extract intent and entities"""
        message = message.lower()
        
        # Extract intent
        detected_intent = None
        max_matches = 0
        
        for intent, data in INTENTS.items():
            # Get keywords for the specified language, default to English if not available
            keywords = data['keywords'].get(language, data['keywords']['en'])
            matches = sum(1 for keyword in keywords if keyword in message)
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent
        
        # Extract entities (simplified)
        entities = {}
        if detected_intent == 'fertilizer':
            # Extract crop type
            crops = {
                'en': ['wheat', 'rice', 'maize', 'cotton', 'sugarcane'],
                'hi': ['गेहूं', 'चावल', 'मक्का', 'कपास', 'गन्ना'],
                'pa': ['ਕਣਕ', 'ਚਾਵਲ', 'ਮੱਕੀ', 'ਕਪਾਹ', 'ਗੰਨਾ'],
                'te': ['గోధుమ', 'వరి', 'మొక్కజోన్', 'పత్తి', 'చెరకు'],
                'ta': ['கோதுமை', 'நெல்', 'சோளம்', 'பருத்தி', 'கரும்பு'],
                'bn': ['গম', 'চাল', 'ভুট্টা', 'তুলা', 'আখ']
            }
            
            crop_list = crops.get(language, crops['en'])
            for crop in crop_list:
                if crop in message:
                    entities['crop'] = crop
                    break
        
        elif detected_intent == 'pest':
            # Extract pest name
            pests = {
                'en': ['aphid', 'blight', 'rust', 'fungus', 'bollworm'],
                'hi': ['एफिड', 'ब्लाइट', 'रस्ट', 'फंगस', 'बोलवर्म'],
                'pa': ['ਐਫਿਡ', 'ਬਲਾਈਟ', 'ਰਸਟ', 'ਫੰਗਸ', 'ਬੋਲਵਰਮ'],
                'te': ['యాఫిడ్', 'బ్లైట్', 'తుప్ప', 'ఫంగస్', 'బాల్‌వేర్మ్'],
                'ta': ['ஆஃபிட்', 'பிளைட்', 'துருவம்', 'பூசணம்', 'பஞ்சுப்பூச்சி'],
                'bn': ['আফিড', 'ব্লাইট', 'রাস্ট', 'ছত্রাক', 'বোলওয়ার্ম']
            }
            
            pest_list = pests.get(language, pests['en'])
            for pest in pest_list:
                if pest in message:
                    entities['pest'] = pest
                    break
        
        elif detected_intent == 'market':
            # Extract crop name
            crops = {
                'en': ['wheat', 'rice', 'maize', 'cotton', 'sugarcane'],
                'hi': ['गेहूं', 'चावल', 'मक्का', 'कपास', 'गन्ना'],
                'pa': ['ਕਣਕ', 'ਚਾਵਲ', 'ਮੱਕੀ', 'ਕਪਾਹ', 'ਗੰਨਾ'],
                'te': ['గోధుమ', 'వరి', 'మొక్కజోన్', 'పత్తి', 'చెరకు'],
                'ta': ['கோதுமை', 'நெல்', 'சோளம்', 'பருத்தி', 'கரும்பு'],
                'bn': ['গম', 'চাল', 'ভুট্টা', 'তুলা', 'আখ']
            }
            
            crop_list = crops.get(language, crops['en'])
            for crop in crop_list:
                if crop in message:
                    entities['crop'] = crop
                    break
        
        return {
            'intent': detected_intent,
            'entities': entities,
            'language': language,
            'message': message
        }
    
    def _process_image(self, image_data: str) -> Dict[str, Any]:
        """Process image data to extract information"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            
            # Analyze image with ML service
            analysis = self.ml_service.analyze_image(image)
            
            return analysis
        except Exception as e:
            print(f"Error processing image: {e}")
            return {'error': 'Image processing failed'}
    
    def get_response(self, processed_data: Dict[str, Any], user: User) -> str:
        """Generate response based on processed message and user context"""
        intent = processed_data['intent']
        entities = processed_data['entities']
        language = processed_data['language']
        
        # Check for image analysis first
        if 'image_analysis' in processed_data and processed_data['image_analysis']:
            return self._get_image_response(processed_data['image_analysis'], language)
        
        if not intent:
            # Default response
            default_responses = {
                'en': "I'm here to help with crop selection, pest control, fertilizer advice, weather updates, and market prices. You can also send images of your crops for analysis. What would you like to know?",
                'hi': "मैं फसल चयन, कीट नियंत्रण, उर्वरक सलाह, मौसम अपडेट और बाजार मूल्यों में आपकी मदद करने के लिए यहाँ हूँ। आप विश्लेषण के लिए अपनी फसलों की छवियां भी भेज सकते हैं। आप क्या जानना चाहेंगे?",
                'pa': "ਮੈਂ ਫਸਲ ਚੋਣ, ਕੀਟ ਨਿਯੰਤਰਣ, ਖਾਦ ਸਲਾਹ, ਮੌਸਮ ਅਪਡੇਟ ਅਤੇ ਮਾਰਕੀਟ ਕੀਮਤਾਂ ਨਾਲ ਤੁਹਾਡੀ ਮਦਦ ਕਰਨ ਲਈ ਇੱਥੇ ਹਾਂ। ਤੁਸੀਂ ਆਪਣੀਆਂ ਫਸਲਾਂ ਦੀਆਂ ਤਸਵੀਰਾਂ ਵਿਸ਼ਲੇਸ਼ਣ ਲਈ ਭੇਜ ਸਕਦੇ ਹੋ। ਤੁਸੀਂ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
                'te': "నేను పంట ఎంపిక, పురుగు నియంత్రణ, ఎరువు సలహా, వాతావరణ నవీకరణలు మరియు మార్కెట్ ధరలతో మీకు సహాయం చేయడానికి ఇక్కడ ఉన్నాను. మీరు మీ పంటల చిత్రాలను విశ్లేషణ కోసం కూడా పంపవచ్చు. మీరు తెలుసుకోవాలనుకున్నారా?",
                'ta': "பயிர் தேர்வு, பூச்சி கட்டுப்பாடு, உரம் ஆலோசனை, வானிலை புதுப்பிப்புகள் மற்றும் சந்தை விலைகளுடன் உங்களுக்கு உதவ இங்கே இருக்கிறேன். பகுப்பாய்வுக்கு உங்கள் பயிர்களின் படங்களையும் அனுப்பலாம். நீங்கள் என்ன தெரிந்துகொள்ள விரும்புகிறீர்கள்?",
                'bn': "আমি ফসল নির্বাচন, পোকা নিয়ন্ত্রণ, সার পরামর্শ, আবহাওয়া আপডেট এবং বাজার মূল্যের সাথে আপনাকে সাহায্য করতে এখানে। আপনি বিশ্লেষণের জন্য আপনার ফসলের ছবিও পাঠাতে পারেন। আপনি কি জানতে চান?"
            }
            return default_responses.get(language, default_responses['en'])
        
        # Get intent-specific response
        response_template = INTENTS[intent]['responses'].get(language, INTENTS[intent]['responses']['en'])
        
        # Fill in template with user-specific data
        if intent == 'fertilizer':
            recommendation = self._get_fertilizer_recommendation(user, entities.get('crop'), language)
            return response_template.format(recommendation=recommendation)
        
        elif intent == 'pest':
            pest_name = entities.get('pest', 'unknown pest')
            treatment = self._get_pest_treatment(pest_name, language)
            return response_template.format(pest_name=pest_name, treatment=treatment)
        
        elif intent == 'weather':
            location = user.location or 'your area'
            condition = 'sunny'
            temp = '32'
            return response_template.format(location=location, condition=condition, temp=temp)
        
        elif intent == 'market':
            crop = entities.get('crop', 'crop')
            price = '2100'
            mandi = 'Delhi'
            return response_template.format(crop=crop, price=price, mandi=mandi)
        
        elif intent == 'soil':
            nitrogen_level = 'medium'
            phosphorus_level = 'low'
            potassium_level = 'high'
            ph_level = '6.8'
            return response_template.format(
                nitrogen_level=nitrogen_level,
                phosphorus_level=phosphorus_level,
                potassium_level=potassium_level,
                ph_level=ph_level
            )
        
        return response_template
    
    def _get_image_response(self, image_analysis: Dict, language: str) -> str:
        """Generate response based on image analysis"""
        if 'error' in image_analysis:
            return "Sorry, I couldn't analyze the image. Please try again with a clearer image."
        
        # Check if pest or disease was detected
        if 'pest' in image_analysis:
            pest = image_analysis['pest']
            confidence = image_analysis.get('confidence', 0)
            
            if confidence > 0.8:
                responses = {
                    'en': f"I've detected {pest} in your crop with high confidence. I recommend applying {self._get_pest_treatment(pest, 'en')}.",
                    'hi': f"मैं आपकी फसल में {pest} का पता लगाया है जिसमें उच्च विश्वास है। मैं {self._get_pest_treatment(pest, 'hi')} लगाने की सिफारिश करता हूं।",
                    'pa': f"ਮੈਂ ਤੁਹਾਡੀ ਫਸਲ ਵਿੱਚ {pest} ਦੀ ਖੋਜ ਕੀਤੀ ਹੈ ਜਿਸ ਵਿੱਚ ਉੱਚ ਵਿਸ਼ਵਾਸ ਹੈ। ਮੈਂ {self._get_pest_treatment(pest, 'pa')} ਲਾਉਣ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕਰਦਾ ਹਾਂ।",
                    'te': f"నేను మీ పంటలో {pest} గుర్తించాను, దీనికి అధిక విశ్వాసం ఉంది. నేను {self._get_pest_treatment(pest, 'te')} వర్తింపజేయమని సిఫార్సు చేస్తున్నాను.",
                    'ta': f"நான் உங்கள் பயிரில் {pest} கண்டறினேன், இதற்கு அதிக நம்பகம் உள்ளது. நான் {self._get_pest_treatment(pest, 'ta')} பயன்படுத்த பரிந்துரைக்கிறேன்.",
                    'bn': f"আমি আপনার ফসলে {pest} সনাক্ষ করেছি যার উচ্চ আত্মবিশ্বাস রয়েছে। আমি {self._get_pest_treatment(pest, 'bn')} প্রয়োগ করার সুপারিশ করছি।"
                }
                return responses.get(language, responses['en'])
            else:
                responses = {
                    'en': f"I think there might be {pest} in your crop, but I'm not completely sure. Could you send a clearer image?",
                    'hi': f"मुझे लगता है कि आपकी फसल में {pest} हो सकता है, लेकिन मैं पूरी तरह से निश्चित नहीं ह। क्या आप एक स्पष्ट छवि भेज सकते हैं?",
                    'pa': f"ਮੈਨੂੰ ਲੱਗਦਾ ਹੈ ਕਿ ਤੁਹਾਡੀ ਫਸਲ ਵਿੱਚ {pest} ਹੋ ਸਕਦਾ ਹੈ, ਪਰ ਮੈਂ ਪੂਰੀ ਤਰ੍ਹਾਂ ਯਕੀਰ ਨਹੀਂ ਹਾਂ। ਕੀ ਤੁਸੀਂ ਇੱਕ ਸਾਫ਼ ਚਿੱਤਰ ਭੇਜ ਸਕਦੇ ਹੋ?",
                    'te': f"నాకు అనుకూలం మీ పంటలో {pest} ఉంటుంది, కానీ నేను ఖచ్చింతగా నిర్ధారించలేదు. మీరు స్పష్టమైన చిత్రాన్ని పంపగలరా?",
                    'ta': f"நான் உங்கள் பயிரில் {pest} இருப்பதாக நினைக்கிறேன், ஆனால் நான் முழுமையாக உறுதியாக இல்லை. நீங்கள் ஒரு தெளிவான படத்தை அனுப்பலாமா?",
                    'bn': f"আমার মনে হয় আপনার ফসলে {pest} হতে পারে, কিন্তু আমি নিশ্চিত নই। আপনি কি একটি পরিষ্কার চিত্র পাঠাতে পারেন?"
                }
                return responses.get(language, responses['en'])
        
        # Check if disease was detected
        elif 'disease' in image_analysis:
            disease = image_analysis['disease']
            confidence = image_analysis.get('confidence', 0)
            
            if confidence > 0.8:
                responses = {
                    'en': f"I've detected {disease} in your crop with high confidence. I recommend applying {self._get_disease_treatment(disease, 'en')}.",
                    'hi': f"मैं आपकी फसल में {disease} का पता लगाया ह। जिसमें उच्च विश्वास ह।। मैं {self._get_disease_treatment(disease, 'hi')} लगाने की सिफारिश करता हूं।",
                    'pa': f"ਮੈਂ ਤੁਹਾਡੀ ਫਸਲ ਵਿੱਚ {disease} ਦੀ ਖੋਜ ਕੀਤੀ ਹੈ ਜਿਸ ਵਿੱਚ ਉੱਚ ਵਿਸ਼ਵਾਸ ਹੈ। ਮੈਂ {self._get_disease_treatment(disease, 'pa')} ਲਾਉਣ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਕਰਦਾ ਹਾਂ।",
                    'te': f"నేను మీ పంటలో {disease} గుర్తించాను, దీనికి అధిక విశ్వాసం ఉంది. నేను {self._get_disease_treatment(disease, 'te')} వర్తింపజేయమని సిఫార్సు చేస్తున్నాను.",
                    'ta': f"நான் உங்கள் பயிரில் {disease} கண்டறினேன், இதற்கு அதிக நம்பகம் உள்ளது. நான் {self._get_disease_treatment(disease, 'ta')} பயன்படுத்த பரிந்துரைக்கிறேன்.",
                    'bn': f"আমি আপনার ফসলে {disease} সনাক্ষ করেছি যার উচ্চ আত্মবিশ্বাস রয়েছে। আমি {self._get_disease_treatment(disease, 'bn')} প্রয়োগ করার সুপারিশ করছি।"
                }
                return responses.get(language, responses['en'])
            else:
                responses = {
                    'en': f"I think there might be {disease} in your crop, but I'm not completely sure. Could you send a clearer image?",
                    'hi': f"मुझे लगता है कि आपकी फसल में {disease} हो सकता है, लेकिन मैं पूरी तरह से निश्चित नहीं ह। क्या आप एक स्पष्ट छवि भेज सकते हैं?",
                    'pa': f"ਮੈਨੂੰ ਲੱਗਦਾ ਹੈ ਕਿ ਤੁਹਾਡੀ ਫਸਲ ਵਿੱਚ {disease} ਹੋ ਸਕਦਾ ਹੈ, ਪਰ ਮੈਂ ਪੂਰੀ ਤਰ੍ਹਾਂ ਯਕੀਰ ਨਹੀਂ ਹਾਂ। ਕੀ ਤੁਸੀਂ ਇੱਕ ਸਾਫ਼ ਚਿੱਤਰ ਭੇਜ ਸਕਦੇ ਹੋ?",
                    'te': f"నాకు అనుకూలం మీ పంటలో {disease} ఉంటుంది, కానీ నేను ఖచ్చింతగా నిర్ధారించలేదు. మీరు స్పష్టమైన చిత్రాన్ని పంపగలరా?",
                    'ta': f"நான் உங்கள் பயிரில் {disease} இருப்பதாக நினைக்கிறேன், ஆனால் நான் முழுமையாக உறுதியாக இல்லை. நீங்கள் ஒரு தெளிவான படத்தை அனுப்பலாமா?",
                    'bn': f"আমার মনে হয় আপনার ফসলে {disease} হতে পারে, কিন্তু আমি নিশ্চিত নই। আপনি কি একটি পরিষ্কার চিত্র পাঠাতে পারেন?"
                }
                return responses.get(language, responses['en'])
        
        # Default response for healthy crop
        responses = {
            'en': "Your crop looks healthy! Keep up the good work. If you have any specific concerns, feel free to ask.",
            'hi': "आपकी फसल स्वस्थ्य दिखती ह। अच्छा कार्य जारी रखें। यदि आपकी कोई विशिष्ट चिंता है, तो बेझिक पूछें।",
            'pa': "ਤੁਹਾਡੀ ਫਸਲ ਸਿਹਤਮੰਦੀ ਲੱਗਦੀ ਹੈ! ਚੰਗੇ ਕੰਮ ਜਾਰੀ ਰੱਖੋ। ਜੇ ਤੁਹਾਡੀ ਕੋਈ ਖਾਸ ਚਿੰਤਾ ਹੈ, ਤਾਂ ਬੇਝਿੱਕ ਪੁੱਛੋ।",
            'te': "మీ పంట ఆరోగ్యంగా కనిపిస్తోంది! మంచి పని కొనసాగి కొనసాగి ఉంది. మీకు ఏవైనా నిర్దిష్ట ఆందోళాలు ఉంటే, దయచేసి అడగండి.",
            'ta': "உங்கள் பயிர் ஆரோக்கியமாகத் தெரிகிறது! நன்றை வேலையைத் தொடரவும். உங்களுக்கு எந்த குறிப்பாடுகள் இருந்தால், தயவு செய்து கேட்கவும்.",
            'bn': "আপনার ফসল স্বাস্থ্য দেখায! ভালো কাজ চালিয়ে যান। আপনার কোনো নির্দিষ্ট উদ্বেগ থাকলে, বিনা দ্বিধায়ে জিজ্ঞাসা করুন।"
        }
        return responses.get(language, responses['en'])

    def _get_fertilizer_recommendation(self, user: User, crop: Optional[str], language: str) -> str:
        # Placeholder for actual fertilizer recommendation logic
        # This would typically involve querying a database or an agronomic service
        if crop:
            return f"For {crop}, a balanced NPK fertilizer is generally recommended. Specific recommendations depend on soil test results."
        return "Please specify the crop for a fertilizer recommendation."

    def _get_pest_treatment(self, pest: str, language: str) -> str:
        # Placeholder for actual pest treatment logic
        # This would typically involve querying a database or an agronomic service
        return f"For {pest}, consider using organic pesticides or consulting a local expert."

    def _get_disease_treatment(self, disease: str, language: str) -> str:
        # Placeholder for actual disease treatment logic
        # This would typically involve querying a database or an agronomic service
        return f"For {disease}, ensure proper sanitation and consider applying a suitable fungicide."