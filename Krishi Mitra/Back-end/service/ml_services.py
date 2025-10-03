import numpy as np
import tensorflow as tf
from PIL import Image
from typing import Dict, Any, List, Tuple
import os

class MLService:
    def __init__(self):
        # Load models
        self.pest_model = self._load_pest_model()
        self.disease_model = self._load_disease_model()
        
        # Class labels
        self.pest_classes = ['aphid', 'blight', 'rust', 'fungus', 'bollworm', 'healthy']
        self.disease_classes = ['blast', 'bacterial_leaf_blight', 'sheath_blight', 'rust', 'healthy']
    
    def _load_pest_model(self):
        """Load pest detection model"""
        # In a real implementation, this would load a trained model
        # For demo, we'll use a placeholder
        model_path = os.path.join('ml_models', 'pest_detection.h5')
        if os.path.exists(model_path):
            return tf.keras.models.load_model(model_path)
        else:
            # Return a dummy model for demo
            return self._create_dummy_model(len(self.pest_classes))
    
    def _load_disease_model(self):
        """Load disease detection model"""
        # In a real implementation, this would load a trained model
        # For demo, we'll use a placeholder
        model_path = os.path.join('ml_models', 'disease_detection.h5')
        if os.path.exists(model_path):
            return tf.keras.models.load_model(model_path)
        else:
            # Return a dummy model for demo
            return self._create_dummy_model(len(self.disease_classes))
    
    def _create_dummy_model(self, num_classes: int):
        """Create a dummy model for demo purposes"""
        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(224, 224, 3)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        return model
    
    def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze image for pests and diseases"""
        # Preprocess image
        processed_image = self._preprocess_image(image)
        
        # Predict pests
        pest_predictions = self.pest_model.predict(processed_image)
        pest_class = self.pest_classes[np.argmax(pest_predictions[0])]
        pest_confidence = float(np.max(pest_predictions[0]))
        
        # Predict diseases
        disease_predictions = self.disease_model.predict(processed_image)
        disease_class = self.disease_classes[np.argmax(disease_predictions[0])]
        disease_confidence = float(np.max(disease_predictions[0]))
        
        # Determine primary issue
        if pest_confidence > disease_confidence and pest_class != 'healthy':
            return {
                'type': 'pest',
                'pest': pest_class.replace('_', ' ').title(),
                'confidence': pest_confidence
            }
        elif disease_confidence > 0.5 and disease_class != 'healthy':
            return {
                'type': 'disease',
                'disease': disease_class.replace('_', ' ').title(),
                'confidence': disease_confidence
            }
        else:
            return {
                'type': 'healthy',
                'message': 'No pests or diseases detected',
                'confidence': max(pest_confidence, disease_confidence)
            }
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for model input"""
        # Resize image to model input size
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array