import logging
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_prometheus.models import ExportModelOperationsMixin
from rest_framework.authtoken.models import Token

log = logging.getLogger("django")


class User(ExportModelOperationsMixin("user"), AbstractUser):
    """
    Base class for users and user related actions
    """

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    SIGNUP_OPTS = (
        ("GOOGLE", "google"),
        ("FACEBOOK", "facebook"),
        ("EMAIL", "email"),
    )

    is_verified = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    provider = models.CharField(
        max_length=40, choices=SIGNUP_OPTS, default="email"
    )
    refresh_token = models.CharField(max_length=255, null=True)
    access_token = models.CharField(max_length=255, null=True)
    avatar_url = models.URLField(null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

    def get_token(self):
        """get auth token for this user"""
        try:
            token = Token.objects.get(user=self)
            return token
        except Token.DoesNotExist:
            return None


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=None, **kwargs):
    """Follow up actions based on user save"""

    # Only create a token if the user is new
    # to the system.
    if instance and created:
        token = Token.objects.create(user=instance)
        token.save()
