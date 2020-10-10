import os

running_in_cloud = "WEBSITE_SITE_NAME" in os.environ

if running_in_cloud:
    NLP_COSMOS_ENDPOINT = os.environ["NLP_COSMOS_ENDPOINT"]
    NLP_COSMOS_KEY = os.environ["NLP_COSMOS_KEY"]
    NLP_BLOB_CONNECTION = os.environ["NLP_BLOB_CONNECTION"]
    NLP_BLOB_CONTAINER = os.environ["NLP_BLOB_CONTAINER"]
else:
    DATA_CLEAN_LEMMATIZATION = ""
    DATA_CLEAN_STEMMING = ""
    DATA_CLEAN_TOKENIZATION = ""
    NLP_COSMOS_ENDPOINT = "https://nlp-movie-data.documents.azure.com:443/"
    NLP_COSMOS_KEY = ""
    NLP_BLOB_CONNECTION = ""
    NLP_BLOB_CONTAINER = ""