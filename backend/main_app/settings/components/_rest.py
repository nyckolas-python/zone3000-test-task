from datetime import timedelta

from main_app.settings import config

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

LOGIN_REDIRECT_URL = "/api/v1/swagger/"

SPECTACULAR_SETTINGS = {
    'TITLE': 'ZONE3000 Project API',
    'DESCRIPTION': 'ZONE3000 test project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
    },
    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticated'],
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config(
            "ACCESS_TOKEN_EXPIRES_MINUTES",
            default=60,
        ),
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        minutes=config(
            "REFRESH_TOKEN_EXPIRES_MINUTES",
            default=60 * 24 * 14,
        ),
    ),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}
