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
    
    "COMPONENT_SPLIT_REQUEST": True,  

    'TAGS': [  # 定義標籤
        # {'name': '氣象資訊', 'description': '處理 [氣象資訊] 相關數據'},
    ],


}