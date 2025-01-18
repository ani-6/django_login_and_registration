"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
# To keep secret keys in environment variables
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  #Directory loaction of all apps
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

# Determine the environment and load the correct .env file
environment = os.getenv('DJANGO_ENV', 'production')

if environment == 'production':
    dotenv_path = os.path.join(BASE_DIR, '.env.production')
else:
    dotenv_path = os.path.join(BASE_DIR, '.env.development')

load_dotenv(dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',   # Add account app
    'main.apps.MainConfig',   # Add main app
    'social_django',    # Add Social login app
    'maintenance_mode',    # Maintenance mode
    'rest_framework',   # REST API
    'rest_framework.authtoken', # REST API
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',    # Compression middleware for faster page load
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',    # Maintenance mode middlerware
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',    # For social Login
                'social_django.context_processors.login_redirect',  # For social Login
                'account.context_processors.user_thumbnail_url',    # For thumbnail url
                'main.context_processors.announcement_context_processor',   # For notifications
                'main.context_processors.settings_variable_processor',  # For sub url
                'main.context_processors.user_group_processor',  # For checking group permission
            ],
        },
    },
]

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db/db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# For Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.backends.EmailBackend',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

sub_url = os.getenv('SUBURL', '')
# If the environment variable is available and not empty
if sub_url:
    # Repeat it twice with '/' as a separator
    LOGIN_REDIRECT_URL = f"/{sub_url}/"
else:
    # Otherwise, set it to blank
    LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'account:login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "base/static/"),
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = LOGIN_REDIRECT_URL + 'secure_media/'

# Custom storage variables.
GDRIVEFOLDERID=os.getenv('DriveFolderId')
SECRETFOLDERID=os.getenv('SecretFolderId')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# social auth configs for github
SOCIAL_AUTH_GITHUB_KEY = str(os.getenv('GITHUB_KEY'))
SOCIAL_AUTH_GITHUB_SECRET = str(os.getenv('GITHUB_SECRET'))

# social auth configs for google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv('GOOGLE_KEY'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv('GOOGLE_SECRET'))

# email configs
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = str(os.getenv('EMAIL_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_PASSWORD'))

# Define session age
SESSION_COOKIE_AGE = 60 * 60 * 8  #in seconds
SESSION_SAVE_EVERY_REQUEST = True
#SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
#SESSION_EXPIRE_AT_BROWSER_CLOSE=True

#Maintenance mode config
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = False
MAINTENANCE_MODE_IGNORE_STAFF = False
MAINTENANCE_MODE_IGNORE_SUPERUSER = True
MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = ()
MAINTENANCE_MODE_LOGOUT_AUTHENTICATED_USER = False
MAINTENANCE_MODE_STATUS_CODE = 503
MAINTENANCE_MODE_TEMPLATE = "error-maintenance.html"

#Rest Api
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

#Cores settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True 
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

#CSRF settings
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
CSRF_COOKIE_HTTPONLY = False  # To allow JavaScript to access the CSRF cookie
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SAMESITE = 'LAX'

#Ensure session cookies are sent
SESSION_COOKIE_SAMESITE = "Lax"
 
#Define your logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'logfile.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO', 
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Only enable file logging in production
if environment == 'production':
    LOGGING['loggers']['django']['handlers'] = ['file']
 
else:
    LOGGING['loggers']['django']['handlers'] = ['console']
   
