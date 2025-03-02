import faiss
import numpy as np
import uuid
from datetime import datetime
from utils.config import FAISS_STORAGE_PATH
import os

def generate_fake_embeddings(text):
    """
    Generate fake embeddings for the given text.

    Args:
        text (str): The text to generate embeddings for.

    Returns:
        list: A list of fake embeddings.
    """
    return [ord(char) for char in text]

def save_to_faiss(document, model, index, unique_id, embeddings):
    """
    Save a document to FAISS with additional fields.

    Args:
        document (dict): The document to be saved. Must contain a 'domain' field.
        model (str): The model name to be included in the index name.
        index (faiss.Index): The FAISS index to save the embeddings to.
        unique_id (str): The unique ID to be used for the document.
        embeddings (list): The embeddings to be saved.

    Raises:
        ValueError: If the document does not contain a 'domain' field.
    """
    domain = document.get('domain')
    if not domain:
        raise ValueError("Document must contain a 'domain' field")
    
    # Add additional fields
    document['timestamp'] = datetime.utcnow().isoformat()
    document['model'] = model
    document['unique_id'] = unique_id
    
    # Ensure the embeddings match the dimension of the FAISS index
    dimension = index.d
    if len(embeddings) < dimension:
        embeddings.extend([0] * (dimension - len(embeddings)))
    elif len(embeddings) > dimension:
        embeddings = embeddings[:dimension]
    embeddings = np.array(embeddings).astype('float32').reshape(1, -1)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Add the embeddings to the FAISS index with unique_id as metadata
    index.add_with_ids(embeddings, np.array([int(unique_id)]))
    print(f"Document saved to FAISS index with ID: {document['unique_id']}")

def save_index_to_disk(index, domain, model):
    """
    Save the FAISS index to disk.

    Args:
        index (faiss.Index): The FAISS index to save.
        domain (str): The domain name.
        model (str): The model name.
    """
    file_path = os.path.join(FAISS_STORAGE_PATH, f"{domain}_{model}.index")
    faiss.write_index(index, file_path)
    print(f"FAISS index saved to {file_path}")

def load_index_from_disk(domain, model):
    """
    Load the FAISS index from disk.

    Args:
        domain (str): The domain name.
        model (str): The model name.

    Returns:
        faiss.Index: The loaded FAISS index.
    """
    file_path = os.path.join(FAISS_STORAGE_PATH, f"{domain}_{model}.index")
    index = faiss.read_index(file_path)
    if not isinstance(index, faiss.IndexIDMap):
        index = faiss.IndexIDMap(index)
    print(f"FAISS index loaded from {file_path}")
    return index

def get_top_k_from_faiss(query_text, index, k=5):
    """
    Retrieve the top k nearest neighbors from the FAISS index.

    Args:
        query_text (str): The query text to search for.
        index (faiss.Index): The FAISS index to search.
        k (int): The number of nearest neighbors to retrieve.

    Returns:
        list: The unique IDs of the top k nearest neighbors.
    """
    # Generate fake embeddings for the query text
    query_embeddings = generate_fake_embeddings(query_text)
    # Ensure the embeddings match the dimension of the FAISS index
    dimension = index.d
    if len(query_embeddings) < dimension:
        query_embeddings.extend([0] * (dimension - len(query_embeddings)))
    elif len(query_embeddings) > dimension:
        query_embeddings = query_embeddings[:dimension]
    query_embeddings = np.array(query_embeddings).astype('float32').reshape(1, -1)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(query_embeddings)
    
    # Search the FAISS index
    distances, indices = index.search(query_embeddings, k)
    return [str(idx) for idx in indices[0].tolist() if idx != -1]




