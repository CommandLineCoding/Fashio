import os

from .base import *  # noqa: F403, F401

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-wdf9=9pl_8b1a!3ozlnf2j+3p(do8iq1b78x%gb%2f*&hg=-a%",
)

DEBUG = True

ALLOWED_HOSTS = ["*"]

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
