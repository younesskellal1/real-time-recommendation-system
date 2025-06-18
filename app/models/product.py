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
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

# Sample products database
PRODUCTS_DB = [
    Product(1, "iPhone 15", "Electronics", 999.99, "Latest Apple smartphone", 4.5, ["smartphone", "apple", "mobile"]),
    Product(2, "Samsung Galaxy S24", "Electronics", 899.99, "Android flagship phone", 4.3, ["smartphone", "samsung", "android"]),
    Product(3, "MacBook Pro", "Electronics", 1999.99, "Professional laptop", 4.7, ["laptop", "apple", "computer"]),
    Product(4, "Dell XPS 13", "Electronics", 1299.99, "Ultrabook laptop", 4.4, ["laptop", "dell", "computer"]),
    Product(5, "Nike Air Max", "Fashion", 120.99, "Running shoes", 4.2, ["shoes", "nike", "running"]),
    Product(6, "Adidas Ultraboost", "Fashion", 180.99, "Premium running shoes", 4.6, ["shoes", "adidas", "running"]),
    Product(7, "Levi's Jeans", "Fashion", 79.99, "Classic denim jeans", 4.1, ["jeans", "levi", "denim"]),
    Product(8, "The Great Gatsby", "Books", 12.99, "Classic American novel", 4.0, ["book", "fiction", "classic"]),
    Product(9, "1984", "Books", 13.99, "Dystopian novel", 4.8, ["book", "fiction", "dystopian"]),
    Product(10, "Coffee Maker", "Home", 89.99, "Automatic coffee machine", 4.3, ["coffee", "kitchen", "appliance"]),    
    Product(11, "Sony WH-1000XM5", "Electronics", 349.99, "Noise-cancelling headphones", 4.8, ["headphones", "sony", "audio"]),
    Product(12, "Apple Watch Series 9", "Electronics", 399.99, "Smartwatch with health tracking", 4.5, ["watch", "apple", "wearable"]),
    Product(13, "Instant Pot Duo", "Home", 99.99, "Multi-use pressure cooker", 4.7, ["kitchen", "cooker", "appliance"]),
    Product(14, "Dyson V11 Vacuum", "Home", 599.99, "Cordless stick vacuum cleaner", 4.6, ["vacuum", "dyson", "cleaning"]),
    Product(15, "Harry Potter Box Set", "Books", 59.99, "Complete Harry Potter series", 4.9, ["book", "fantasy", "series"]),
    Product(16, "The Lean Startup", "Books", 19.99, "Entrepreneurship guide", 4.3, ["book", "business", "startup"]),
    Product(17, "Ray-Ban Wayfarer", "Fashion", 129.99, "Classic sunglasses", 4.4, ["sunglasses", "rayban", "accessory"]),
    Product(18, "North Face Jacket", "Fashion", 199.99, "Waterproof outdoor jacket", 4.5, ["jacket", "northface", "outdoor"]),
    Product(19, "Wilson Tennis Racket", "Sports", 149.99, "Professional tennis racket", 4.6, ["tennis", "racket", "wilson"]),
    Product(20, "Yoga Mat Pro", "Sports", 39.99, "Non-slip yoga mat", 4.2, ["yoga", "mat", "fitness"]),
    Product(21, "GoPro HERO11", "Electronics", 429.99, "Action camera for adventure", 4.7, ["camera", "gopro", "action"]),
    Product(22, "Kindle Paperwhite", "Electronics", 129.99, "E-reader with high-res display", 4.6, ["ereader", "kindle", "amazon"]),
    Product(23, "Philips Hue Starter Kit", "Home", 179.99, "Smart lighting system", 4.5, ["lighting", "philips", "smart home"]),
    Product(24, "Bose SoundLink Mini", "Electronics", 99.99, "Portable Bluetooth speaker", 4.4, ["speaker", "bose", "audio"]),
    Product(25, "Fitbit Charge 5", "Electronics", 149.99, "Fitness tracker with GPS", 4.3, ["fitness", "fitbit", "wearable"]),
    Product(26, "Lego Star Wars X-Wing", "Toys", 49.99, "Star Wars themed Lego set", 4.8, ["lego", "star wars", "toy"]),
    Product(27, "Barbie Dreamhouse", "Toys", 199.99, "Barbie's luxury dollhouse", 4.7, ["barbie", "dollhouse", "toy"]),
    Product(28, "Maybelline Mascara", "Beauty", 9.99, "Volumizing mascara", 4.2, ["mascara", "maybelline", "beauty"]),
    Product(29, "Oral-B Electric Toothbrush", "Health", 59.99, "Rechargeable toothbrush", 4.5, ["toothbrush", "oralb", "health"]),
    Product(30, "Samsonite Suitcase", "Travel", 139.99, "Durable travel suitcase", 4.6, ["suitcase", "samsonite", "travel"]),
    Product(31, "Canon EOS Rebel T7", "Electronics", 449.99, "Entry-level DSLR camera", 4.4, ["camera", "canon", "photography"]),
    Product(32, "Monopoly Classic", "Toys", 24.99, "Classic board game", 4.3, ["game", "monopoly", "boardgame"]),
    Product(33, "Cuisinart Air Fryer", "Home", 129.99, "Countertop air fryer oven", 4.5, ["air fryer", "cuisinart", "kitchen"]),
    Product(34, "Patagonia Backpack", "Fashion", 89.99, "Durable outdoor backpack", 4.6, ["backpack", "patagonia", "outdoor"]),
    Product(35, "FIFA 24", "Games", 69.99, "Latest football video game", 4.7, ["fifa", "video game", "football"]),
]