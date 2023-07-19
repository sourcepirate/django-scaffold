import logging
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from django.http import Http404
from {{cookiecutter.project_slug}}.users.oauth2 import OAuthException
from {{cookiecutter.project_slug}}.users.models import User
from {{cookiecutter.project_slug}}.users.serializers import (
    GoogleGrantSerializer,
    FacebookLoginSerialzer,
    UserSerializer,
)

log = logging.getLogger("django")


class GoogleLoginAPI(generics.CreateAPIView):

    serializer_class = GoogleGrantSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """persist the user if not exist"""
        try:
            serializer = self.get_serializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = user.get_token()
                return Response(
                    {
                        "id": user.id,
                        "name": user.username,
                        "email": user.email,
                        "token": token.key,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Bad Gateway"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except OAuthException as ex:
            return Response(
                {"error": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            log.error("[Error]: %s", e, exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class FacebookLoginAPI(generics.CreateAPIView):

    serializer_class = FacebookLoginSerialzer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """persist the user if not exist"""
        try:
            serializer = self.get_serializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                token = user.get_token()
                return Response(
                    {
                        "id": user.id,
                        "name": user.username,
                        "email": user.email,
                        "token": token.key,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Bad Gateway"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except OAuthException as ex:
            return Response(
                {"error": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            log.error("[Error]: %s", e, exc_info=True)
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class UserAPI(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            user = self.request.user
            user = User.objects.get(id=user.id)
            return user
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        user = self.get_object()
        data = request.data
        avatar_url = user.avatar_url

        serializer = self.get_serializer(
            instance=user, data=data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save(avatar_url=avatar_url)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        user = self.get_object()
        serializer = self.get_serializer(
            instance=user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(is_active=False)
            return Response({"success": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
