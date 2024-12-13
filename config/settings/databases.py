from ..django.base import *

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': { # MySQL(預設)
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': config('MYSQL_DATABASE'), # MySQL 資料庫的名稱
        'USER': config('MYSQL_USER'), # 使用者名稱
        'PASSWORD': config('MYSQL_PASSWORD'), # 密碼
        'HOST': config('DB_HOST', default='db'), # IP 地址
        'PORT': config('DB_PORT', default='3306'), # 埠號(mysql為 3306)
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
}