"""
Django settings for architecture_bank0 project.
"""

from pathlib import Path
import os

# ================================
# 📁 BASE DIRECTORY
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent


# ================================
# 🔐 SECURITY
# ================================
SECRET_KEY = 'django-insecure-1*oo9)gnv(aof3whms$owr!v!f=336hxc-1$8yn%ttdqn-5=ia'

DEBUG = False  # ✅ IMPORTANT (Render needs this)

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']


# ================================
# 📦 INSTALLED APPS
# ================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'designs',
]


# ================================
# ⚙️ MIDDLEWARE
# ================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ✅ WhiteNoise (VERY IMPORTANT)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # ✅ Fix for Render CSRF
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ================================
# 🌐 URL CONFIG
# ================================
ROOT_URLCONF = 'architecture_bank0.urls'


# ================================
# 🎨 TEMPLATES
# ================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [os.path.join(BASE_DIR, 'templates')],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'architecture_bank0.wsgi.application'


# ================================
# 🗄 DATABASE
# ================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ================================
# 🔑 PASSWORD VALIDATION
# ================================
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


# ================================
# 🌍 INTERNATIONALIZATION
# ================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# ================================
# 📁 STATIC FILES (IMPORTANT)
# ================================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ WhiteNoise Storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ================================
# 📷 MEDIA FILES
# ================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ================================
# 🔐 LOGIN REDIRECT
# ================================
LOGIN_URL = '/login/'


# ================================
# 🌐 RENDER FIXES
# ================================
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']


# ================================
# 💳 RAZORPAY (OPTIONAL)
# ================================
# RAZORPAY_KEY = "rzp_test_xxxxx"
# RAZORPAY_SECRET = "your_secret_here"