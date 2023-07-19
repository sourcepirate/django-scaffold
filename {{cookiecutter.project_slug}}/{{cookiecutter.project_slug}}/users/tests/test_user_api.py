import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from {{cookiecutter.project_slug}}.users.models import User


class TestUserAPI(TestCase):
    """Test user api case"""

    def setUp(self):
        self.test_user = User(username="sathya", email="sathya@run.com")
        self.test_user.save()
        self.token = self.test_user.get_token()

    def test_user_profile_api(self):
        """scenario test whether the user api
        is functioning properly
        """

        response = self.client.get(
            reverse("api:users:userapi"),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        json_response = response.json()

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(json_response["id"], self.test_user.id)

    def test_user_profile_update(self):
        """scenario test whether the user api
        is functioning properly
        """

        data = {
            "first_name": "sathya",
            "last_name": "balaji",
            "username": "sathya",
        }

        response = self.client.put(
            reverse("api:users:userapi", kwargs={"pk": self.test_user.id}),
            content_type="application/json",
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)

        user = User.objects.get(id=self.test_user.id)

        self.assertEqual(user.first_name, "sathya")
        self.assertEqual(user.last_name, "balaji")

    def test_user_profile_invalid_token(self):
        """scenario test whether the user api
        is functioning properly
        """

        response = self.client.get(
            reverse("api:users:userapi"),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token token",
        )

        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_deactivate_user_account(self):
        """scenario test whether the user api
        is functioning properly
        """

        response = self.client.delete(
            reverse("api:users:userapi"),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        self.assertEquals(status.HTTP_200_OK, response.status_code)
