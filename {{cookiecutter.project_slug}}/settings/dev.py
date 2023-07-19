DEBUG = True

DEV_DOMAIN = "localhost"

OAUTH_PROVIDERS = {
    "GOOGLE": {
        "CLIENT_ID": "718073818853-dcq4tub2usgh4f0snqlkakqq41fasrmu.apps.googleusercontent.com",
        "CLIENT_SECRET": "wz-5VD87QuewFZAYbOE-DKov",
        "REDIRECT_URL": "http://localhost:8000",
    },
    "FACEBOOK": {
        "CLIENT_ID": "2371990756417604",
        "CLIENT_SECRET": "399ef1d57e59eb3402f228bfe30d1fa0",
        "REDIRECT_URL": "http://localhost:8000/",  # traling slash due to the stupid bug in facebook.
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
        "TIMEOUT": 60 * 20,
    }
}

DOMAIN_ADDRESS = "localhost"
VERIFY_VIEW_LINK = "http://{}:8000/v1/users/verify".format(DOMAIN_ADDRESS)
