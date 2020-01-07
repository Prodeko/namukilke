from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from django.contrib.staticfiles.storage import ManifestFilesMixin
from azure.common import AzureMissingResourceHttpError


class AzureMediaStorage(AzureStorage):
    account_name = "prodekostorage"
    account_key = settings.STORAGE_KEY
    azure_container = "media"
    expiration_secs = None