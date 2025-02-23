from utils.helpers import sync_json_to_es_faiss
from storage.json_storage import save_to_json
from storage.faiss_storage import save_to_faiss, get_top_k_from_faiss, generate_fake_embeddings
from storage.elastic_storage import save_to_elasticsearch, text_search, initialize_elasticsearch
from utils.id_generator import generate_unique_id
from datetime import datetime

class RAGDomain:
    def __init__(self, domain_name: str, model_name: str):
        """Initialize a domain with Elasticsearch collections and FAISS index."""
        self.domain_name = domain_name
        self.model_name = model_name
        self.faiss_index, self.es = self.load()

    def load(self):
        """Load data from JSON to Elasticsearch and FAISS."""
        es = initialize_elasticsearch()
        faiss_index, es = sync_json_to_es_faiss(es, self.domain_name, self.model_name)
        return faiss_index, es

    def add_data(self, document: dict):
        """Adds a document to JSON, then to Elasticsearch and FAISS."""
        document['domain'] = self.domain_name
        document['timestamp'] = datetime.utcnow().isoformat()
        save_to_json(document)
        unique_id = generate_unique_id(self.es, f"{self.domain_name}_{self.model_name}".lower())
        document['unique_id'] = unique_id
        embeddings = generate_fake_embeddings(document['text'])
        save_to_elasticsearch(self.es, document, self.model_name, unique_id)
        save_to_faiss(document, self.model_name, self.faiss_index, unique_id, embeddings)

    def generate_embeddings(self, text: str):
        """Generate fake embeddings for the text."""
        embeddings = generate_fake_embeddings(text)
        return embeddings

    def text_search(self, query: str, k=5):
        """Performs keyword-based text search using Elasticsearch."""
        return text_search(self.es, query, f"{self.domain_name}_{self.model_name}".lower(), k)

    def embedding_search(self, query_text: str, k=5):
        """Finds similar embeddings using FAISS."""
        return get_top_k_from_faiss(query_text, self.faiss_index, k)
