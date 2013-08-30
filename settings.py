# -*- coding: utf-8 -*-

import os.path
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = "Europe/Rome"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "uploads")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/uploads/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/static/"

# Additional directories which hold static files
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_ROOT, "static"),
# ]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Subdirectory of COMPRESS_ROOT to store the cached media files in
# COMPRESS_OUTPUT_DIR = "cache"

# http://stackoverflow.com/questions/7602904/temporarily-disabling-django-caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
    # =todo: upgrade to django 1.4
    # "django.template.loaders.filesystem.Loader",
    # "django.template.loaders.app_directories.Loader",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware", # enabling redirects app
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware", # enabling middleware for flatpages app
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "itwishlist.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    # "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static",
    
    "pinax.core.context_processors.pinax_settings",

    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.markup",
    "django.contrib.comments",
    "django.contrib.flatpages", # enabling flatpages app
    "django.contrib.redirects", # enabling redirects app
    
    "pinax.templatetags",
    
    # theme
    "pinax_theme_bootstrap",
    "django_forms_bootstrap",
    
    # external
    "notification", # must be first
    "staticfiles",
    "compressor",
    # "debug_toolbar",
    "mailer",
    "django_openid",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
    "idios",
    "metron",
    
    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    
    # Misc
    "voting",
    "relationships",
    "easy_thumbnails",
    # 'generic_aggregation'

    # Project
    "profiles",
    "blog",
    "fileupload",
    
    "gunicorn",
    # =todo: authenticate against drupal users db
    # "ippcdrupal",
    # http://docs.gunicorn.org/en/latest/run.html
    # START:
    # gunicorn --daemon wsgi:application
    
    # STOP: ps aux | grep gunicorn
    # kill -HUP ####
    
    
    # First install south, then syncdb, then uncomment apps under Project above and migrate
    # "south",
]

APPEND_SLASH = True

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/%s/" % o.username,
    # "auth.user": lambda o: "/up/%s/" % o.username,
}

AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

AUTHENTICATION_BACKENDS = [
    # =todo: authenticate against drupal users db
    # 'ippcdrupal.auth_backends.DrupalUserAuthBackend',
    "pinax.apps.account.auth_backends.AuthenticationBackend",
]

# =todo: authenticate against drupal users db
# DRUPAL_SITE_PATH is the absolute path to Drupal installation
# DRUPAL_SITE_PATH = "/path/to/drupalsitename/"
# DRUPAL_SITE_NAME is the Drupal site name, e.g. example.com
# DRUPAL_SITE_NAME = "drupalsitename.tld"

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?

# =todo: authenticate against drupal users db
# LOGIN_URL = '/sso/'
# =todo: authenticate against drupal users db
# LOGIN_REDIRECT_URLNAME = 'profiles.views.sso'

LOGIN_REDIRECT_URLNAME = "desk"
LOGOUT_REDIRECT_URLNAME = "home"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# https://github.com/ilblackdragon/django-blogs
# BLOG_ENABLE_USER_BLOG = True

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from settings_local import *
except ImportError:
    pass

