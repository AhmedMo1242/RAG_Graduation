from utils.helpers import sync_json_to_es_faiss, split_text_into_chunks
from storage.json_storage import save_to_json
from storage.faiss_storage import save_to_faiss, get_top_k_from_faiss, generate_fake_embeddings
from storage.elastic_storage import save_to_elasticsearch, text_search, initialize_elasticsearch, get_all_documents
from utils.id_generator import generate_unique_id
from datetime import datetime

class RAGDomain:
    def __init__(self, domain_name: str, model_name: str, chunk_size=500, overlap=50, embedding_size=128):
        """Initialize a domain with Elasticsearch collections and FAISS index."""
        self.domain_name = domain_name
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.overlap = overlap 
        self.faiss_index, self.es, self.embedding_size = self.load(embedding_size)

    def load(self, embedding_size=128):
        """Load data from JSON to Elasticsearch and FAISS."""
        es = initialize_elasticsearch()
        faiss_index, es, embedding_size = sync_json_to_es_faiss(es, self.domain_name, self.model_name, embedding_size)
        return faiss_index, es, embedding_size

    def add_data(self, document: dict):
        """Adds a document to JSON, then to Elasticsearch and FAISS."""
        print("i'm here")
        document['domain'] = self.domain_name
        document['timestamp'] = datetime.utcnow().isoformat()
        save_to_json(document, self.domain_name)
        unique_id = generate_unique_id(self.es, f"{self.domain_name}_{self.model_name}".lower())
        document['unique_id'] = unique_id
        chunks = split_text_into_chunks(document['data'], self.chunk_size, self.overlap)
        for chunk in chunks:
            chunk_document = document.copy()
            chunk_document['data'] = chunk
            chunk_embeddings = generate_fake_embeddings(chunk)
            save_to_elasticsearch(self.es, chunk_document, self.model_name, unique_id)
            save_to_faiss(chunk_document, self.model_name, self.faiss_index, unique_id, chunk_embeddings)
        
        # Print all documents in Elasticsearch
        print("All documents in Elasticsearch:")
        get_all_documents(self.es, f"{self.domain_name}_{self.model_name}".lower())

    def text_search(self, query: str, k=5):
        """Performs keyword-based text search using Elasticsearch."""
        return text_search(self.es, query, f"{self.domain_name}_{self.model_name}".lower(), k)

    def embedding_search(self, query_text: str, k=5):
        """Finds similar embeddings using FAISS."""
        return get_top_k_from_faiss(query_text, self.faiss_index, k)
    
    def hybrid_search(self, query: str, k=5):
        """Combines keyword-based and embedding-based search."""

