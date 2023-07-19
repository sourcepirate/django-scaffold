import json
import requests
import logging
from requests import Session
from urllib.parse import urlencode

log = logging.getLogger("django")


class OAuthException(Exception):
    """Base Oauth Exception"""

    pass


class OAuth2Base(object):
    """Oauth2 mix provides the interface to
    get all necessary access and refresh
    token
    """

    REQUEST_REDIRECT_BASE_URL = None
    REQUEST_EXCHANGE_CODE_URL = None

    CLIENT_ID_KEY = "client_id"
    CLIENT_SECRET_KEY = "client_secret"
    SCOPE_KEY = "scope"
    REDIRECT_URI_KEY = "redirect_uri"

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        scopes=None,
        redirect_uri=None,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._scopes = scopes
        self._redirect_uri = redirect_uri
        self._session = Session()

    def _construct_redirect_url(self):
        _scope_string = " ".join(self._scopes)
        url_params = {
            self.SCOPE_KEY: _scope_string,
            "access_type": "offline",
            self.REDIRECT_URI_KEY: self._redirect_uri,
            "response_type": "code",
            self.CLIENT_ID_KEY: self._client_id,
        }
        query_stirng = urlencode(url_params)
        return f"{self.REQUEST_REDIRECT_BASE_URL}?{query_stirng}"

    def get_redirect_uri(self):
        """get the redirect url for getting an access code"""
        return self._construct_redirect_url()

    def exchange(self, code, http_method="post", **kwargs):
        params = {
            "code": code,
            self.CLIENT_ID_KEY: self._client_id,
            self.CLIENT_SECRET_KEY: self._client_secret,
            self.REDIRECT_URI_KEY: self._redirect_uri,
        }
        params.update(kwargs)
        http_method_func = getattr(self._session, http_method)
        _request_kwargs = (
            {"data": params} if http_method == "post" else {"params": params}
        )
        response = http_method_func(
            self.REQUEST_EXCHANGE_CODE_URL, **_request_kwargs
        )
        response_json = response.json()
        if response.ok:
            return response_json
        if "error" in response_json:
            raise OAuthException(response_json.get("error"))


class GoogleOAuth2(OAuth2Base):

    REQUEST_REDIRECT_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    REQUEST_EXCHANGE_CODE_URL = "https://www.googleapis.com/oauth2/v4/token"

    API_BASE = " https://www.googleapis.com/oauth2/v2/"

    def _construct_resource_url(self, resource):
        return f"{self.API_BASE}{resource}"

    def get_info(self, attribute, token):
        """get user information from the system"""
        response = self._session.get(
            self._construct_resource_url(attribute),
            headers={"Authorization": f"Bearer {token}"},
        )
        log.info(response.json())
        if not response.ok:
            raise OAuthException("Attribute fetch failed!")
        return response.json()


class FacebookOAuth2(OAuth2Base):

    REQUEST_REDIRECT_BASE_URL = "https://www.facebook.com/v3.3/dialog/oauth"
    REQUEST_EXCHANGE_CODE_URL = (
        "https://graph.facebook.com/v3.3/oauth/access_token"
    )

    API_BASE = "https://graph.facebook.com/v3.3/me"

    def _construct_redirect_url(self):
        url_params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
        }
        log.info(url_params)
        query_string = urlencode(url_params)
        return f"{self.REQUEST_REDIRECT_BASE_URL}?{query_string}"

    def get_info(self, attribute, token):
        """get user information from the system"""

        response = self._session.get(
            self.API_BASE,
            params={"access_token": token, "fields": ",".join(attribute)},
        )

        log.info(response.json())

        if not response.ok:
            return OAuthException("Attribute fetch failed")
        return response.json()
