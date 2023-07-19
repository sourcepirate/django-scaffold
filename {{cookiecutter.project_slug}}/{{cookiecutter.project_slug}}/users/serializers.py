import logging
from django.db import IntegrityError
from {{cookiecutter.project_slug}}.users.models import (
    User,
)
from {{cookiecutter.project_slug}}.users.oauth2 import OAuthException
from rest_framework import serializers
from django.conf import settings
from {{cookiecutter.project_slug}}.users.oauth2 import GoogleOAuth2, FacebookOAuth2


log = logging.getLogger("django")


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "avatar_url",
            "username",
        )


class GoogleGrantSerializer(serializers.Serializer):
    """Oauth2 Serialzier for google"""

    _AUTH_SCOPES = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]

    access_token = serializers.CharField(required=True)

    def create_or_update_user(self, user_info, token):
        try:  # if exist update their tokens.
            email = user_info["email"]
            user = User.objects.get(email=email, provider="GOOGLE")
            user.access_token = user_info.get("access_token", token)
            user.refresh_token = user_info.get("refresh_token")
        except User.DoesNotExist:  # If user doesn't exist create a new one.
            user = User(username=user_info["name"], email=user_info["email"])
            user.provider = "GOOGLE"
            user.avatar_url = user_info.get("picture", None)
            user.username = "".join(user_info.get("name", "").split(" "))
            user.access_token = user_info.get("access_token", token)
            user.refresh_token = user_info.get("refresh_token", None)
        return user

    def create(self, validate_data):
        try:
            google_settings = settings.OAUTH_PROVIDERS["GOOGLE"]
            oauth2_client = GoogleOAuth2(
                client_id=google_settings["CLIENT_ID"],
                client_secret=google_settings["CLIENT_SECRET"],
                scopes=self._AUTH_SCOPES,
                redirect_uri=google_settings["REDIRECT_URL"],
            )
            token = validate_data["access_token"]
            user_info = oauth2_client.get_info("userinfo", token)
            user = self.create_or_update_user(user_info, token)
            user.save()
            return user
        except IntegrityError:
            raise OAuthException("Account already exists for this email id")


class FacebookLoginSerialzer(serializers.Serializer):

    _AUTH_SCOPES = ["id", "name", "email", "picture"]

    access_token = serializers.CharField(required=True, max_length=512)

    def create_or_update_user(self, user_info, token):
        try:  # if exist update their tokens.
            email = user_info["email"]
            user = User.objects.get(email=email, provider="FACEBOOK")
            user.access_token = user_info.get("access_token", token)
        except User.DoesNotExist:  # If user doesn't exist create a new one.
            user = User(username=user_info["name"], email=user_info["email"])
            user.provider = "FACEBOOK"
            picture = user_info["picture"]["data"]["url"]
            user.avatar_url = picture
            user.username = "".join(user_info.get("name", "").split(" "))
            user.access_token = user_info.get("access_token", token)
        return user

    def create(self, validate_data):
        try:
            fb_settings = settings.OAUTH_PROVIDERS["FACEBOOK"]
            oauth2_client = FacebookOAuth2(
                client_id=fb_settings["CLIENT_ID"],
                client_secret=fb_settings["CLIENT_SECRET"],
                scopes=self._AUTH_SCOPES,
                redirect_uri=fb_settings["REDIRECT_URL"],
            )
            token = validate_data["access_token"]
            user_info = oauth2_client.get_info(self._AUTH_SCOPES, token)
            user_info["access_token"] = token
            user = self.create_or_update_user(user_info, token)
            user.save()
            return user
        except IntegrityError:
            raise OAuthException("Account already exists for this email id")
