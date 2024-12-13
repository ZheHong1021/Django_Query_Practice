#region 【DRF設定】
REST_FRAMEWORK = {
    # Swagger-UI
    'DEFAULT_SCHEMA_CLASS': "drf_spectacular.openapi.AutoSchema",

    # 客製化 Exception捕捉
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', # 引入 Simple-JWT
        # 'rest_framework.renderers.JSONRenderer', # 不要開啟 Browsable API

        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),

    # 日期時間格式
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ], # Filter Backend

    'ORDERING_PARAM': 'ordering',  # 排序參數

    # 【限制API訪問速率(避免爬蟲過量爬取)】
    # 超過限制後，會回傳http 429錯誤
    # https://blog.typeart.cc/django%E8%88%87django%20REST%20framework(DRF)%E9%96%8B%E7%99%BC%E7%AD%86%E8%A8%98/
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle', # AnonRateThrottle：暱名用戶
    #     'rest_framework.throttling.UserRateThrottle' # UserRateThrottle：登入用戶
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '1000/day', # 用ip來判(一天限制只能 Request 100次)
    #     'user': '10000/day' # 用session來判斷(一天限制只能 Request 1000次)
    # },

    # 【換頁限制】
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 100,  # 指定每页返回的数据量

}
#endregion