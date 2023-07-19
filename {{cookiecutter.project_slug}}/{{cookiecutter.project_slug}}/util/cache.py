import logging
from django.core.cache import cache
from django.utils.encoding import force_str
from datetime import datetime
from rest_framework import generics
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import (
    DefaultKeyConstructor,
)

log = logging.getLogger("django")


def get_id_from_user(request):
    if (
        hasattr(request, "user")
        and request.user
        and request.user.is_authenticated
    ):
        return force_str(request.user.id)
    else:
        return "anonymous"


def get_view_id(view_instance):
    return ":".join(
        [view_instance.__module__, view_instance.__class__.__name__]
    )


def construct_key_from_request(request, view_instance):
    key = ":".join(
        [
            get_id_from_user(request),
            get_view_id(view_instance),
        ]
    )
    constructed_key = f"api_updated_at:{key}"
    return constructed_key


class UserUpdatedAtKeyBit(bits.KeyBitBase):
    def get_data(
        self, params, view_instance, view_method, request, args, kwargs
    ):
        key = construct_key_from_request(request, view_instance)
        log.info("Constructed key: %s", key)
        value = cache.get(key)
        if not value:
            value = datetime.utcnow().timestamp()
            cache.set(key, value=value)
        return force_str(value)


class DefaultObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql_query = bits.RetrieveSqlQueryKeyBit()
    user_key_bit = bits.UserKeyBit()
    model_instance = bits.ArgsKeyBit()
    updated_at_bit = UserUpdatedAtKeyBit()


class DefaultListKeyConstructor(DefaultKeyConstructor):
    list_sql_query = bits.ListSqlQueryKeyBit()
    pagination = bits.PaginationKeyBit()
    user_key_bit = bits.UserKeyBit()
    model_instance = bits.ListModelKeyBit()
    updated_at_bit = UserUpdatedAtKeyBit()


default_object_cache_key_func = DefaultObjectKeyConstructor()
default_list_cache_key_func = DefaultListKeyConstructor()


class ListCreateAPIView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        key = construct_key_from_request(request, self)
        cache.set(key, value=datetime.utcnow().timestamp())
        return super().create(request, *args, **kwargs)


class RetriveDestroyAPIView(generics.RetrieveDestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        key = construct_key_from_request(request, self)
        cache.delete(key)
        return super().destroy(request, *args, **kwargs)
