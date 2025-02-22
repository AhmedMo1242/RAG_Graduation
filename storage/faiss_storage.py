import faiss
import numpy as np
import uuid
from datetime import datetime

def generate_fake_embeddings(text):
    """
    Generate fake embeddings for the given text.

    Args:
        text (str): The text to generate embeddings for.

    Returns:
        list: A list of fake embeddings.
    """
    return [ord(char) for char in text]

def save_to_faiss(document, model, index):
    """
    Save a document to FAISS with additional fields.

    Args:
        document (dict): The document to be saved. Must contain a 'domain' field.
        model (str): The model name to be included in the index name.
        index (faiss.Index): The FAISS index to save the embeddings to.

    Raises:
        ValueError: If the document does not contain a 'domain' field.
    """
    domain = document.get('domain')
    if not domain:
        raise ValueError("Document must contain a 'domain' field")
    
    # Add additional fields
    document['timestamp'] = datetime.utcnow().isoformat()
    document['model'] = model
    document['unique_id'] = str(uuid.uuid4())
    
    # Generate fake embeddings for the text
    embeddings = generate_fake_embeddings(document['text'])
    
    # Ensure the embeddings match the dimension of the FAISS index
    dimension = index.d
    if len(embeddings) < dimension:
        embeddings.extend([0] * (dimension - len(embeddings)))
    elif len(embeddings) > dimension:
        embeddings = embeddings[:dimension]
    embeddings = np.array(embeddings).astype('float32').reshape(1, -1)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Add the embeddings to the FAISS index
    index.add(embeddings)
    print(f"Document saved to FAISS index with ID: {document['unique_id']}")

def save_index_to_disk(index, file_path):
    """
    Save the FAISS index to disk.

    Args:
        index (faiss.Index): The FAISS index to save.
        file_path (str): The file path to save the index to.
    """
    faiss.write_index(index, file_path)
    print(f"FAISS index saved to {file_path}")

def load_index_from_disk(file_path):
    """
    Load the FAISS index from disk.

    Args:
        file_path (str): The file path to load the index from.

    Returns:
        faiss.Index: The loaded FAISS index.
    """
    index = faiss.read_index(file_path)
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
        list: The indices of the top k nearest neighbors.
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
    return indices[0]

