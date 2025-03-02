import os
from rag_manager.domain import RAGDomain
from utils.config import FAISS_STORAGE_PATH

class RAGManager:
    def __init__(self):
        """Initialize RAG Manager and connect to everything."""
        self.domains = []
        self.working_domains = {}
        self.load_all_domains()

    def load_all_domains(self):
        """Load all domain-model variations from the FAISS storage path."""
        for file_name in os.listdir(FAISS_STORAGE_PATH):
            if file_name.endswith(".index"):
                domain_model = file_name.replace(".index", "").split("_")
                if len(domain_model) == 2:
                    domain_name, model_name = domain_model
                    self.domains.append({"domain": domain_name, "model": model_name})

    def add_domain(self, domain_name: str, model_name: str, chunk_size=500, overlap=50, embedding_size=128):
        """Creates a new RAG domain with Elasticsearch and a FAISS index."""
        domain_key = (domain_name, model_name)
        if domain_key in self.working_domains or any(d["domain"] == domain_name and d["model"] == model_name for d in self.domains):
            return self.working_domains.get(domain_key) or RAGDomain(domain_name, model_name, chunk_size, overlap, embedding_size)
        
        domain = RAGDomain(domain_name, model_name, chunk_size, overlap, embedding_size)
        self.domains.append({"domain": domain_name, "model": model_name})
        self.working_domains[domain_key] = domain
        return domain

    def add_data(self, domain_name: str, model_name: str, document: dict):
        """Add data to a specific domain."""
        domain = self.load_domain(domain_name, model_name)
        domain.add_data(document)

    def list_domains(self):
        """Returns a list of all available domains."""
        return self.domains

    def load_domain(self, domain_name: str, model_name: str):
        """Loads domain metadata into memory for faster access."""
        domain_key = (domain_name, model_name)
        if domain_key in self.working_domains:
            return self.working_domains[domain_key]
        
        for domain in self.domains:
            if domain["domain"] == domain_name and domain["model"] == model_name:
                self.working_domains[domain_key] = RAGDomain(domain_name, model_name)
                return self.working_domains[domain_key]
        
        return self.add_domain(domain_name, model_name)

    def generate_prompt(self, domain_name: str, model_name: str, query: str, mode: str = "hybrid"):
        """Generate prompt using text, embedding, or hybrid search."""
        domain = self.load_domain(domain_name, model_name)
        if mode == "text":
            return domain.text_search(query)
        elif mode == "embedding":
            return domain.embedding_search(query_text=query)
        elif mode == "hybrid":
            return domain.hybrid_search(query)
        else:
            raise ValueError("Invalid mode. Choose from 'text', 'embedding', or 'hybrid'.")