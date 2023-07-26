import os
from corsheaders.defaults import default_headers

# Hostname
HOSTNAME = os.environ.get("HOSTNAME_ALLOWED", "localhost")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(BASE_DIR, "/app/media")
MEDIA_URL = "/media/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.co m/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "e_16(6eaztvawiopdvxe5(*nr9rm=x5_7yg3ya0n61imjd(yua"


ALLOWED_HOSTS = ["0.0.0.0", HOSTNAME]
FRONTEND_DOMAIN = os.environ.get("FRONTEND_DOMAIN", "example.com")

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
SCRAPE_DIR = os.path.join(BASE_DIR, "scrape")

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    "http://localhost",
    "http://localhost:3000",
    "http://{}".format(HOSTNAME),
    "https://*.localhost:3000",
    "https://localhost",
    "https://{}".format(FRONTEND_DOMAIN),
)

CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-kalki-org",
]

REDIS_CONNECTION_STRING = os.environ.get("REDIS_CONNECTION_STRING")

broker_url = REDIS_CONNECTION_STRING

CELERY_BROKER_URL = broker_url

CSRF_TRUSTED_ORIGINS = ["https://{}".format(HOSTNAME)]
# Application definition
AUTH_USER_MODEL = "users.User"

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_OBJECT_CACHE_KEY_FUNC": "{{cookiecutter.project_slug}}.util.cache.default_object_cache_key_func",
    "DEFAULT_LIST_CACHE_KEY_FUNC": "{{cookiecutter.project_slug}}.util.cache.default_list_cache_key_func",
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

VENDOR_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "rest_framework_swagger",
    "guardian",
    "django_prometheus",
]

KALKI_APPS = ["{{cookiecutter.project_slug}}.users", "{{cookiecutter.project_slug}}.search"]

INSTALLED_APPS = DJANGO_APPS + VENDOR_APPS + KALKI_APPS

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # default
    "guardian.backends.ObjectPermissionBackend",
)

ROOT_URLCONF = "config.urls"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# Getting all database params

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "{{cookiecutter.project_slug}}pw")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "{{cookiecutter.project_slug}}")
POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "{{cookiecutter.project_slug}}")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 3306))


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",  # For monitoring queries.
        "NAME": POSTGRES_DATABASE,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_prometheus.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_CONNECTION_STRING,
    }
}

RDB_HOST = os.environ.get("RDB_HOST", "rethinkdb")
RDB_PORT = int(os.environ.get("RDB_PORT", 28015))


result_backend = REDIS_CONNECTION_STRING

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# Password reset token validation interval
PASSWORD_RESET_TIMEOUT_DAYS = 30


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = "/var/www/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
PROMETHEUS_LATENCY_BUCKETS = (
    0.1,
    0.2,
    0.5,
    0.6,
    0.8,
    1.0,
    2.0,
    3.0,
    4.0,
    5.0,
    6.0,
    7.5,
    9.0,
    12.0,
    15.0,
    20.0,
    30.0,
    float("inf"),
)


# EMAIL_CONFIGARATION
EMAIL_HOST_USER = os.environ.get("SMTP_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_HOST = os.environ.get("SMTP_SERVER", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
PROMETHEUS_EXPORT_MIGRATIONS = False

VERIFY_VIEW_LINK = "http://localhost:8000/v1/users/verify"

RESET_VIEW_LINK = "http://localhost:3000/frontresetview/"

VERIFY_SUCCESS_VIEW = "http://localhost:3000/emailsuccess"
VERIFY_FAILURE_VIEW = "http://localhost:3000/emailfailure"

SPACES_ACCESS_ID = os.environ.get("SPACES_ACCESS_ID", "")
SPACES_SECRET_KEY = os.environ.get("SPACES_SECRET_KEY", "")

AWS_ACCESS_KEY_ID = SPACES_ACCESS_ID
AWS_SECRET_ACCESS_KEY = SPACES_SECRET_KEY
AWS_S3_ENDPOINT_URL = "https://ams3.digitaloceanspaces.com"
AWS_S3_REGION_NAME = "ams3"
AWS_STORAGE_BUCKET_NAME = "{{cookiecutter.project_slug}}"
