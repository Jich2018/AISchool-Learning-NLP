import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from flask import current_app as app


class Blob_Manager():

    def __init__(self):
        blob_service_client = BlobServiceClient.from_connection_string(app.config["NLP_BLOB_CONNECTION"])
        container_client = blob_service_client.get_container_client(app.config["NLP_BLOB_CONTAINER"])
        self.container = container_client

    def get(self, data):
        blob_client = self.container.get_blob_client(data["path"])
        blob_client.download_blob()