from .base import *

# Insecure secret key for local development
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-wdf9=9pl_8b1a!3ozlnf2j+3p(do8iq1b78x%gb%2f*&hg=-a%",
)

# Enable debug mode locally
DEBUG = True

# Allow connections from localhost, docker network, and podman hosts
ALLOWED_HOSTS = ["*"]

# Mailer configuration for local dev (prints emails to container logs)
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}