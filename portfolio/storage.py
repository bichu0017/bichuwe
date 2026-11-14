import os

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
        project_url = os.environ["SUPABASE_URL"].rstrip("/")
        bucket = os.environ["SUPABASE_STORAGE_BUCKET"]
        return f"{project_url}/storage/v1/object/public/{bucket}/{name}"
