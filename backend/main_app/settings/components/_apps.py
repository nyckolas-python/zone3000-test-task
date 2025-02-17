INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    "corsheaders",
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',

    # Local apps
    'url_management.apps.UrlManagementConfig',
    'users.apps.UsersConfig',
    'redirector.apps.RedirectorConfig'

]
