from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, LocationMessage, FollowEvent
import os

from config import Config
from recommender import RestaurantRecommender
from message_templates import (
    create_welcome_message, create_category_selection_message,
    create_carousel_message, create_location_request_message,
    create_error_message, create_searching_message
)
from utils import validate_location, logger

# Initialize Flask app
app = Flask(__name__)

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

# Initialize LINE Bot API
line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# Initialize recommender
recommender = RestaurantRecommender()

# Store user sessions (in production, use Redis or database)
user_sessions = {}

@app.route("/")
def home():
    """Health check endpoint"""
    return "LINE Restaurant Bot is running! 🍴", 200

@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook callback endpoint"""
    # Get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        abort(400)

    # Get request body as text
    body = request.get_data(as_text=True)
    logger.info(f"Request body: {body}")

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    """Handle when user follows the bot"""
    logger.info(f"New follower: {event.source.user_id}")
    
    # Send welcome message
    welcome_msg = create_welcome_message()
    line_bot_api.reply_message(event.reply_token, welcome_msg)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle text messages"""
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    logger.info(f"User {user_id} sent: {text}")
    
    # Check if it's a category selection
    if text in Config.CATEGORIES:
        # Store user's category preference
        if user_id not in user_sessions:
            user_sessions[user_id] = {}
        user_sessions[user_id]['category'] = text
        
        # Check if user has shared location
        if 'location' in user_sessions[user_id]:
            # User has location, search restaurants
            location = user_sessions[user_id]['location']
            search_and_reply(event.reply_token, user_id, location['latitude'], location['longitude'], text)
        else:
            # Request location
            location_msg = create_location_request_message()
            line_bot_api.reply_message(event.reply_token, location_msg)
    
    elif text == "選擇類別":
        # Show category selection
        category_msg = create_category_selection_message()
        line_bot_api.reply_message(event.reply_token, category_msg)
    
    else:
        # Default response - show welcome message
        welcome_msg = create_welcome_message()
        line_bot_api.reply_message(event.reply_token, welcome_msg)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    """Handle location messages - this is the key feature!"""
    user_id = event.source.user_id
    latitude = event.message.latitude
    longitude = event.message.longitude
    
    logger.info(f"User {user_id} shared location: ({latitude}, {longitude})")
    
    # Validate location
    if not validate_location(latitude, longitude):
        error_msg = create_error_message()
        line_bot_api.reply_message(event.reply_token, error_msg)
        return
    
    # Store user's location
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    user_sessions[user_id]['location'] = {
        'latitude': latitude,
        'longitude': longitude
    }
    
    # Get user's category preference (if any)
    category = user_sessions[user_id].get('category', '全部')
    
    # Search and reply with recommendations
    search_and_reply(event.reply_token, user_id, latitude, longitude, category)

def search_and_reply(reply_token, user_id, latitude, longitude, category=None):
    """
    Search for restaurants and reply with recommendations
    
    Args:
        reply_token: LINE reply token
        user_id: LINE user ID (for push messages)
        latitude: User's latitude
        longitude: User's longitude
        category: Restaurant category filter
    """
    try:
        # Get recommendations (do this first to avoid wasting reply_token)
        recommendations = recommender.get_recommendations(latitude, longitude, category)
        
        # Create carousel message
        carousel_msg = create_carousel_message(recommendations)
        
        # Create category selection for next search
        category_msg = create_category_selection_message()
        
        # Reply with both messages
        line_bot_api.reply_message(reply_token, [carousel_msg, category_msg])
        
    except Exception as e:
        logger.error(f"Error in search_and_reply: {e}")
        error_msg = create_error_message()
        try:
            line_bot_api.reply_message(reply_token, error_msg)
        except:
            pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
