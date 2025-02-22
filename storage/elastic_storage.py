from elasticsearch import Elasticsearch
from datetime import datetime
import sys
import os

# Add the root directory of your project to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import ELASTICSEARCH_HOSTS, ELASTICSEARCH_CLOUD_ID, ELASTICSEARCH_API_KEY, ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD
from utils.helpers import generate_unique_id

# Initialize Elasticsearch client
if ELASTICSEARCH_CLOUD_ID:
    es = Elasticsearch(cloud_id=ELASTICSEARCH_CLOUD_ID, api_key=ELASTICSEARCH_API_KEY)
else:
    es = Elasticsearch(
        hosts=ELASTICSEARCH_HOSTS,
        http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
        verify_certs=False  
    )

# Test connection
try:
    es.ping()
    print("Connected to Elasticsearch")
except Exception as e:
    print(f"Failed to connect to Elasticsearch: {e}")

def save_to_elasticsearch(document, model, unique_id=None):
    """
    Save a document to Elasticsearch with additional fields.

    Args:
        document (dict): The document to be saved. Must contain a 'domain' field.
        model (str): The model name to be included in the index name.
        unique_id (str): The unique ID to be used for the document. If None, a new UUID will be generated.

    Raises:
        ValueError: If the document does not contain a 'domain' field.
    """
    domain = document.get('domain')
    if not domain:
        raise ValueError("Document must contain a 'domain' field")
    
    # Add additional fields
    document['timestamp'] = datetime.utcnow().isoformat()
    document['model'] = model

    # Define the index name
    index_name = f"{domain}_{model}".lower()

    document['unique_id'] = unique_id or generate_unique_id(es, index_name)

    # Check if the index exists
    if not es.indices.exists(index=index_name):
        # Create the index if it does not exist
        es.indices.create(index=index_name)
        print(f"Created new index: {index_name}")

    # Save the document to Elasticsearch
    es.index(index=index_name, id=document['unique_id'], body=document)
    print(f"Document saved to Elasticsearch index: {index_name}")

def get_all_documents(index_name):
    try:
        response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=10000)
        documents = response['hits']['hits']
        for doc in documents:
            print(doc['_source'])
    except Exception as e:
        print(f"Failed to retrieve documents: {e}")
