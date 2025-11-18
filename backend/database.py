"""
Database Module
Manages product information, prices, and transactions using SQLite
"""

import sqlite3
import json
import os
from datetime import datetime


class ProductDatabase:
    """Handles product database operations"""

    def __init__(self, db_path):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            return True
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            return False

    def initialize_schema(self):
        """Create database tables if they don't exist"""
        try:
            cursor = self.conn.cursor()

            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    name_polish TEXT NOT NULL,
                    category TEXT,
                    price_per_kg REAL NOT NULL,
                    price_per_unit REAL,
                    sell_by_weight BOOLEAN DEFAULT 1,
                    typical_weight_g INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    weight_g REAL NOT NULL,
                    price_per_kg REAL NOT NULL,
                    total_price REAL NOT NULL,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.conn.commit()
            print("Database schema initialized successfully")
            return True

        except Exception as e:
            print(f"Error initializing schema: {str(e)}")
            return False

    def populate_default_products(self):
        """Populate database with default fruit/vegetable products and prices (in PLN)"""
        # Polish names and realistic prices per kg in PLN
        products = [
            # Apples (Jabłka) - 4-8 PLN/kg
            ("Apple Braeburn", "Jabłko Braeburn", "Owoce", 7.50),
            ("Apple Crimson Snow", "Jabłko Crimson Snow", "Owoce", 8.00),
            ("Apple Golden 1", "Jabłko Golden", "Owoce", 5.50),
            ("Apple Golden 2", "Jabłko Golden", "Owoce", 5.50),
            ("Apple Golden 3", "Jabłko Golden", "Owoce", 5.50),
            ("Apple Granny Smith", "Jabłko Granny Smith", "Owoce", 7.00),
            ("Apple Pink Lady", "Jabłko Pink Lady", "Owoce", 9.00),
            ("Apple Red 1", "Jabłko czerwone", "Owoce", 6.00),
            ("Apple Red 2", "Jabłko czerwone", "Owoce", 6.00),
            ("Apple Red 3", "Jabłko czerwone", "Owoce", 6.00),
            ("Apple Red Delicious", "Jabłko Red Delicious", "Owoce", 7.50),
            ("Apple Red Yellow 1", "Jabłko czerwono-żółte", "Owoce", 6.50),
            ("Apple Red Yellow 2", "Jabłko czerwono-żółte", "Owoce", 6.50),

            # Bananas (Banany) - 5-7 PLN/kg
            ("Banana", "Banan", "Owoce", 5.50),
            ("Banana Lady Finger", "Banan Lady Finger", "Owoce", 8.00),
            ("Banana Red", "Banan czerwony", "Owoce", 12.00),

            # Berries (Jagody) - 15-35 PLN/kg
            ("Blueberry", "Borówka", "Owoce", 28.00),
            ("Strawberry", "Truskawka", "Owoce", 18.00),
            ("Strawberry Wedge", "Truskawka (kawałek)", "Owoce", 18.00),
            ("Raspberry", "Malina", "Owoce", 32.00),

            # Citrus (Cytrusy) - 5-10 PLN/kg
            ("Grapefruit Pink", "Grejpfrut różowy", "Owoce", 8.00),
            ("Grapefruit White", "Grejpfrut biały", "Owoce", 7.50),
            ("Lemon", "Cytryna", "Owoce", 8.50),
            ("Lemon Meyer", "Cytryna Meyer", "Owoce", 12.00),
            ("Limes", "Limonka", "Owoce", 15.00),
            ("Mandarine", "Mandarynka", "Owoce", 7.00),
            ("Orange", "Pomarańcza", "Owoce", 6.00),

            # Stone fruits (Owoce pestkowe) - 8-15 PLN/kg
            ("Apricot", "Morela", "Owoce", 12.00),
            ("Avocado", "Awokado", "Owoce", 18.00),
            ("Avocado ripe", "Awokado dojrzałe", "Owoce", 18.00),
            ("Cherry 1", "Czereśnia", "Owoce", 25.00),
            ("Cherry 2", "Czereśnia", "Owoce", 25.00),
            ("Cherry Rainier", "Czereśnia Rainier", "Owoce", 35.00),
            ("Cherry Wax Black", "Czereśnia czarna", "Owoce", 28.00),
            ("Cherry Wax Red", "Czereśnia czerwona", "Owoce", 25.00),
            ("Cherry Wax Yellow", "Czereśnia żółta", "Owoce", 30.00),
            ("Peach", "Brzoskwinia", "Owoce", 10.00),
            ("Peach 2", "Brzoskwinia", "Owoce", 10.00),
            ("Peach Flat", "Brzoskwinia płaska", "Owoce", 12.00),
            ("Plum", "Śliwka", "Owoce", 8.00),
            ("Plum 2", "Śliwka", "Owoce", 8.00),
            ("Plum 3", "Śliwka", "Owoce", 8.00),
            ("Nectarine", "Nektarynka", "Owoce", 11.00),
            ("Nectarine Flat", "Nektarynka płaska", "Owoce", 13.00),

            # Tropical fruits (Owoce tropikalne) - 10-25 PLN/kg
            ("Mango", "Mango", "Owoce", 16.00),
            ("Mango Red", "Mango czerwone", "Owoce", 18.00),
            ("Papaya", "Papaja", "Owoce", 20.00),
            ("Passion Fruit", "Marakuja", "Owoce", 45.00),
            ("Pineapple", "Ananas", "Owoce", 8.00),
            ("Pineapple Mini", "Ananas mini", "Owoce", 12.00),
            ("Pomegranate", "Granat", "Owoce", 15.00),

            # Melons (Melony) - 3-6 PLN/kg
            ("Cantaloupe 1", "Melon Kantalupa", "Owoce", 5.50),
            ("Cantaloupe 2", "Melon Kantalupa", "Owoce", 5.50),
            ("Watermelon", "Arbuz", "Owoce", 3.50),

            # Grapes (Winogrona) - 8-15 PLN/kg
            ("Grape Blue", "Winogrona niebieskie", "Owoce", 12.00),
            ("Grape Pink", "Winogrona różowe", "Owoce", 14.00),
            ("Grape White", "Winogrona białe", "Owoce", 10.00),
            ("Grape White 2", "Winogrona białe", "Owoce", 10.00),
            ("Grape White 3", "Winogrona białe", "Owoce", 10.00),
            ("Grape White 4", "Winogrona białe", "Owoce", 10.00),

            # Other fruits (Inne owoce) - 6-12 PLN/kg
            ("Guava", "Guawa", "Owoce", 22.00),
            ("Kiwi", "Kiwi", "Owoce", 10.00),
            ("Kumquats", "Kumkwat", "Owoce", 35.00),
            ("Lychee", "Liczi", "Owoce", 40.00),
            ("Pear", "Gruszka", "Owoce", 7.00),
            ("Pear 2", "Gruszka", "Owoce", 7.00),
            ("Pear Abate", "Gruszka Abate", "Owoce", 8.50),
            ("Pear Forelle", "Gruszka Forelle", "Owoce", 9.00),
            ("Pear Kaiser", "Gruszka Kaiser", "Owoce", 8.00),
            ("Pear Monster", "Gruszka Monster", "Owoce", 10.00),
            ("Pear Red", "Gruszka czerwona", "Owoce", 9.50),
            ("Pear Stone", "Gruszka Stone", "Owoce", 7.50),
            ("Pear Williams", "Gruszka Williams", "Owoce", 8.50),
            ("Quince", "Pigwa", "Owoce", 6.00),

            # Vegetables - Peppers (Papryka) - 8-15 PLN/kg
            ("Pepper Green", "Papryka zielona", "Warzywa", 9.00),
            ("Pepper Orange", "Papryka pomarańczowa", "Warzywa", 12.00),
            ("Pepper Red", "Papryka czerwona", "Warzywa", 12.00),
            ("Pepper Yellow", "Papryka żółta", "Warzywa", 12.00),

            # Vegetables - Tomatoes (Pomidory) - 6-12 PLN/kg
            ("Tomato 1", "Pomidor", "Warzywa", 8.00),
            ("Tomato 2", "Pomidor", "Warzywa", 8.00),
            ("Tomato 3", "Pomidor", "Warzywa", 8.00),
            ("Tomato 4", "Pomidor", "Warzywa", 8.00),
            ("Tomato Cherry Red", "Pomidor koktajlowy", "Warzywa", 15.00),
            ("Tomato Heart", "Pomidor malinowy", "Warzywa", 14.00),
            ("Tomato Maroon", "Pomidor bordowy", "Warzywa", 10.00),
            ("Tomato not Ripened", "Pomidor niedojrzały", "Warzywa", 7.00),
            ("Tomato Yellow", "Pomidor żółty", "Warzywa", 12.00),

            # Other vegetables (Inne warzywa) - 3-10 PLN/kg
            ("Cactus fruit", "Owoc kaktusa", "Owoce", 25.00),
            ("Carambula", "Karambola", "Owoce", 30.00),
            ("Cauliflower", "Kalafior", "Warzywa", 6.00),
            ("Cocos", "Kokos", "Owoce", 8.00),
            ("Corn", "Kukurydza", "Warzywa", 4.50),
            ("Corn Husk", "Kukurydza w liściach", "Warzywa", 4.50),
            ("Cucumber Ripe", "Ogórek", "Warzywa", 5.50),
            ("Cucumber Ripe 2", "Ogórek", "Warzywa", 5.50),
            ("Dates", "Daktyl", "Owoce", 35.00),
            ("Eggplant", "Bakłażan", "Warzywa", 8.00),
            ("Ginger Root", "Imbir", "Warzywa", 18.00),
            ("Granadilla", "Granadilla", "Owoce", 40.00),
            ("Kohlrabi", "Kalarepa", "Warzywa", 4.50),
            ("Onion Red", "Cebula czerwona", "Warzywa", 4.00),
            ("Onion Red Peeled", "Cebula czerwona obrana", "Warzywa", 5.00),
            ("Onion White", "Cebula biała", "Warzywa", 3.50),
            ("Potato Red", "Ziemniak czerwony", "Warzywa", 2.50),
            ("Potato Red Washed", "Ziemniak czerwony myty", "Warzywa", 3.00),
            ("Potato Sweet", "Batat", "Warzywa", 7.00),
            ("Potato White", "Ziemniak biały", "Warzywa", 2.00),
            ("Redded Radish", "Rzodkiewka", "Warzywa", 6.00),
            ("Salak", "Salak", "Owoce", 35.00),
            ("Tamarillo", "Tamarillo", "Owoce", 30.00),
            ("Tangelo", "Tangelo", "Owoce", 10.00),
            ("Walnut", "Orzech włoski", "Owoce", 40.00),
            ("Walnut Peeled", "Orzech włoski obrany", "Owoce", 60.00),

            # Nuts (Orzechy) - 30-70 PLN/kg
            ("Chestnut", "Kasztan", "Owoce", 25.00),
            ("Hazelnut", "Orzech laskowy", "Owoce", 45.00),
            ("Hazelnut Peeled", "Orzech laskowy obrany", "Owoce", 65.00),
            ("Nut Forest", "Orzech leśny", "Owoce", 50.00),
            ("Nut Pecan", "Orzech pekan", "Owoce", 70.00),
        ]

        try:
            cursor = self.conn.cursor()

            # Check if products already exist
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"Database already contains {count} products")
                return True

            # Insert products
            for name, name_polish, category, price_per_kg in products:
                try:
                    cursor.execute('''
                        INSERT INTO products (name, name_polish, category, price_per_kg, sell_by_weight)
                        VALUES (?, ?, ?, ?, 1)
                    ''', (name, name_polish, category, price_per_kg))
                except sqlite3.IntegrityError:
                    # Product already exists, skip
                    pass

            self.conn.commit()
            print(f"Added {len(products)} products to database")
            return True

        except Exception as e:
            print(f"Error populating products: {str(e)}")
            return False

    def get_product_by_name(self, name):
        """Get product information by name"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

        except Exception as e:
            print(f"Error getting product: {str(e)}")
            return None

    def calculate_price(self, product_name, weight_grams):
        """Calculate price for a product based on weight"""
        try:
            product = self.get_product_by_name(product_name)

            if not product:
                return {"error": f"Product {product_name} not found"}

            weight_kg = weight_grams / 1000
            total_price = weight_kg * product['price_per_kg']

            return {
                "product_name": product['name'],
                "product_name_polish": product['name_polish'],
                "weight_grams": weight_grams,
                "weight_kg": round(weight_kg, 3),
                "price_per_kg": product['price_per_kg'],
                "total_price": round(total_price, 2),
                "currency": "PLN"
            }

        except Exception as e:
            return {"error": str(e)}

    def add_transaction(self, product_name, weight_g, price_per_kg, total_price, confidence=None):
        """Add a transaction to the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (product_name, weight_g, price_per_kg, total_price, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (product_name, weight_g, price_per_kg, total_price, confidence))

            self.conn.commit()
            return {"success": True, "transaction_id": cursor.lastrowid}

        except Exception as e:
            print(f"Error adding transaction: {str(e)}")
            return {"error": str(e)}

    def get_recent_transactions(self, limit=10):
        """Get recent transactions"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM transactions
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error getting transactions: {str(e)}")
            return []


# Global database instance
db = None


def initialize_database(db_path):
    """Initialize the global database instance"""
    global db
    db = ProductDatabase(db_path)

    if not db.connect():
        return False

    if not db.initialize_schema():
        return False

    if not db.populate_default_products():
        return False

    return True


def get_database():
    """Get the global database instance"""
    return db
