import time
import io
from boto3 import session
from botocore.client import Config
from hashlib import md5
from csv import DictWriter
from django.conf import settings


class SpacesUploader(object):
    def __init__(self):
        self._session = session.Session()
        self._client = self._session.client(
            "s3",
            endpoint_url="https://ams3.digitaloceanspaces.com",
            region_name="ams3",
            aws_access_key_id=settings.SPACES_ACCESS_ID,
            aws_secret_access_key=settings.SPACES_SECRET_KEY,
        )

    def _hash_name(self, name):
        md = md5()
        md.update(name.encode("utf-8"))
        named_hash = md.hexdigest()
        return named_hash

    def generate_upload_url(self, org, name, default_expiry=300):
        named_hash = self._hash_name(name)
        signed_url = self._client.generate_presigned_url(
            "put_object",
            Params={"Bucket": "{{cookiecutter.project_slug}}", "Key": f"{org}/{named_hash}"},
            ExpiresIn=default_expiry,
        )
        return signed_url

    def generate_fetch_url(self, org, name, default_expiry=300):
        named_hash = self._hash_name(name)
        signed_url = self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "{{cookiecutter.project_slug}}", "Key": f"{org}/{named_hash}"},
            ExpiresIn=default_expiry,
        )
        return signed_url

    def generate_obj_url(self, org, name):
        named_hash = self._hash_name(name)
        return (
            f"https://ams3.digitaloceanspaces.com/{{cookiecutter.project_slug}}/{org}/{named_hash}"
        )

    def upload(self, kalki_id, fd):
        prefix_path = settings.S3_ARCHIVE_PATH
        random_id = int(time.time())
        key_name = f"{prefix_path}/{kalki_id}/{random_id}.csv"
        self._client.upload_fileobj(fd, "{{cookiecutter.project_slug}}", key_name)
