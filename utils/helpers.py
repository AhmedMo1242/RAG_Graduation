import json
import os
import faiss
from elasticsearch import Elasticsearch
from storage.elastic_storage import save_to_elasticsearch, get_all_documents
from storage.faiss_storage import save_to_faiss, load_index_from_disk, save_index_to_disk, generate_fake_embeddings
from utils.config import JSON_STORAGE_PATH, FAISS_STORAGE_PATH
from utils.id_generator import generate_unique_id
from utils.config import DOMAIN_METADATA_PATH

def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """
    Split text into chunks of specified size with overlap.

    Args:
        text (str): The text to split.
        chunk_size (int): The size of each chunk in words.
        overlap (int): The number of overlapping words between chunks.

    Returns:
        list: A list of text chunks.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def load_domain_metadata(metadata_file_path):
    """Load domain metadata from JSON file."""
    if os.path.exists(metadata_file_path):
        with open(metadata_file_path, 'r') as f:
            return json.load(f)
    return {}

def save_domain_metadata(metadata_file_path, metadata):
    """Save domain metadata to JSON file."""
    with open(metadata_file_path, 'w') as f:
        json.dump(metadata, f, indent=4)

def sync_json_to_es_faiss(es, domain_name, model_name, embedding_size=128):
    """
    Sync all JSON documents into Elasticsearch and FAISS.

    Args:
        es (Elasticsearch): The Elasticsearch client.
        domain_name (str): The domain name.
        model_name (str): The model name.
        embedding_size (int): The size of the embeddings.

    Returns:
        tuple: The FAISS index, Elasticsearch client, and embedding size.
    """
    index_name = f"{domain_name}_{model_name}".lower()
    faiss_index = None

    # Ensure metadata file exists
    metadata_file_path = os.path.join(DOMAIN_METADATA_PATH, f"{domain_name}_{model_name}.json")
    if not os.path.exists(metadata_file_path):
        with open(metadata_file_path, 'w') as f:
            json.dump({}, f)

    # Load or create domain metadata
    metadata = load_domain_metadata(metadata_file_path)
    domain_key = f"{domain_name}_{model_name}"
    if domain_key in metadata:
        embedding_size = metadata[domain_key].get("embedding_size", embedding_size)
    else:
        metadata[domain_key] = {"embedding_size": embedding_size}
        save_domain_metadata(metadata_file_path, metadata)

    # Check if FAISS index exists
    faiss_file_path = os.path.join(FAISS_STORAGE_PATH, f"{domain_name}_{model_name}.index")
    if os.path.exists(faiss_file_path):
        faiss_index = load_index_from_disk(domain_name, model_name)
    else:
        # Create a new FAISS index if it does not exist
        faiss_index = faiss.IndexFlatL2(embedding_size)

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
            chunks = split_text_into_chunks(document['data'])
            for chunk in chunks:
                chunk_document = document.copy()
                chunk_document['data'] = chunk
                chunk_embeddings = generate_fake_embeddings(chunk)
                save_to_elasticsearch(es, chunk_document, model_name, unique_id)
                save_to_faiss(chunk_document, model_name, faiss_index, unique_id, chunk_embeddings)

    save_index_to_disk(faiss_index, domain_name, model_name)
    return faiss_index, es, embedding_size
