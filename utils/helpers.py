import json
import os
import faiss
from elasticsearch import Elasticsearch
from storage.elastic_storage import save_to_elasticsearch, get_all_documents
from storage.faiss_storage import save_to_faiss, load_index_from_disk, save_index_to_disk, generate_fake_embeddings
from utils.config import JSON_STORAGE_PATH, FAISS_STORAGE_PATH
from utils.id_generator import generate_unique_id

def sync_json_to_es_faiss(es, domain_name, model_name):
    """
    Sync all JSON documents into Elasticsearch and FAISS.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        domain_name (str): The domain name.
        model_name (str): The model name.

    Returns:
        tuple: The FAISS index and Elasticsearch client.
    """
    index_name = f"{domain_name}_{model_name}".lower()
    faiss_index = None

    # Check if FAISS index exists
    faiss_file_path = os.path.join(FAISS_STORAGE_PATH, f"{domain_name}_{model_name}.index")
    if os.path.exists(faiss_file_path):
        faiss_index = load_index_from_disk(domain_name, model_name)
    else:
        # Create a new FAISS index if it does not exist
        faiss_index = faiss.IndexFlatL2(128)  # Assuming 128-dimensional embeddings

    # Check if Elasticsearch index exists
    if es.indices.exists(index=index_name):
        # Get all documents from Elasticsearch and sort by timestamp
        es_documents = get_all_documents(es, index_name)
        if es_documents:
            es_documents.sort(key=lambda x: x['timestamp'], reverse=True)
            last_es_timestamp = es_documents[0]['timestamp']
        else:
            last_es_timestamp = None
    else:
        last_es_timestamp = None

    file_path = os.path.join(JSON_STORAGE_PATH, f"{domain_name}.json")
    if not os.path.exists(file_path):
        # Create an empty JSON file if it does not exist
        with open(file_path, 'w') as f:
            json.dump([], f)

    with open(file_path, 'r') as f:
        documents = json.load(f)
        for document in documents:
            if last_es_timestamp and document['timestamp'] <= last_es_timestamp:
                continue
            unique_id = generate_unique_id(es, index_name)
            document['unique_id'] = unique_id
            embeddings = generate_fake_embeddings(document['text'])
            save_to_elasticsearch(es, document, model_name, unique_id)
            save_to_faiss(document, model_name, faiss_index, unique_id, embeddings)

    save_index_to_disk(faiss_index, domain_name, model_name)
    return faiss_index, es
