from linebot.models import (
    TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn,
    URIAction, MessageAction, QuickReply, QuickReplyButton, LocationAction
)
from utils import format_distance
from config import Config
import urllib.parse

def create_welcome_message():
    """Create welcome message with quick reply buttons"""
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=LocationAction(label="📍 分享我的位置")),
        QuickReplyButton(action=MessageAction(label="🍽️ 全部", text="全部")),
        QuickReplyButton(action=MessageAction(label="☕ 飲料", text="飲料")),
        QuickReplyButton(action=MessageAction(label="🍔 快餐", text="快餐")),
        QuickReplyButton(action=MessageAction(label="🍰 甜點", text="甜點")),
    ])
    
    message = TextSendMessage(
        text="歡迎使用餐廳推薦機器人！🍴\n\n請分享您的位置，我會為您推薦附近的美食餐廳。\n\n您也可以選擇餐廳類別來篩選結果。",
        quick_reply=quick_reply
    )
    
    return message

def create_category_selection_message():
    """Create category selection message with quick reply"""
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🍽️ 全部", text="全部")),
        QuickReplyButton(action=MessageAction(label="☕ 飲料", text="飲料")),
        QuickReplyButton(action=MessageAction(label="🍔 快餐", text="快餐")),
        QuickReplyButton(action=MessageAction(label="🍰 甜點", text="甜點")),
        QuickReplyButton(action=MessageAction(label="🥘 中式", text="中式")),
        QuickReplyButton(action=MessageAction(label="🍱 日式", text="日式")),
        QuickReplyButton(action=MessageAction(label="🍝 西式", text="西式")),
        QuickReplyButton(action=MessageAction(label="🍲 火鍋", text="火鍋")),
        QuickReplyButton(action=MessageAction(label="🥟 小吃", text="小吃")),
    ])
    
    message = TextSendMessage(
        text="請選擇您想要的餐廳類別：",
        quick_reply=quick_reply
    )
    
    return message

def create_carousel_message(recommendations):
    """
    Create carousel template message for restaurant recommendations
    
    Args:
        recommendations: List of recommended restaurants
    
    Returns:
        TemplateSendMessage with CarouselTemplate
    """
    if not recommendations:
        return TextSendMessage(text="抱歉，附近沒有找到符合條件的餐廳。請試試其他類別或位置。")
    
    columns = []
    for restaurant in recommendations:
        # Format distance
        distance_text = format_distance(restaurant['distance_km'])
        
        # Create Google Maps URL (using restaurant name for better results)
        # We use the name + address (city/street) to make it more accurate
        search_query = f"{restaurant['name']}"
        if restaurant.get('address') and restaurant['address'] != '地址未提供':
             # Extract just the city part if possible, or use full address
             # This helps find the specific branch
             search_query += f" {restaurant['address']}"
             
        encoded_query = urllib.parse.quote(search_query)
        maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
        
        # Truncate name if too long
        name = restaurant['name']
        if len(name) > 40:
            name = name[:37] + "..."
        
        # Truncate address if too long
        address = restaurant['address']
        if len(address) > 60:
            address = address[:57] + "..."
        
        # Build info text (distance + address + cuisine if available)
        info_parts = [f"📍 {distance_text}"]
        if address != '地址未提供':
            info_parts.append(address)
        if restaurant.get('cuisine'):
            info_parts.append(f"🍽️ {restaurant['cuisine']}")
        
        info_text = '\n'.join(info_parts)
        
        # Create column
        column = CarouselColumn(
            title=name,
            text=info_text,
            actions=[
                URIAction(
                    label="🗺️ 開啟地圖導航",
                    uri=maps_url
                ),
                URIAction(
                    label="📱 查看位置",
                    uri=f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
                )
            ]
        )
        columns.append(column)
    
    carousel_template = CarouselTemplate(columns=columns)
    message = TemplateSendMessage(
        alt_text=f"為您推薦 {len(recommendations)} 家餐廳",
        template=carousel_template
    )
    
    return message

def create_location_request_message():
    """Create message requesting user location"""
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=LocationAction(label="📍 分享我的位置"))
    ])
    
    message = TextSendMessage(
        text="請先分享您的位置，我才能為您推薦附近的餐廳喔！😊",
        quick_reply=quick_reply
    )
    
    return message

def create_error_message():
    """Create error message"""
    message = TextSendMessage(
        text="抱歉，系統發生錯誤。請稍後再試。😔"
    )
    
    return message

def create_searching_message(category=None):
    """Create searching message"""
    if category and category != '全部':
        text = f"正在搜尋附近的{category}餐廳...🔍"
    else:
        text = "正在搜尋附近的餐廳...🔍"
    
    message = TextSendMessage(text=text)
    return message
