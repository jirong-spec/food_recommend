import requests
from config import Config
from utils import calculate_distance, logger

class RestaurantRecommender:
    """Restaurant recommendation engine using OpenStreetMap Overpass API"""
    
    def __init__(self):
        self.api_url = Config.OVERPASS_API_URL
        self.search_radius = Config.SEARCH_RADIUS
        self.max_results = Config.MAX_RESULTS
        
    def build_overpass_query(self, latitude, longitude, category=None):
        """
        Build Overpass QL query for nearby restaurants
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            category: Restaurant category filter (optional)
        
        Returns:
            Overpass QL query string
        """
        # Get amenity tags based on category
        if category and category in Config.CATEGORIES:
            amenities = Config.CATEGORIES[category]
        else:
            amenities = Config.CATEGORIES['全部']
        
        # Build amenity filter
        amenity_filters = []
        for amenity in amenities:
            amenity_filters.append(f'["amenity"="{amenity}"]')
        
        # Also search by cuisine tag if category specified
        cuisine_filters = []
        if category and category in Config.CUISINE_TAGS:
            cuisines = Config.CUISINE_TAGS[category]
            for cuisine in cuisines:
                cuisine_filters.append(f'["cuisine"="{cuisine}"]')
        
        # Combine filters
        all_filters = amenity_filters + cuisine_filters
        filter_query = ''.join([f'node{f}(around:{self.search_radius},{latitude},{longitude});' for f in all_filters])
        
        # Overpass QL query
        query = f"""
        [out:json][timeout:25];
        (
            {filter_query}
        );
        out body;
        >;
        out skel qt;
        """
        
        return query
    
    def search_nearby_restaurants(self, latitude, longitude, category=None):
        """
        Search for nearby restaurants using Overpass API
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            category: Restaurant category filter (optional)
        
        Returns:
            List of restaurant data
        """
        query = self.build_overpass_query(latitude, longitude, category)
        
        try:
            logger.info(f"Searching restaurants near ({latitude}, {longitude}) with category: {category}")
            
            response = requests.post(
                self.api_url,
                data={'data': query},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract elements (nodes)
            elements = data.get('elements', [])
            
            # Filter to only include nodes with names
            restaurants = []
            for element in elements:
                if element.get('type') == 'node' and element.get('tags', {}).get('name'):
                    restaurants.append(element)
            
            logger.info(f"Found {len(restaurants)} restaurants from OSM")
            return restaurants
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Overpass API: {e}")
            return []
        except Exception as e:
            logger.error(f"Error processing Overpass data: {e}")
            return []
    
    def calculate_score(self, restaurant, user_lat, user_lon, category=None):
        """
        Calculate recommendation score for a restaurant
        
        Since OSM doesn't have ratings, we focus on:
        - Distance (70% weight)
        - Category match (30% weight)
        
        Args:
            restaurant: Restaurant data from Overpass API
            user_lat: User's latitude
            user_lon: User's longitude
            category: User's preferred category
        
        Returns:
            Tuple of (score, distance_km)
        """
        # Calculate distance
        rest_lat = restaurant.get('lat')
        rest_lon = restaurant.get('lon')
        distance_km = calculate_distance(user_lat, user_lon, rest_lat, rest_lon)
        
        # Normalize distance (0 = closest, 1 = farthest within radius)
        max_distance_km = self.search_radius / 1000.0
        distance_normalized = min(distance_km / max_distance_km, 1.0)
        
        # Category match
        category_match = 0.0
        if category and category != '全部':
            tags = restaurant.get('tags', {})
            amenity = tags.get('amenity', '')
            cuisine = tags.get('cuisine', '')
            
            # Check if amenity or cuisine matches category
            category_amenities = Config.CATEGORIES.get(category, [])
            category_cuisines = Config.CUISINE_TAGS.get(category, [])
            
            if amenity in category_amenities or cuisine in category_cuisines:
                category_match = 1.0
            # Partial match for cuisine tags
            elif any(c in cuisine for c in category_cuisines):
                category_match = 0.5
        
        # Calculate final score (distance-focused since no ratings)
        score = (
            Config.WEIGHT_DISTANCE * (1 - distance_normalized) +
            Config.WEIGHT_CATEGORY * category_match
        )
        
        return score, distance_km
    
    def get_recommendations(self, latitude, longitude, category=None):
        """
        Get top restaurant recommendations
        
        Args:
            latitude: User's latitude
            longitude: User's longitude
            category: Restaurant category filter
        
        Returns:
            List of recommended restaurants with scores
        """
        # Search nearby restaurants
        restaurants = self.search_nearby_restaurants(latitude, longitude, category)
        
        if not restaurants:
            return []
        
        # Calculate scores for each restaurant
        scored_restaurants = []
        for restaurant in restaurants:
            tags = restaurant.get('tags', {})
            score, distance = self.calculate_score(restaurant, latitude, longitude, category)
            
            # Extract address components
            addr_street = tags.get('addr:street', '')
            addr_housenumber = tags.get('addr:housenumber', '')
            addr_city = tags.get('addr:city', '')
            
            # Build address string
            address_parts = []
            if addr_city:
                address_parts.append(addr_city)
            if addr_street:
                address_parts.append(addr_street)
            if addr_housenumber:
                address_parts.append(addr_housenumber)
            
            address = ' '.join(address_parts) if address_parts else '地址未提供'
            
            scored_restaurants.append({
                'name': tags.get('name', 'Unknown'),
                'address': address,
                'distance_km': distance,
                'score': score,
                'latitude': restaurant.get('lat'),
                'longitude': restaurant.get('lon'),
                'amenity': tags.get('amenity', ''),
                'cuisine': tags.get('cuisine', ''),
                'phone': tags.get('phone', ''),
                'website': tags.get('website', ''),
                'opening_hours': tags.get('opening_hours', ''),
            })
        
        # Sort by score (highest first) and return top N
        scored_restaurants.sort(key=lambda x: x['score'], reverse=True)
        top_recommendations = scored_restaurants[:self.max_results]
        
        logger.info(f"Returning {len(top_recommendations)} recommendations")
        return top_recommendations
