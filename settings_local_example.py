INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

DEFAULT_FROM_EMAIL = 'email@domain.tld'

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "yourdbname",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "localhost",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "5432",                             # Set to empty string for default. Not used with sqlite3.
    }
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

THUMBNAIL_DEBUG = True

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production backend?
# EMAIL_BACKEND = "mailer.backend.DbBackend"

# Testing Email Sending in local development environment
# https://docs.djangoproject.com/en/dev/topics/email/#testing-e-mail-sending
# http://blog.danawoodman.com/blog/2011/09/11/testing-email-sending-locally-in-django/
# In terminal:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
# EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD
# EMAIL_USE_TLS
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = "verysecrethereitis-CHANGE-TO-SOMETHING-ELSE-AND-DONT-SHARE"