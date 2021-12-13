"""
Django settings for mmb_pf project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import logging
import os
from datetime import datetime
from pathlib import Path

MMB_PF_VERSION = "0.9.0"
logger = logging.getLogger(__name__)
logger.critical(
    f"{'#'*80}\n# MMB PF v{MMB_PF_VERSION} started: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n{'#'*80}\n"
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# For regeneration
# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()
SECRET_KEY = ""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["62.109.19.127", "mmb-pf.fvds.ru", "fzeulf.mmb-pf.fvds.ru", "jl.mmb-pf.fvds.ru"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "administration.apps.AdministrationConfig",
    "ckeditor",
    "addrbook",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "administration.MMBPFUsers"
ROOT_URLCONF = "mmb_pf.urls"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# used in the admin interface
CKEDITOR_CONFIGS = {
    "basic_extended": {
        "toolbar": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "CodeSnippet",
                    "Preview",
                    "Maximize",
                    "-",
                    "Save",
                    "-",
                    "Image",
                    "Table",
                    "HorizontalRule",
                    "SpecialChar",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "-",
                    "Undo",
                    "Redo",
                    "-",
                    "Find",
                    "Replace",
                    "-",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "TextColor",
                    "BGColor",
                    "-",
                    "NumberedList",
                    "BulletedList",
                    "Blockquote",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "RemoveFormat",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "Link",
                    "Unlink",
                ],
            },
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
        ],
        "extraPlugins": "codesnippet",
        "height": 500,
        "codeBlock": {"languages": [{"language": "css", "label": "CSS"}, {"language": "xml", "label": "HTML/XML"}]},
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "mmb_pf.drf_api.custom_exception_handler",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "mmb_pf_tags": "templatetags.custom_filters",
            },
        },
    },
]

WSGI_APPLICATION = "mmb_pf.wsgi.application"
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
# these params should be changed together
SESSION_COOKIE_AGE = 31449600  # 1 year
CSRF_COOKIE_AGE = 31449600  # 1 year

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
        "TIMEOUT": None,
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "mmb_pf_debug": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/nginx/mmb_pf_debug.log",
            "maxBytes": 1024 * 1024 * 50,  # 50 MB
            "backupCount": 5,
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mmb_pf_debug"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,
        },
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# DO NOT SHARE THIS DIR AT NGINX !
# PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, "storage/")


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
