from config.django.base import SECRET_KEY

#region 【Simple-JWT 設定】
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5), # 指 Access Token 的靜態有效期限，時效較【短】(通常建議將其設置為幾分鐘到數小時之間)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3), # 指 Refresh Token 的有效期限，時效較【長】: user維持登入狀態的時間(通常建議將其設置為幾天到幾週之間。)
    "ROTATE_REFRESH_TOKENS": True, # (預設False):更新Token時，只會更新 access token。如果設為 True，則連 refresh token也會跟著更新
    "BLACKLIST_AFTER_ROTATION": True, # (預設False):設為True時，token更新之後，舊的 refresh 和 access token 都失去權限，這也相對安全
    "UPDATE_LAST_LOGIN": True, # (預設False):設為True時，每次登入時，都會更新 user 的 last_login 欄位

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
    
    # 指 Refresh Token 的動態有效期限
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=3),

    # "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # 使用客製化的SERIALIZER
    "TOKEN_OBTAIN_SERIALIZER": "core.auth.jwt_token_app.serializers.MyTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
#endregion