import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for LINE Restaurant Bot"""
    
    # LINE Messaging API
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    
    # OpenStreetMap Overpass API
    OVERPASS_API_URL = os.getenv('OVERPASS_API_URL', 'https://overpass-api.de/api/interpreter')
    
    # Recommendation settings
    SEARCH_RADIUS = int(os.getenv('SEARCH_RADIUS', 2000))  # meters (default: 2km)
    MAX_RESULTS = int(os.getenv('MAX_RESULTS', 5))  # number of restaurants to recommend
    
    # Scoring weights (no rating from OSM, so we adjust)
    WEIGHT_DISTANCE = float(os.getenv('WEIGHT_DISTANCE', 0.7))  # Increased from 0.3
    WEIGHT_CATEGORY = float(os.getenv('WEIGHT_CATEGORY', 0.3))  # Increased from 0.2
    
    # OSM amenity tags for restaurant categories (in Traditional Chinese)
    CATEGORIES = {
        '飲料': ['cafe', 'coffee', 'tea', 'bubble_tea', 'juice_bar'],
        '快餐': ['fast_food', 'burger', 'sandwich', 'pizza'],
        '甜點': ['bakery', 'dessert', 'ice_cream', 'cake_shop', 'pastry'],
        '中式': ['restaurant;chinese', 'restaurant;taiwanese'],
        '日式': ['restaurant;japanese', 'restaurant;sushi', 'restaurant;ramen'],
        '西式': ['restaurant;italian', 'restaurant;french', 'restaurant;american', 'steak_house'],
        '火鍋': ['restaurant;hotpot', 'restaurant;hot_pot'],
        '小吃': ['street_food', 'food_court', 'snack_bar'],
        '全部': ['restaurant', 'cafe', 'fast_food', 'food_court', 'bakery']  # All food-related amenities
    }
    
    # OSM cuisine tags mapping
    CUISINE_TAGS = {
        '飲料': ['coffee_shop', 'tea', 'bubble_tea', 'juice'],
        '快餐': ['burger', 'sandwich', 'pizza', 'chicken'],
        '甜點': ['cake', 'ice_cream', 'dessert', 'pastry'],
        '中式': ['chinese', 'taiwanese', 'cantonese'],
        '日式': ['japanese', 'sushi', 'ramen', 'udon'],
        '西式': ['italian', 'french', 'american', 'steak'],
        '火鍋': ['hotpot', 'hot_pot'],
        '小吃': ['street_food', 'noodle', 'dumpling']
    }
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.LINE_CHANNEL_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")
        if not Config.LINE_CHANNEL_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET is not set")

