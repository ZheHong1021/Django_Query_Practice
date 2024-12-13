#region 【CORS設定】支持跨域配置开始
CORS_ORIGIN_ALLOW_ALL = True # 允許所有跨站請求, 且whitelist不會被使用
# CORS_ORIGIN_WHITELIST = ( # 設定白名單
# ) 

CORS_ALLOW_CREDENTIALS = True # 設定為 True 時，允許跨來源資源共用時發送 Cookie。默認值為 False

# CORS_ALLOW_ALL_ORIGINS = False # 預設『False』，填『True』代表允許任何請求的呼叫(很危險)
# CORS_ALLOWED_ORIGINS = [ # 允許這些網域可以請求資源
# ]

# CORS_ALLOWED_ORIGIN_REGEXES = [ # 填網域的列表，但是網域的名稱可以用 regular expression 來表示
# ]
# CORS_EXPOSE_HEADERS = [ # 設定要公開的自訂標頭列表，這些標頭可以在 JavaScript 中存取。
# ]
#endregion

#region 【CSRF設定】
# CSRF_COOKIE_SECURE = False # 設置為 True 後，Django 會強制要求 CSRF cookie 只能通過 HTTPS 進行傳輸
# CSRF_COOKIE_HTTPONLY = True # 指定CSRF Token是否設定為HTTPOnly，設為True就無法在瀏覽器中透過JavaScript訪問該Cookie，可以防止XSS攻擊
# SESSION_COOKIE_SECURE = True # 設置為 True 後，Django 會強制要求 session cookie 只能通過 HTTPS 進行傳輸
# CSRF_TRUSTED_ORIGINS = [
# ]
#endregion