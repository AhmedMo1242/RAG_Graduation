import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON configuration
JSON_STORAGE_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "storage", "json"))

# Elasticsearch configuration
ELASTICSEARCH_HOSTS = ["http://localhost:10000"]
ELASTICSEARCH_CLOUD_ID = None
ELASTICSEARCH_API_KEY = None
ELASTICSEARCH_USERNAME = "elastic"
ELASTICSEARCH_PASSWORD = "AYRVyWwXLbFU-QylMbae"

# FAISS configuration
FAISS_STORAGE_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "storage", "faiss"))

# Domain metadata configuration
DOMAIN_METADATA_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "storage", "meta"))
