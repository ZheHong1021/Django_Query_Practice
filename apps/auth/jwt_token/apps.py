from django.apps import AppConfig


class JwtTokenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth.jwt_token'
    label = 'jwt_token'
