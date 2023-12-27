from storages_backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    bucket_name = 'storepictures117'
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = 'storepictures117'
    location = 'static'