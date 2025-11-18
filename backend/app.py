"""
Flask Backend Application for AI-Powered Shop Scale
Handles image classification, weight estimation, and pricing
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import base64
from io import BytesIO
from PIL import Image

# Import our modules
from model_loader import initialize_classifier, get_classifier
from weight_estimator import initialize_estimator, get_estimator
from database import initialize_database, get_database

# Initialize Flask app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)  # Enable CORS for frontend communication

# Configuration
MODEL_PATH = os.path.join(BASE_DIR, 'fruit_classifier_model.h5')
LABELS_PATH = os.path.join(BASE_DIR, 'model_info.json')
DB_PATH = os.path.join(BASE_DIR, 'data', 'products.db')

# Global state
app_initialized = False


def initialize_app():
    """Initialize all components"""
    global app_initialized

    if app_initialized:
        return True

    print("=" * 60)
    print("Initializing AI-Powered Shop Scale Application...")
    print("=" * 60)

    # Initialize ML model
    print("\n[1/3] Loading ML model...")
    if not initialize_classifier(MODEL_PATH, LABELS_PATH):
        print("ERROR: Failed to load classifier model")
        return False
    print("✓ ML model loaded successfully")

    # Initialize weight estimator
    print("\n[2/3] Initializing weight estimator...")
    if not initialize_estimator():
        print("ERROR: Failed to initialize weight estimator")
        return False
    print("✓ Weight estimator initialized")

    # Initialize database
    print("\n[3/3] Initializing database...")
    if not initialize_database(DB_PATH):
        print("ERROR: Failed to initialize database")
        return False
    print("✓ Database initialized")

    print("\n" + "=" * 60)
    print("Application initialized successfully!")
    print("=" * 60 + "\n")

    app_initialized = True
    return True


@app.route('/')
def serve_frontend():
    """Serve frontend index.html"""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve other static files"""
    if path.startswith('api/'):
        return jsonify({"error": "Not found"}), 404
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "app": "AI-Powered Shop Scale",
        "version": "1.0.0"
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict fruit/vegetable type and estimate weight
    Expects: POST with image data (base64 or multipart file)
    Returns: Classification results, weight estimate, and price
    """
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        initialize_app()

    try:
        # Get image from request
        image_data = None

        if 'image' in request.files:
            # Handle multipart file upload
            file = request.files['image']
            image_data = file.read()
        elif 'image' in request.json:
            # Handle base64 encoded image
            base64_image = request.json['image']
            # Remove data:image/...;base64, prefix if present
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]
            image_data = base64.b64decode(base64_image)
        else:
            return jsonify({"error": "No image provided"}), 400

        # Get classifier and make prediction
        classifier = get_classifier()
        if not classifier:
            return jsonify({"error": "Classifier not initialized"}), 500

        prediction_result = classifier.predict(image_data, top_k=5)

        if "error" in prediction_result:
            return jsonify({"error": prediction_result["error"]}), 500

        # Get top prediction
        top_pred = prediction_result['top_prediction']
        product_name = top_pred['label']
        confidence = top_pred['confidence']

        # Estimate weight
        estimator = get_estimator()
        weight_result = estimator.estimate_weight(product_name)

        # Calculate price
        db = get_database()
        price_result = db.calculate_price(product_name, weight_result['weight_grams'])

        # Combine all results
        response = {
            "success": True,
            "classification": {
                "product": product_name,
                "confidence": round(confidence * 100, 2),
                "alternatives": prediction_result['predictions'][1:] if len(prediction_result['predictions']) > 1 else []
            },
            "weight": weight_result,
            "price": price_result,
            "timestamp": str(os.times())
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/calculate_price', methods=['POST'])
def calculate_price():
    """
    Calculate price for a specific product and weight
    Expects: {"product_name": "...", "weight_grams": ...}
    """
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        initialize_app()

    try:
        data = request.json
        product_name = data.get('product_name')
        weight_grams = data.get('weight_grams')

        if not product_name or weight_grams is None:
            return jsonify({"error": "Missing product_name or weight_grams"}), 400

        db = get_database()
        result = db.calculate_price(product_name, weight_grams)

        if "error" in result:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get list of all available products"""
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        if not initialize_app():
            return jsonify({"error": "Failed to initialize application"}), 500

    try:
        db = get_database()
        if not db or not db.conn:
            return jsonify({"error": "Database not initialized"}), 500

        cursor = db.conn.cursor()
        cursor.execute("SELECT name, name_polish, category, price_per_kg FROM products ORDER BY name")
        rows = cursor.fetchall()

        products = [dict(row) for row in rows]
        return jsonify({"products": products, "count": len(products)})

    except Exception as e:
        print(f"Error in get_products: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/product/<name>', methods=['GET'])
def get_product(name):
    """Get specific product information"""
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        initialize_app()

    try:
        db = get_database()
        product = db.get_product_by_name(name)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(product)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    """
    Record a transaction
    Expects: {"product_name": "...", "weight_g": ..., "price_per_kg": ..., "total_price": ..., "confidence": ...}
    """
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        initialize_app()

    try:
        data = request.json
        product_name = data.get('product_name')
        weight_g = data.get('weight_g')
        price_per_kg = data.get('price_per_kg')
        total_price = data.get('total_price')
        confidence = data.get('confidence')

        if not all([product_name, weight_g, price_per_kg, total_price]):
            return jsonify({"error": "Missing required fields"}), 400

        db = get_database()
        result = db.add_transaction(product_name, weight_g, price_per_kg, total_price, confidence)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get recent transactions"""
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        initialize_app()

    try:
        limit = request.args.get('limit', 10, type=int)
        db = get_database()
        transactions = db.get_recent_transactions(limit)

        return jsonify({"transactions": transactions, "count": len(transactions)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/model_info', methods=['GET'])
def get_model_info():
    """Get ML model information"""
    # Ensure app is initialized (for gunicorn/production)
    if not app_initialized:
        initialize_app()

    try:
        classifier = get_classifier()
        if not classifier:
            return jsonify({"error": "Classifier not initialized"}), 500

        info = classifier.get_model_info()
        return jsonify(info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Initialize application components
    if not initialize_app():
        print("Failed to initialize application. Exiting.")
        exit(1)

    # Run Flask development server
    print("\nStarting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /                    - Health check")
    print("  POST /api/predict         - Classify fruit/vegetable and get price")
    print("  POST /api/calculate_price - Calculate price for product")
    print("  GET  /api/products        - List all products")
    print("  GET  /api/product/<name>  - Get specific product")
    print("  POST /api/transaction     - Record a transaction")
    print("  GET  /api/transactions    - Get recent transactions")
    print("  GET  /api/model_info      - Get model information")
    print("\nPress CTRL+C to stop the server\n")

    app.run(host='0.0.0.0', port=5000, debug=True)
