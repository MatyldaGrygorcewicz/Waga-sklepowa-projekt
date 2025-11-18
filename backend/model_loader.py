"""
Model Loader Module
Handles loading and using the fruit/vegetable classification model
"""

import json
import numpy as np
from tensorflow import keras
from PIL import Image
import io
import os


class FruitClassifier:
    """Wrapper class for fruit/vegetable classification model"""

    def __init__(self, model_path, labels_path):
        """
        Initialize the classifier

        Args:
            model_path: Path to the .h5 model file
            labels_path: Path to the model_info.json file
        """
        self.model_path = model_path
        self.labels_path = labels_path
        self.model = None
        self.labels = None
        self.model_info = None

    def load_model(self):
        """Load the Keras model and label information"""
        try:
            # Load the trained model
            print(f"Loading model from {self.model_path}...")
            self.model = keras.models.load_model(self.model_path)
            print("Model loaded successfully!")

            # Load the labels and model info
            print(f"Loading labels from {self.labels_path}...")
            with open(self.labels_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.labels = data['labels']
                self.model_info = data
            print(f"Loaded {len(self.labels)} fruit/vegetable categories")

            return True

        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False

    def preprocess_image(self, image_data):
        """
        Preprocess image for model input

        Args:
            image_data: Raw image data (bytes or PIL Image)

        Returns:
            Preprocessed numpy array ready for model
        """
        try:
            # Convert bytes to PIL Image if needed
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data

            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize to model input size (32x32)
            image = image.resize((32, 32))

            # Convert to numpy array
            img_array = np.array(image)

            # Normalize pixel values to [0, 1]
            img_array = img_array.astype('float32') / 255.0

            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)

            return img_array

        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return None

    def predict(self, image_data, top_k=3):
        """
        Predict fruit/vegetable type from image

        Args:
            image_data: Raw image data (bytes or PIL Image)
            top_k: Number of top predictions to return

        Returns:
            Dictionary with prediction results
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_data)
            if processed_image is None:
                return {"error": "Failed to preprocess image"}

            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)

            # Get top K predictions
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]
            top_probs = predictions[0][top_indices]

            # Format results
            results = []
            for idx, prob in zip(top_indices, top_probs):
                results.append({
                    "label": self.labels[idx],
                    "confidence": float(prob),
                    "class_id": int(idx)
                })

            return {
                "success": True,
                "predictions": results,
                "top_prediction": results[0] if results else None
            }

        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return {"error": str(e)}

    def get_model_info(self):
        """Return model information"""
        return self.model_info if self.model_info else {}


# Global classifier instance
classifier = None


def initialize_classifier(model_path, labels_path):
    """Initialize the global classifier instance"""
    global classifier
    classifier = FruitClassifier(model_path, labels_path)
    return classifier.load_model()


def get_classifier():
    """Get the global classifier instance"""
    return classifier
