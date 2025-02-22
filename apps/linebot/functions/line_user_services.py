# line_user_service.py
from django.conf import settings
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import RichMenu

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def get_followers():
    """
    獲取 LINE Bot 的所有追蹤者 (好友) 清單
    
    Returns:
        dict: 包含用戶ID清單的響應
        
    Note:
        這個方法使用 get_followers_ids() 獲取所有追蹤您 Bot 的用戶 ID
        因 LINE API 限制，每次調用會返回包含最多 1000 個用戶 ID 的分頁結果
    """
    try:
        # 初始化結果列表和下一頁標記
        all_user_ids = []
        next_cursor = None
        
        # 分頁獲取所有用戶 ID
        while True:
            followers_response = line_bot_api.get_followers_ids(next_cursor)
            all_user_ids.extend(followers_response.user_ids)
            
            # 檢查是否有下一頁
            next_cursor = followers_response.next
            if not next_cursor:
                break
        
        return {
            'success': True,
            'user_ids': all_user_ids,
            'count': len(all_user_ids)
        }
    except LineBotApiError as e:
        return {
            'success': False,
            'error': f"LINE API Error: {str(e)}"
        }

def get_user_profile(user_id):
    """
    獲取指定 LINE 用戶的詳細資料
    
    Args:
        user_id (str): LINE 用戶 ID
        
    Returns:
        dict: 用戶資料，包括顯示名稱、頭像 URL 等
    """
    try:
        profile = line_bot_api.get_profile(user_id)
        return {
            'success': True,
            'user_id': profile.user_id,
            'display_name': profile.display_name,
            'picture_url': profile.picture_url,
            'status_message': profile.status_message,
            'language': profile.language
        }
    except LineBotApiError as e:
        return {
            'success': False,
            'error': f"無法獲取用戶資料: {str(e)}"
        }

def get_all_users_profiles():
    """
    獲取所有追蹤者的詳細資料
    
    Returns:
        list: 所有用戶的詳細資料列表
    """
    followers = get_followers()
    
    if not followers['success']:
        return followers
    
    user_profiles = []
    for user_id in followers['user_ids']:
        profile = get_user_profile(user_id)
        if profile['success']:
            user_profiles.append(profile)
    
    return {
        'success': True,
        'profiles': user_profiles,
        'count': len(user_profiles)
    }

def get_group_member_ids(group_id):
    """
    獲取特定群組中的用戶 ID 列表
    
    Args:
        group_id (str): LINE 群組 ID
        
    Returns:
        dict: 包含群組成員 ID 的列表
    """
    try:
        # 初始化結果列表和下一頁標記
        all_member_ids = []
        next_cursor = None
        
        # 分頁獲取所有成員 ID
        while True:
            members_response = line_bot_api.get_group_member_ids(group_id, next_cursor)
            all_member_ids.extend(members_response.member_ids)
            
            # 檢查是否有下一頁
            next_cursor = members_response.next
            if not next_cursor:
                break
        
        return {
            'success': True,
            'group_id': group_id,
            'member_ids': all_member_ids,
            'count': len(all_member_ids)
        }
    except LineBotApiError as e:
        return {
            'success': False,
            'error': f"無法獲取群組成員: {str(e)}"
        }