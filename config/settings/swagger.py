# swagger.py
SPECTACULAR_SETTINGS = {
    "TITLE": "Query練習平台",

    # 描述
    "DESCRIPTION": "Swagger API",

    # 版本
    "VERSION": "1.0.0", 
    
    "SERVE_INCLUDE_SCHEMA": False,

    # 確保可以使用 form/data
    "POST_PROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.hooks.postprocess_schema_customization"
    ],

    # 開啟 Swagger UI 的 persistAuthorization 功能
    # [只適合 Swagger UI開放給 development 環境使用]
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    
    "COMPONENT_SPLIT_REQUEST": True,  

    'TAGS': [  # 定義標籤
        {'name': '權限處理 - JWT', 'description': '處理 [權限處理 - JWT] 相關數據'},
        {'name': '系統管理 - 用戶', 'description': '處理 [系統管理 - 用戶] 相關數據'},
        {'name': '系統管理 - 用戶註銷紀錄', 'description': '處理 [系統管理 - 用戶註銷紀錄] 相關數據'},
        {'name': '系統管理 - 角色', 'description': '處理 [系統管理 - 角色] 相關數據'},
        {'name': '系統管理 - 權限', 'description': '處理 [系統管理 - 權限] 相關數據'},
        {'name': '系統管理 - 菜單', 'description': '處理 [系統管理 - 菜單] 相關數據'},
        {'name': '貼文', 'description': '處理 [貼文] 相關數據'},
        {'name': '貼文圖片', 'description': '處理 [貼文圖片] 相關數據'},
        {'name': 'Line服務 - 用戶', 'description': '處理 [Line服務 - 用戶] 相關數據'},
    ],


}