# RAG_Graduation

## Table of Contents
1. [Description](#description)
2. [System Components](#system-components)
3. [Data Storage Strategy](#data-storage-strategy)
4. [RAG Manager Class](#rag-manager-class)
5. [RAG Domain Class](#rag-domain-class)
6. [Wrapper for Easy API Access](#wrapper-for-easy-api-access)
## Description
This is RAG for our graduation project. We aim to implement a system with different domains and a conditional RAG (Retrieval-Augmented Generation). The system will manage multiple domains, handle model selection, and perform search operations using FAISS and Elasticsearch for text or embedding retrieval.

## System Components
The system consists of two main classes:
- **`RAGManager`**: Manages multiple domains, handles model selection, and search operations.
- **`RAGDomain`**: Represents a single domain, stores data, embeddings, and facilitates retrieval.

Each domain has its own database and can use different embedding models.

## Data Storage Strategy
Each RAG domain is stored in a **JSON file** for raw data persistence and backed by **FAISS** for embedding retrieval and **Elasticsearch** for text-based retrieval.

### Storage Breakdown
- **Raw Data Storage (JSON File)**
    - Stores all text data, metadata, logs, embeddings, and timestamps.
    - Acts as a persistent backup and can be reloaded when needed.
- **FAISS (Per-Domain & Model-Based)**
    - A **single index** per domain & model that contains:
        - **Embeddings** (for similarity search)
- **Elasticsearch (Per-Domain & Model-Based)**
    - A **single index** per domain & model that contains:
        - **Raw Text & Metadata** (for standard queries)
        - **Embeddings** (for similarity search)
        - **Logs & Syscalls** (for tracking interactions)
        - **Time Index** (to enable time-based retrieval)

## RAG Manager Class
The `RAGManager` class manages multiple domains and provides an API for external interactions. It is responsible for:

- Adding and deleting domains.
- Listing available domains.
- Loading domain metadata into memory.
- Selecting and loading the appropriate model/tokenizer for embedding.
- Generating prompts using:
  - Text search.
  - Embedding search.
  - Hybrid search (combining both methods).


## RAG Domain Class
The `RAGDomain` class handles data ingestion, embedding generation, and retrieval within a single domain. It is responsible for:

- Adding raw text and metadata to the domain.
- Deleting specific data based on conditions.
- Generating embeddings and storing them in FAISS and MongoDB.
- Performing keyword-based text search using MongoDB indexes.
- Finding similar embeddings using FAISS.
- Combining text and embedding search for improved results.

## Wrapper for Easy API Access
To simplify usage, a wrapper function provides an easy way to interact with the RAG system. The `RAGWrapper` class is responsible for:

- Initializing the RAG system and loading domains.
- Adding data to a specific RAG domain.
- Generating prompts across a domain using:
  - Text search.
  - Embedding search.
  - Hybrid mode.


## Limitations - Future Work - Problems
- **Embedding Generation**: We need to choose an embedding model.
- **Hybrid Search**: We need to combine the text and embedding search.
- **Prompt Generation**: We need to do a good prompt generation.
- **Testing**: We need to test the system.
- **Preforming Embedding Search**: It saves the last thing in faiss again when we load it for the first time.
