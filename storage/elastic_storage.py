from elasticsearch import Elasticsearch
from datetime import datetime
import sys
import os
import warnings

# Add the root directory of your project to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import ELASTICSEARCH_HOSTS, ELASTICSEARCH_CLOUD_ID, ELASTICSEARCH_API_KEY, ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD
from utils.id_generator import generate_unique_id

# Suppress warnings for unverified HTTPS requests
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

def initialize_elasticsearch():
    """
    Initialize the Elasticsearch client.

    Returns:
        Elasticsearch: The initialized Elasticsearch client.
    """
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
    
    return es

def save_to_elasticsearch(es, document, model, unique_id=None):
    """
    Save a document to Elasticsearch with additional fields.

    Args:
        es (Elasticsearch): The Elasticsearch client.
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

def get_all_documents(es, index_name):
    try:
        response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=10000)
        documents = response['hits']['hits']
        for doc in documents:
            print(doc['_source'])
    except Exception as e:
        print(f"Failed to retrieve documents: {e}")

def text_search(es, query, index_name, k=5):
    """
    Search for documents in Elasticsearch based on text query.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        query (str): The text query to search for.
        index_name (str): The name of the index to search.
        k (int): The number of top results to return.

    Returns:
        list: The top k search results sorted by timestamp descending.
    """
    try:
        response = es.search(
            index=index_name,
            body={
                "query": {
                    "match": {
                        "text": query
                    }
                },
                "sort": [
                    {"timestamp": {"order": "desc"}}
                ],
                "size": k
            }
        )
        hits = response['hits']['hits']
        return [hit['_source'] for hit in hits]
    except Exception as e:
        print(f"Failed to search documents: {e}")
        return []

def load_specific_index(es, index_name):
    """
    Load a specific closed index by reopening it.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        index_name (str): The name of the index to load.

    Returns:
        bool: True if the index was successfully opened, False otherwise.
    """
    try:
        # Check if the index exists
        if not es.indices.exists(index=index_name):
            print(f"Index '{index_name}' does not exist.")
            return False

        # Open the index
        es.indices.open(index=index_name)
        print(f"Index '{index_name}' has been opened.")
        return True
    except Exception as e:
        if 'index_closed_exception' in str(e):
            print(f"Index '{index_name}' is already closed.")
        else:
            print(f"Failed to open index '{index_name}': {e}")
        return False

def close_specific_index(es, index_name):
    """
    Close a specific index, saving it to disk and removing it from memory.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        index_name (str): The name of the index to close.

    Returns:
        bool: True if the index was successfully closed, False otherwise.
    """
    try:
        # Check if the index exists
        if not es.indices.exists(index=index_name):
            print(f"Index '{index_name}' does not exist.")
            return False

        # Close the index
        es.indices.close(index=index_name)
        print(f"Index '{index_name}' has been closed and saved to disk.")
        return True
    except Exception as e:
        print(f"Failed to close index '{index_name}': {e}")
        return False