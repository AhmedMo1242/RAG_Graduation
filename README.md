# RAG_Graduation

## Table of Contents
1. [Description](#description)
2. [System Components](#system-components)
3. [Data Storage Strategy](#data-storage-strategy)
4. [RAG Manager Class](#rag-manager-class)
5. [RAG Domain Class](#rag-domain-class)
6. [Wrapper for Easy API Access](#wrapper-for-easy-api-access)
7. [Tasks](#tasks)
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

## Tasks

| Task | Subtask | Description | Status |
|------|---------|------------|--------|
| **1. Implement Storage Handling Manually** | 1.1 JSON Storage | Develop functions for reading and writing JSON files. | ✅ |
|  | 1.2 FAISS Index Management | Implement functions to create, and delete FAISS indices. | ✅ |
|  | 1.3 Elasticsearch Index Management | Handle structured data storage and retrieval with Elasticsearch. | ✅ |
| **2. Handle a Single Domain (`RAGDomain`)** | 2.1 Data Ingestion | Add raw text and metadata to the domain. | ✅ |
|  | 2.2 Embedding Generation | Generate embeddings and store them in FAISS and ElasticSearch. |✅ |
|  | 2.3 Text Search | Perform keyword-based search using ElasticSearch indexes. | ✅ |
|  | 2.4 Embedding Search | Find similar embeddings using FAISS. |✅ |
|  | 2.5 Hybrid Search | Combine text and embedding search for improved results. | ⏳ |
| **3. Handle Multiple Domains (`RAGManager`)** | 3.1 Add/Delete Domains | Implement functions to add and remove RAG domains. | ⏳ |
|  | 3.2 List Domains | Develop functionality to list all available domains. | ⏳ |
|  | 3.3 Model & Tokenizer Selection | Load appropriate models for embedding generation. | ⏳ |
|  | 3.4 Multi-Domain Search | Implement domain-wide search across multiple domains. | ⏳ |
| **4. Create API Wrapper (`RAGWrapper`)** | 4.1 System Initialization | Load and configure the RAG system. | ⏳ |
|  | 4.2 Data Management API | Provide easy functions to add data to a specific domain. | ⏳ |
|  | 4.3 Prompt Generation API | Implement API for generating prompts using different search modes. | ⏳ |

## Limitations - Future Work - Problems
- **Embedding Generation**: We need to choose an embedding model.
- **Embedding Search**:  Faiss output is the index of the data, we need to try to get the data from the index and store the unique ids in the index. (Issues as Faiss only use numbers as ids)
- **Hybrid Search**: We need to combine the text and embedding search.
