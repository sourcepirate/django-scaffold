import json
import logging
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from {{cookiecutter.project_slug}}.users.models import User
from {{cookiecutter.project_slug}}.users.oauth2 import GoogleOAuth2, OAuthException

log = logging.getLogger("django")


class TestGoogleLoginSignup(TestCase):
    """This test suite test the login and signup process
    for social login
       Following are the behaviours:
         * a new or existing user login in with the system
           via google oauth2
         * the authorization code is recived and the user
           email information is been recived by the system
         * if the user does not exist a new user entry
           is created on the database
         * if the user is already existing then his/her
           access_token, refresh_token will be updated
           by the system.
         * a security token is also generated by the system
           along with user entry.
    """

    def setUp(self):
        self.existing_user = User(
            username="sathya",
            email="sathya@clementi.com",
            refresh_token="sometoken",
            access_token="access_token",
        )
        self.existing_user.save()

    @patch.object(GoogleOAuth2, "get_info")
    @patch.object(GoogleOAuth2, "exchange")
    def test_successfull_google_oauth_login(self, exchange_mock, info_mock):
        """A very successfull google oauth login
        requires two step
           * exchange of `authorization_code` with
             `access_token`.
           * getting user profile information
             from the `resource_provider`.
        """

        exchange_mock.return_value = {}
        # exchange_mock.return_value = {
        #     "access_token": "ya29.Gls1Byu2oMRgW09vVPKTLZvI4249Mbom-n5Rn3GukFv0ofPxwpz5NDBkhR8hdEJbxr1E9AQv4AmiIuAXWsZKfQZhoX7Wu5Dd_ZjrcZC-9UL_dkjZ6ZyuLADBGuGZ",
        #     "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjExOGRmMjU0YjgzNzE4OWQxYmMyYmU5NjUwYTgyMTEyYzAwZGY1YTQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDE4OTc5ODEzMzI4MDQzNzczNDQiLCJlbWFpbCI6InBsYXNtYXNoYWRvd3hAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJaTDdLXzZZR3o5QzVvQ0VPU2lia1JBIiwiaWF0IjoxNTYxNzMyNTA1LCJleHAiOjE1NjE3MzYxMDV9.iY2QE-EV5Z9rMZ2UOL51Auo8fzD_IPNA74UU__dlmSgrA71EgB5Lix9gLQm3Da6olTpPlVc7vyrYeswm7rDY5iVxafuxwqMgRVaDEYkOv3R_41x-h_qMEcqALOorJg1jIaPRCqai7dY5Pt9-jSYhzzDY1ZOsXh8ZRliyF_SSUitzwZS2wozosujvg-duT1ZkEFClYJ5-Z5tH67aa4MUHZME88muGZ6uWjdmkjyX8ohJBPbFf5zEJ2lGtPLtifQG4h4lgeTmzGSO-kZYPVNIYjrasrrxSVuR2qD1YHJ3bPRmpNyel5mx9I8rybZ2qV1MbNZPzwukq2mrh52z20cd4jQ",
        #     "expires_in": 3600,
        #     "token_type": "Bearer",
        #     "scope": "openid https://www.googleapis.com/auth/userinfo.email",
        #     "refresh_token": "1/i33xyuNPSFRXxNlgQ1aYisIwuexEUxUBfTiAdWQjbZg",
        # }

        info_mock.return_value = {
            "id": "101897981332804377344",
            "email": "plasmashadowx@gmail.com",
            "verified_email": "true",
            "name": "sathya Narrayanan",
            "given_name": "sathya",
            "family_name": "Narrayanan",
            "picture": "https://lh4.googleusercontent.com/-z4ftUoSAZos/AAAAAAAAAAI/AAAAAAAAABQ/FlmOkdr2qts/photo.jpg",
            "locale": "en",
        }

        response = self.client.post(
            reverse("api:users:social_auth_google"),
            data={"access_token": "abcdd"},
        )

        content = response.json()

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(content["email"], "plasmashadowx@gmail.com")
        self.assertEquals(content["name"], "sathyaNarrayanan")

        user = User.objects.get(email="plasmashadowx@gmail.com")
        self.assertIsNotNone(user)
        self.assertEquals(user.provider, "GOOGLE")

    # @patch.object(GoogleOAuth2, "exchange")
    # def test_google_oauth_login_on_grant_failure(self, exchange_mock):
    #     """Testing google oauth2 login when there is a grant
    #     failure
    #         * What if the failure happens on grant exchange ?
    #         a 500 status will be emitted along with the description
    #         of the error.
    #     """

    #     exchange_mock.side_effect = OAuthException("Invalid Grant!!")

    #     response = self.client.post(
    #         reverse("api:users:social_auth_google"), data={"code": 123}
    #     )

    #     self.assertEquals(
    #         response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )
    #     content = response.json()
    #     self.assertDictEqual({"error": "Invalid Grant!!"}, content)

    @patch.object(GoogleOAuth2, "get_info")
    @patch.object(GoogleOAuth2, "exchange")
    def test_google_oauth_login_on_info_failure(
        self, exchange_mock, info_mock
    ):
        """Testing google oauth2 login when there is a information
        failure from the scope
           * What if the failure happens in the second step ?
           a 500 status emited along with error description.
        """

        exchange_mock.return_value = {}

        # exchange_mock.return_value = {
        #     "access_token": "ya29.Gls1Byu2oMRgW09vVPKTLZvI4249Mbom-n5Rn3GukFv0ofPxwpz5NDBkhR8hdEJbxr1E9AQv4AmiIuAXWsZKfQZhoX7Wu5Dd_ZjrcZC-9UL_dkjZ6ZyuLADBGuGZ",
        #     "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjExOGRmMjU0YjgzNzE4OWQxYmMyYmU5NjUwYTgyMTEyYzAwZGY1YTQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDE4OTc5ODEzMzI4MDQzNzczNDQiLCJlbWFpbCI6InBsYXNtYXNoYWRvd3hAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJaTDdLXzZZR3o5QzVvQ0VPU2lia1JBIiwiaWF0IjoxNTYxNzMyNTA1LCJleHAiOjE1NjE3MzYxMDV9.iY2QE-EV5Z9rMZ2UOL51Auo8fzD_IPNA74UU__dlmSgrA71EgB5Lix9gLQm3Da6olTpPlVc7vyrYeswm7rDY5iVxafuxwqMgRVaDEYkOv3R_41x-h_qMEcqALOorJg1jIaPRCqai7dY5Pt9-jSYhzzDY1ZOsXh8ZRliyF_SSUitzwZS2wozosujvg-duT1ZkEFClYJ5-Z5tH67aa4MUHZME88muGZ6uWjdmkjyX8ohJBPbFf5zEJ2lGtPLtifQG4h4lgeTmzGSO-kZYPVNIYjrasrrxSVuR2qD1YHJ3bPRmpNyel5mx9I8rybZ2qV1MbNZPzwukq2mrh52z20cd4jQ",
        #     "expires_in": 3600,
        #     "token_type": "Bearer",
        #     "scope": "openid https://www.googleapis.com/auth/userinfo.email",
        #     "refresh_token": "1/i33xyuNPSFRXxNlgQ1aYisIwuexEUxUBfTiAdWQjbZg",
        # }

        info_mock.side_effect = OAuthException("Attribute fetch failed!")

        response = self.client.post(
            reverse("api:users:social_auth_google"),
            data={"access_token": "abcded"},
        )

        content = response.json()

        self.assertEquals(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        self.assertDictEqual({"error": "Attribute fetch failed!"}, content)
