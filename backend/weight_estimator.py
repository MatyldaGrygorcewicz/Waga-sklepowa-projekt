"""
Weight Estimator Module
Estimates weight of fruits/vegetables based on type and visual features
Uses rule-based approach with average weights per category
"""

import random


class WeightEstimator:
    """Estimates weight of fruits and vegetables"""

    def __init__(self):
        """Initialize weight estimator with average weights (in grams)"""
        # Average weights for different fruit/vegetable categories
        # Format: "fruit_name": (min_weight, typical_weight, max_weight)
        self.weight_database = {
            # Apples (various types)
            "Apple Braeburn": (150, 180, 220),
            "Apple Crimson Snow": (150, 180, 220),
            "Apple Golden 1": (150, 180, 220),
            "Apple Golden 2": (150, 180, 220),
            "Apple Golden 3": (150, 180, 220),
            "Apple Granny Smith": (150, 200, 250),
            "Apple Pink Lady": (140, 170, 200),
            "Apple Red 1": (150, 180, 220),
            "Apple Red 2": (150, 180, 220),
            "Apple Red 3": (150, 180, 220),
            "Apple Red Delicious": (150, 180, 220),
            "Apple Red Yellow 1": (150, 180, 220),
            "Apple Red Yellow 2": (150, 180, 220),

            # Bananas
            "Banana": (120, 150, 180),
            "Banana Lady Finger": (80, 100, 120),
            "Banana Red": (100, 130, 160),

            # Berries
            "Blueberry": (100, 150, 200),  # per container
            "Strawberry": (150, 200, 250),  # per container
            "Strawberry Wedge": (10, 15, 20),  # per piece
            "Raspberry": (100, 150, 200),  # per container

            # Citrus
            "Grapefruit Pink": (200, 300, 450),
            "Grapefruit White": (200, 300, 450),
            "Lemon": (80, 120, 150),
            "Lemon Meyer": (70, 100, 130),
            "Limes": (60, 90, 120),
            "Mandarine": (60, 90, 120),
            "Orange": (120, 180, 250),

            # Stone fruits
            "Apricot": (30, 50, 70),
            "Avocado": (150, 200, 250),
            "Avocado ripe": (150, 200, 250),
            "Cherry 1": (5, 8, 12),  # per piece
            "Cherry 2": (5, 8, 12),  # per piece
            "Cherry Rainier": (5, 8, 12),  # per piece
            "Cherry Wax Black": (5, 8, 12),  # per piece
            "Cherry Wax Red": (5, 8, 12),  # per piece
            "Cherry Wax Yellow": (5, 8, 12),  # per piece
            "Peach": (120, 160, 200),
            "Peach 2": (120, 160, 200),
            "Peach Flat": (100, 140, 180),
            "Plum": (60, 90, 120),
            "Plum 2": (60, 90, 120),
            "Plum 3": (60, 90, 120),
            "Nectarine": (120, 150, 180),
            "Nectarine Flat": (100, 130, 160),

            # Tropical fruits
            "Mango": (200, 350, 500),
            "Mango Red": (200, 350, 500),
            "Papaya": (400, 700, 1000),
            "Passion Fruit": (30, 50, 70),
            "Pineapple": (800, 1200, 1800),
            "Pineapple Mini": (400, 600, 800),
            "Pomegranate": (200, 300, 400),

            # Melons
            "Cantaloupe 1": (800, 1200, 1600),
            "Cantaloupe 2": (800, 1200, 1600),
            "Watermelon": (3000, 5000, 8000),

            # Grapes
            "Grape Blue": (200, 300, 400),  # per bunch
            "Grape Pink": (200, 300, 400),
            "Grape White": (200, 300, 400),
            "Grape White 2": (200, 300, 400),
            "Grape White 3": (200, 300, 400),
            "Grape White 4": (200, 300, 400),

            # Other fruits
            "Guava": (80, 120, 160),
            "Kiwi": (60, 90, 120),
            "Kumquats": (15, 20, 30),
            "Lychee": (15, 20, 25),
            "Pear": (150, 200, 250),
            "Pear 2": (150, 200, 250),
            "Pear Abate": (150, 200, 250),
            "Pear Forelle": (120, 160, 200),
            "Pear Kaiser": (150, 200, 250),
            "Pear Monster": (200, 300, 400),
            "Pear Red": (150, 200, 250),
            "Pear Stone": (150, 200, 250),
            "Pear Williams": (150, 200, 250),
            "Quince": (200, 300, 400),

            # Vegetables - Peppers
            "Pepper Green": (100, 150, 200),
            "Pepper Orange": (100, 150, 200),
            "Pepper Red": (100, 150, 200),
            "Pepper Yellow": (100, 150, 200),

            # Vegetables - Tomatoes
            "Tomato 1": (80, 120, 160),
            "Tomato 2": (80, 120, 160),
            "Tomato 3": (80, 120, 160),
            "Tomato 4": (80, 120, 160),
            "Tomato Cherry Red": (15, 20, 25),
            "Tomato Heart": (150, 200, 250),
            "Tomato Maroon": (80, 120, 160),
            "Tomato not Ripened": (80, 120, 160),
            "Tomato Yellow": (80, 120, 160),

            # Other vegetables
            "Cactus fruit": (80, 120, 160),
            "Carambula": (80, 120, 160),
            "Cauliflower": (500, 800, 1200),
            "Cocos": (300, 500, 800),
            "Corn": (200, 300, 400),
            "Corn Husk": (200, 300, 400),
            "Cucumber Ripe": (200, 350, 500),
            "Cucumber Ripe 2": (200, 350, 500),
            "Dates": (5, 8, 12),  # per piece
            "Eggplant": (200, 400, 600),
            "Ginger Root": (50, 100, 150),
            "Granadilla": (40, 60, 80),
            "Kohlrabi": (200, 350, 500),
            "Onion Red": (100, 150, 200),
            "Onion Red Peeled": (100, 150, 200),
            "Onion White": (100, 150, 200),
            "Potato Red": (100, 150, 200),
            "Potato Red Washed": (100, 150, 200),
            "Potato Sweet": (150, 250, 350),
            "Potato White": (100, 150, 200),
            "Redded Radish": (30, 50, 70),
            "Salak": (40, 60, 80),
            "Tamarillo": (50, 80, 110),
            "Tangelo": (100, 150, 200),
            "Walnut": (10, 15, 20),  # per piece
            "Walnut Peeled": (5, 8, 12),  # per piece

            # Nuts
            "Chestnut": (10, 15, 20),
            "Hazelnut": (3, 5, 8),
            "Hazelnut Peeled": (2, 3, 5),
            "Nut Forest": (5, 8, 12),
            "Nut Pecan": (8, 12, 16),
        }

    def estimate_weight(self, fruit_name, variation_factor=0.15):
        """
        Estimate weight for a given fruit/vegetable

        Args:
            fruit_name: Name of the fruit/vegetable
            variation_factor: Random variation factor (default 15%)

        Returns:
            Dictionary with estimated weight in grams
        """
        try:
            # Get weight range from database
            if fruit_name not in self.weight_database:
                # If not found, return a generic estimate
                return {
                    "weight_grams": 150,
                    "weight_kg": 0.15,
                    "confidence": "low",
                    "note": f"No specific data for {fruit_name}, using generic estimate"
                }

            min_weight, typical_weight, max_weight = self.weight_database[fruit_name]

            # Add some random variation around typical weight (more realistic)
            variation = random.uniform(-variation_factor, variation_factor)
            estimated_weight = typical_weight * (1 + variation)

            # Clamp to min/max range
            estimated_weight = max(min_weight, min(estimated_weight, max_weight))

            return {
                "weight_grams": round(estimated_weight, 1),
                "weight_kg": round(estimated_weight / 1000, 3),
                "min_weight": min_weight,
                "max_weight": max_weight,
                "typical_weight": typical_weight,
                "confidence": "medium",
                "note": f"Estimated based on typical {fruit_name} weight"
            }

        except Exception as e:
            return {
                "error": str(e),
                "weight_grams": 150,
                "weight_kg": 0.15,
                "confidence": "low"
            }

    def get_weight_range(self, fruit_name):
        """Get the weight range for a fruit/vegetable"""
        if fruit_name in self.weight_database:
            min_w, typ_w, max_w = self.weight_database[fruit_name]
            return {
                "min_grams": min_w,
                "typical_grams": typ_w,
                "max_grams": max_w,
                "min_kg": round(min_w / 1000, 3),
                "typical_kg": round(typ_w / 1000, 3),
                "max_kg": round(max_w / 1000, 3)
            }
        return None


# Global estimator instance
estimator = None


def initialize_estimator():
    """Initialize the global weight estimator"""
    global estimator
    estimator = WeightEstimator()
    return True


def get_estimator():
    """Get the global weight estimator instance"""
    return estimator
