"""
Django settings for Medium project.

Generated by 'django-admin startproject' using Django 3.2.22.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages
import dj_database_url
if os.path.isfile('env.py'):
    import env


#for microsoft login
import msal
from msal import PublicClientApplication
import webbrowser
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False


ALLOWED_HOSTS = ['medium-410cf7fad2b1.herokuapp.com', 'localhost', '127.0.0.1']

X_FRAME_OPTIONS = 'SAMEORIGIN'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_summernote',
    'crispy_forms',
    'social_django',
    'microsoft_auth',
    'blog',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}




MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'Medium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', 
                'microsoft_auth.context_processors.microsoft',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social_core.backends.facebook.FacebookOAuth2',  # Add Facebook backend here
    'microsoft_auth.backends.MicrosoftAuthenticationBackend',  # Add Microsoft backend here
]



SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")
#for extra info
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]

# Microsoft
APPLICATION_ID = os.environ.get("APPLICATION_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


authority_url = 'https://login.microsoftonline.com/consumers/' 
base_url = 'https://graph.microsoft.com/v1.0/'


SCOPES = ['User.Read', 'User.Export.ALL']   

client_instance = msal.ConfidentialClientApplication(
    client_id=APPLICATION_ID,
    client_credential=CLIENT_SECRET,
    authority=authority_url
)

# Check if there is already a valid token available
result = client_instance.acquire_token_silent(SCOPES, account=None)
if not result.get('access_token'):
    authorization_request_url = client_instance.get_authorization_request_url(SCOPES)
    print(authorization_request_url)
    webbrowser.open(authorization_request_url, new=True)

    authorization_code = input("Enter the authorization code: ")

    # Acquire access token using the authorization code
    result = client_instance.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=SCOPES,
    )

# Check if the access token is successfully acquired
if 'access_token' in result:
    access_token_id = result['access_token']
    headers = {'Authorization': 'Bearer ' + access_token_id}

    endpoint = base_url + 'me'
    response = requests.get(endpoint, headers=headers)





#authorization_request_url = client_instance.get_authorization_request_url(SCOPES)
#print(authorization_request_url)
#webbrowser.open(authorization_request_url, new=True)


#authorization_code = input("Enter the authorization code: ")

# Acquire access token using the authorization code
#result = client_instance.acquire_token_by_authorization_code(
#    code=authorization_code,
#    scopes=SCOPES,
#)

# Check if the access token is successfully acquired
#if 'access_token' in result:
#    access_token_id = result['access_token']
#    headers = {'Authorization': 'Bearer ' + access_token_id}

#    endpoint = base_url + 'me'
#    response = requests.get(endpoint, headers=headers)

#    if response.status_code == 200:
#        print("User data retrieved successfully:", response.json())
#    else:
#        print("Failed to retrieve user data:", response.text)
#else:
#    print("Failed to acquire access token:", result.get('error_description', 'Unknown error'))
###############################
#authorization_code = 'M.C545_BAY.2.U.0fc84154-7a3b-4c87-e4a1-94e58ba4a8ca'
#access_token = client_instance.acquire_token_by_authorization_code(
#    code=authorization_code,
#    scopes=SCOPES
#)

#access_token_id = access_token['access_token']
#headers = {'Authorization': 'Bearer ' + access_token_id}

#endpoint = base_url + 'me' 
#response = requests.get(endpoint, headers=headers)

# Tenant ID is also needed for single tenant applications
# MICROSOFT_AUTH_TENANT_ID = 'your-tenant-id-from-apps.dev.microsoft.com'

# pick one MICROSOFT_AUTH_LOGIN_TYPE value
# Microsoft authentication
# include Microsoft Accounts, Office 365 Enterpirse and Azure AD accounts
#MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

WSGI_APPLICATION = 'Medium.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
#


DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
