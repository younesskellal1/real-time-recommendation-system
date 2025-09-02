from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    description: str
    rating: float = 0.0
    tags: List[str] = None
    image_url: str = ''
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'rating': self.rating,
            'tags': self.tags,
            'image_url': self.image_url
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

# Sample products database
PRODUCTS_DB = [
    Product(1, "iPhone 15", "Electronics", 999.99, "Latest Apple smartphone", 4.5, ["smartphone", "apple", "mobile"], "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=facearea&w=400&h=400"),
    Product(2, "Samsung Galaxy S24", "Electronics", 899.99, "Android flagship phone", 4.3, ["smartphone", "samsung", "android"], "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=facearea&w=400&h=400"),
    Product(3, "MacBook Pro", "Electronics", 1999.99, "Professional laptop", 4.7, ["laptop", "apple", "computer"], "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=facearea&w=400&h=400"),
    Product(4, "Dell XPS 13", "Electronics", 1299.99, "Ultrabook laptop", 4.4, ["laptop", "dell", "computer"], "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=facearea&w=400&h=400"),
    Product(5, "Nike Air Max", "Fashion", 120.99, "Running shoes", 4.2, ["shoes", "nike", "running"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(6, "Adidas Ultraboost", "Fashion", 180.99, "Premium running shoes", 4.6, ["shoes", "adidas", "running"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(7, "Levi's Jeans", "Fashion", 79.99, "Classic denim jeans", 4.1, ["jeans", "levi", "denim"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(8, "The Great Gatsby", "Books", 12.99, "Classic American novel", 4.0, ["book", "fiction", "classic"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(9, "1984", "Books", 13.99, "Dystopian novel", 4.8, ["book", "fiction", "dystopian"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(10, "Coffee Maker", "Home", 89.99, "Automatic coffee machine", 4.3, ["coffee", "kitchen", "appliance"], "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=facearea&w=400&h=400"),
    Product(11, "Sony WH-1000XM5", "Electronics", 349.99, "Noise-cancelling headphones", 4.8, ["headphones", "sony", "audio"], "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=facearea&w=400&h=400"),
    Product(12, "Apple Watch Series 9", "Electronics", 399.99, "Smartwatch with health tracking", 4.5, ["watch", "apple", "wearable"], "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=facearea&w=400&h=400"),
    Product(13, "Instant Pot Duo", "Home", 99.99, "Multi-use pressure cooker", 4.7, ["kitchen", "cooker", "appliance"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(14, "Dyson V11 Vacuum", "Home", 599.99, "Cordless stick vacuum cleaner", 4.6, ["vacuum", "dyson", "cleaning"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(15, "Harry Potter Box Set", "Books", 59.99, "Complete Harry Potter series", 4.9, ["book", "fantasy", "series"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(16, "The Lean Startup", "Books", 19.99, "Entrepreneurship guide", 4.3, ["book", "business", "startup"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(17, "Ray-Ban Wayfarer", "Fashion", 129.99, "Classic sunglasses", 4.4, ["sunglasses", "rayban", "accessory"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(18, "North Face Jacket", "Fashion", 199.99, "Waterproof outdoor jacket", 4.5, ["jacket", "northface", "outdoor"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(19, "Wilson Tennis Racket", "Sports", 149.99, "Professional tennis racket", 4.6, ["tennis", "racket", "wilson"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(20, "Yoga Mat Pro", "Sports", 39.99, "Non-slip yoga mat", 4.2, ["yoga", "mat", "fitness"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(21, "GoPro HERO11", "Electronics", 429.99, "Action camera for adventure", 4.7, ["camera", "gopro", "action"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(22, "Kindle Paperwhite", "Electronics", 129.99, "E-reader with high-res display", 4.6, ["ereader", "kindle", "amazon"], "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=facearea&w=400&h=400"),
    Product(23, "Philips Hue Starter Kit", "Home", 179.99, "Smart lighting system", 4.5, ["lighting", "philips", "smart home"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(24, "Bose SoundLink Mini", "Electronics", 99.99, "Portable Bluetooth speaker", 4.4, ["speaker", "bose", "audio"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(25, "Fitbit Charge 5", "Electronics", 149.99, "Fitness tracker with GPS", 4.3, ["fitness", "fitbit", "wearable"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(26, "Lego Star Wars X-Wing", "Toys", 49.99, "Star Wars themed Lego set", 4.8, ["lego", "star wars", "toy"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(27, "Barbie Dreamhouse", "Toys", 199.99, "Barbie's luxury dollhouse", 4.7, ["barbie", "dollhouse", "toy"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(28, "Maybelline Mascara", "Beauty", 9.99, "Volumizing mascara", 4.2, ["mascara", "maybelline", "beauty"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(29, "Oral-B Electric Toothbrush", "Health", 59.99, "Rechargeable toothbrush", 4.5, ["toothbrush", "oralb", "health"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(30, "Samsonite Suitcase", "Travel", 139.99, "Durable travel suitcase", 4.6, ["suitcase", "samsonite", "travel"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(31, "Canon EOS Rebel T7", "Electronics", 449.99, "Entry-level DSLR camera", 4.4, ["camera", "canon", "photography"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(32, "Monopoly Classic", "Toys", 24.99, "Classic board game", 4.3, ["game", "monopoly", "boardgame"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(33, "Cuisinart Air Fryer", "Home", 129.99, "Countertop air fryer oven", 4.5, ["air fryer", "cuisinart", "kitchen"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(34, "Patagonia Backpack", "Fashion", 89.99, "Durable outdoor backpack", 4.6, ["backpack", "patagonia", "outdoor"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(35, "FIFA 24", "Games", 69.99, "Latest football video game", 4.7, ["fifa", "video game", "football"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(36, "Google Pixel 8", "Electronics", 799.99, "Google's latest smartphone with advanced AI features", 4.4, ["smartphone", "google", "android"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(37, "Uniqlo Ultra Light Down Jacket", "Fashion", 69.99, "Lightweight and warm down jacket", 4.5, ["jacket", "uniqlo", "fashion"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(38, "Atomic Habits", "Books", 16.99, "Bestselling self-improvement book by James Clear", 4.8, ["book", "self-help", "habits"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(39, "iRobot Roomba 692", "Home", 249.99, "Robot vacuum cleaner with Wi-Fi connectivity", 4.3, ["vacuum", "irobot", "cleaning"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(40, "Wilson NBA Basketball", "Sports", 29.99, "Official size and weight basketball", 4.6, ["basketball", "wilson", "sports"], "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?auto=format&fit=facearea&w=400&h=400"),
    Product(41, "L'Oreal Paris Serum", "Beauty", 24.99, "Revitalift 1.5% Pure Hyaluronic Acid Serum", 4.7, ["serum", "loreal", "beauty"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(42, "Omron Blood Pressure Monitor", "Health", 49.99, "Automatic digital blood pressure monitor", 4.5, ["health", "omron", "monitor"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(43, "Samsonite Travel Pillow", "Travel", 19.99, "Memory foam neck pillow for travel comfort", 4.2, ["pillow", "samsonite", "travel"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(44, "Hot Wheels Mega Garage", "Toys", 59.99, "Multi-level car garage playset", 4.4, ["hot wheels", "garage", "toy"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(45, "Catan Board Game", "Games", 44.99, "Popular strategy board game for all ages", 4.8, ["catan", "board game", "strategy"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(46, "Purina Cat Chow", "Pet Supplies", 14.99, "Nutritious dry food for adult cats", 4.6, ["cat food", "purina", "pet"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(47, "Ergonomic Office Chair", "Office", 229.99, "Adjustable mesh chair for all-day comfort", 4.5, ["chair", "office", "ergonomic"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(48, "Fiskars Garden Pruner", "Garden", 19.99, "Precision garden pruner for plants and flowers", 4.7, ["pruner", "fiskars", "garden"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(49, "Michelin All-Season Tire", "Automotive", 129.99, "Durable all-season tire for cars", 4.4, ["tire", "michelin", "car"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(50, "Graco Pack 'n Play", "Baby", 89.99, "Portable playard for babies and toddlers", 4.8, ["playard", "graco", "baby"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(51, "Yamaha Acoustic Guitar", "Music", 199.99, "Beginner-friendly acoustic guitar", 4.6, ["guitar", "yamaha", "music"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(52, "Winsor & Newton Watercolors", "Art", 29.99, "Professional watercolor paint set", 4.7, ["watercolor", "paint", "art"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(53, "Ghirardelli Chocolate Squares", "Food", 8.99, "Assorted premium chocolate squares", 4.9, ["chocolate", "ghirardelli", "food"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(54, "Starbucks Pike Place Roast", "Beverage", 12.99, "Medium roast ground coffee", 4.5, ["coffee", "starbucks", "beverage"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(55, "Lysol Disinfecting Wipes", "Cleaning", 5.99, "Antibacterial wipes for surfaces", 4.8, ["wipes", "lysol", "cleaning"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(56, "TRX Suspension Trainer", "Fitness", 129.99, "All-in-one bodyweight training system", 4.7, ["trx", "fitness", "trainer"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(57, "Coleman Camping Tent", "Outdoors", 99.99, "4-person dome tent for camping", 4.6, ["tent", "coleman", "outdoors"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(58, "Swarovski Crystal Necklace", "Jewelry", 79.99, "Elegant crystal pendant necklace", 4.8, ["necklace", "swarovski", "jewelry"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(59, "Cricut Explore Air 2", "Crafts", 199.99, "DIY cutting machine for crafts", 4.7, ["cricut", "crafts", "machine"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(60, "Moleskine Classic Notebook", "Stationery", 19.99, "Hardcover ruled notebook", 4.6, ["notebook", "moleskine", "stationery"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(61, "Nike Revolution 6", "Footwear", 59.99, "Lightweight running shoes", 4.5, ["shoes", "nike", "footwear"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(62, "Philips Hue Smart Plug", "Smart Home", 29.99, "Control devices with your voice or app", 4.4, ["smart plug", "philips", "home"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(63, "Black+Decker Cordless Drill", "Tools", 49.99, "20V cordless drill for home projects", 4.6, ["drill", "black+decker", "tools"], "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=400&h=400"),
    Product(64, "Inception Blu-ray", "Movies", 14.99, "Christopher Nolan's mind-bending thriller", 4.9, ["movie", "inception", "blu-ray"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
    Product(65, "Khan Academy SAT Prep Book", "Education", 24.99, "Comprehensive SAT study guide", 4.8, ["sat", "khan academy", "education"], "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=facearea&w=400&h=400"),
]