import os
from urllib.parse import urlsplit

from django.core.exceptions import ImproperlyConfigured
from storages.backends.s3 import S3Storage


class ProfileImageStorage(S3Storage):
    def __init__(self, **kwargs):
        super().__init__(
            endpoint_url=os.environ["SUPABASE_STORAGE_ENDPOINT"],
            region_name=os.environ.get("SUPABASE_STORAGE_REGION", "us-east-1"),
            bucket_name=os.environ["SUPABASE_STORAGE_BUCKET"],
            access_key=os.environ["SUPABASE_STORAGE_ACCESS_KEY"],
            secret_key=os.environ["SUPABASE_STORAGE_SECRET_KEY"],
            addressing_style="path",
            signature_version="s3v4",
            querystring_auth=False,
            file_overwrite=False,
            **kwargs,
        )

    def url(self, name):
        project_url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
        if not project_url:
            endpoint = urlsplit(os.environ["SUPABASE_STORAGE_ENDPOINT"])
            storage_domain = ".storage.supabase.co"
            host = endpoint.hostname or ""
            if (
                endpoint.scheme not in {"http", "https"}
                or not host.endswith(storage_domain)
                or not host[: -len(storage_domain)]
            ):
                raise ImproperlyConfigured(
                    "Set SUPABASE_URL when using a non-standard Supabase Storage endpoint."
                )
            project_url = f"{endpoint.scheme}://{host[: -len(storage_domain)]}.supabase.co"

        bucket = os.environ["SUPABASE_STORAGE_BUCKET"]
        return f"{project_url}/storage/v1/object/public/{bucket}/{name}"
