from elasticsearch import Elasticsearch

def generate_unique_id(es, index_name):
    """
    Generate a unique sequential ID by checking the latest ID in Elasticsearch.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        index_name (str): The name of the index to check for the latest ID.

    Returns:
        str: A unique sequential ID.
    """
    # Ensure the index has the correct mapping
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "unique_id": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "data": {"type": "text"},
                    "model": {"type": "keyword"},
                    "domain": {"type": "keyword"}
                }
            }
        })
    
    # Get the latest ID from Elasticsearch
    try:
        response = es.search(
            index=index_name,
            body={
                "query": {
                    "match_all": {}
                },
                "sort": [
                    {"unique_id": {"order": "desc"}}
                ],
                "size": 1
            }
        )
        hits = response['hits']['hits']
        if hits:
            latest_id = int(hits[0]['_source']['unique_id'])
            new_id = str(latest_id + 1)
        else:
            new_id = "1"
    except Exception as e:
        print(f"Failed to retrieve the latest ID: {e}")
        new_id = "1"
    
    return new_id