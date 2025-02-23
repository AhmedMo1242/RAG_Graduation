
import uuid
from elasticsearch import Elasticsearch

def generate_unique_id(es, index_name):
    """
    Generate a unique UUID and check for hash collisions in Elasticsearch.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        index_name (str): The name of the index to check for collisions.

    Returns:
        str: A unique UUID.
    """
    while True:
        new_id = str(uuid.uuid4())
        if not es.exists(index=index_name, id=new_id):
            return new_id