import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "rig-not-secret"
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = ["*"]
PKG = os.environ.get("PKG", "silk")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "demo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "proj.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "proj.wsgi.application"
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}
}
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- per-package DEFAULT configuration, exactly as each package's own
# --- README/quickstart tells you to install it. No hardening, no extras.

if PKG == "silk":
    # https://github.com/jazzband/django-silk#installation
    INSTALLED_APPS += ["silk"]
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
    if os.environ.get("SILKY_HARDENED", "0") == "1":
        # NEGATIVE CONTROL: the documented hardening. The detector must say
        # PATCHED here, or its false-positive rate is unknown.
        SILKY_AUTHENTICATION = True
        SILKY_AUTHORISATION = True
        LOGIN_URL = "/admin/login/"

elif PKG == "debug_toolbar":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    _mode = os.environ.get("DTB_IPS", "default")
    if _mode == "default":
        # what the README quickstart says
        INTERNAL_IPS = ["127.0.0.1"]
    elif _mode == "docker":
        # VERBATIM from the package's own docs, "Docker" section of installation.rst
        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]
    elif _mode == "wildcard":
        INTERNAL_IPS = ["*"]
    elif _mode == "allowall":
        # the "just make it work" snippet: a class whose __contains__ is always True
        class _AllIPs(list):
            def __contains__(self, item):
                return True

        INTERNAL_IPS = _AllIPs(["127.0.0.1"])

    if os.environ.get("DTB_XFF") == "1":
        # django-xff / ipware pattern: rewrite REMOTE_ADDR from X-Forwarded-For
        MIDDLEWARE.insert(0, "proj.xffmw.XForwardedForMiddleware")

elif PKG == "health_check":
    # 3.x wants the plugin sub-apps listed; 4.x dropped them (checks are on the view).
    import importlib.util

    INSTALLED_APPS += ["health_check"]
    for _sub in ("health_check.db", "health_check.cache", "health_check.storage"):
        if importlib.util.find_spec(_sub) is not None:
            INSTALLED_APPS.append(_sub)

elif PKG == "prometheus":
    INSTALLED_APPS += ["django_prometheus"]
    MIDDLEWARE.insert(0, "django_prometheus.middleware.PrometheusBeforeMiddleware")
    MIDDLEWARE.append("django_prometheus.middleware.PrometheusAfterMiddleware")

elif PKG == "spectacular":
    INSTALLED_APPS += ["rest_framework", "drf_spectacular"]
    REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}

elif PKG == "graphene":
    INSTALLED_APPS += ["graphene_django"]
    GRAPHENE = {"SCHEMA": "demo.schema.schema"}

elif PKG == "yasg":
    # https://drf-yasg.readthedocs.io/en/stable/readme.html#installation
    INSTALLED_APPS += ["rest_framework", "drf_yasg"]

elif PKG == "rq":
    # https://github.com/rq/django-rq#installation
    INSTALLED_APPS += ["django_rq"]
    RQ_QUEUES = {
        "default": {
            "HOST": os.environ.get("REDIS_HOST", "host.docker.internal"),
            "PORT": 6379,
            "DB": 0,
            "DEFAULT_TIMEOUT": 360,
        }
    }

elif PKG == "explorer":
    # https://django-sql-explorer.readthedocs.io/en/latest/install.html
    INSTALLED_APPS += ["explorer"]
    EXPLORER_CONNECTIONS = {"Default": "default"}
    EXPLORER_DEFAULT_CONNECTION = "default"

elif PKG == "celery_results":
    # https://django-celery-results.readthedocs.io/en/latest/getting_started.html
    INSTALLED_APPS += ["django_celery_results"]
    CELERY_RESULT_BACKEND = "django-db"
