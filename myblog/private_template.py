SECRET_KEY = '...'

MYSQL_SETTINGS = {
    'USER': '...',
    'PASSWORD': '...',
    'HOST': '...',
    'PORT': '...',
}

SENTRY_DSN = '...'

OAUTH_SETTINGS = {
    'GITHUB': {
        'CLIENT_ID': '...',
        'CLIENT_SECRET': '...',
        'CALLBACK_URL': '...'
    },
}

EMAIL_SETTING = {
    'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'HOST': 'smtp.163.com',
    'USER': '...',
    'PASSWORD': '...',
    'PORT': 25,
    'FROM_EMAIL': '...'
}
