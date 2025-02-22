import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

JSON_STORAGE_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "storage", "json"))

# utils/config.py
ELASTICSEARCH_HOSTS = ["https://localhost:9200"]
ELASTICSEARCH_CLOUD_ID = None
ELASTICSEARCH_API_KEY = None
ELASTICSEARCH_USERNAME = "elastic"
ELASTICSEARCH_PASSWORD = "AYRVyWwXLbFU-QylMbae"