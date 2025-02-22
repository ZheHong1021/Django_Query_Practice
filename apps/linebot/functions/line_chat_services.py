# line_services.py
from django.conf import settings
from linebot import LineBotApi
from linebot.models import TextSendMessage, StickerSendMessage, ImageSendMessage

# 初始化 LINE Bot API
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def send_text_message(user_id, text):
    """
    發送文字訊息給指定用戶
    
    Args:
        user_id (str): LINE 用戶 ID
        text (str): 要發送的文字訊息
    
    Returns:
        bool: 發送成功返回 True，失敗返回 False
    """
    try:
        line_bot_api.push_message(
            user_id, 
            TextSendMessage(text=text)
        )
        return True
    except Exception as e:
        print(f"發送訊息失敗: {e}")
        return False

def send_sticker(user_id, package_id='1', sticker_id='1'):
    """
    發送貼圖訊息給指定用戶
    
    Args:
        user_id (str): LINE 用戶 ID
        package_id (str): 貼圖包 ID
        sticker_id (str): 貼圖 ID
    
    Returns:
        bool: 發送成功返回 True，失敗返回 False
    """
    try:
        line_bot_api.push_message(
            user_id, 
            StickerSendMessage(
                package_id=package_id,
                sticker_id=sticker_id
            )
        )
        return True
    except Exception as e:
        print(f"發送貼圖失敗: {e}")
        return False

def send_image(user_id, image_url, preview_url=None):
    """
    發送圖片訊息給指定用戶
    
    Args:
        user_id (str): LINE 用戶 ID
        image_url (str): 圖片 URL
        preview_url (str, optional): 預覽圖片 URL，預設與原圖相同
    
    Returns:
        bool: 發送成功返回 True，失敗返回 False
    """
    if preview_url is None:
        preview_url = image_url
        
    try:
        line_bot_api.push_message(
            user_id, 
            ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=preview_url
            )
        )
        return True
    except Exception as e:
        print(f"發送圖片失敗: {e}")
        return False

def send_multiple_messages(user_id, messages):
    """
    發送多種訊息給指定用戶
    
    Args:
        user_id (str): LINE 用戶 ID
        messages (list): 訊息列表，可包含不同類型的訊息
    
    Returns:
        bool: 發送成功返回 True，失敗返回 False
    """
    try:
        line_bot_api.push_message(user_id, messages)
        return True
    except Exception as e:
        print(f"發送多種訊息失敗: {e}")
        return False