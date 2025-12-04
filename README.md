# 🩺 MediRAG: Advanced Medical RAG System

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red?style=for-the-badge&logo=qdrant&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge&logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📖 Introduction

**MediRAG** is an industrial-grade **Retrieval-Augmented Generation (RAG)** system designed for the medical domain. Unlike basic RAG tutorials, this project focuses on **robust data engineering**, modular architecture, and advanced design patterns required to deploy generative AI systems in production.

This repository is not just a chatbot; it is a reference implementation of how to build resilient, scalable, and maintainable data pipelines for LLM applications.

---

## 🎯 Importance for ML and AI Teams

In the current Generative AI ecosystem, **80% of a RAG system's success lies in the quality of its data engineering**, not just the chosen language model.

For an ML/AI team, adopting an engineering approach like MediRAG offers critical advantages:

### 🚀 Competitive Advantages
1.  **Reproducability and Determinism**: Using managed environments (`uv`, Docker) and orchestrated pipelines eliminates the "it works on my machine" problem.
2.  **Superior Data Quality**: Implementing *Parent-Child Splitting* and *Reranking* strategies ensures the LLM receives precise context, drastically reducing hallucinations.
3.  **Long-Term Maintainability**: The architecture based on **SOLID** principles and **Dependency Injection** allows swapping components (e.g., changing Qdrant for Pinecone, or Gemini for GPT-4) without rewriting the core system.
4.  **Observability and Testing**: Treating data as code through integrity tests and E2E validation pipelines allows detecting degradation in response quality before reaching production.

---

## 🏗️ Architecture and Project Phases

### 🔹 Phase 1: Infrastructure and Ingestion Pipeline (Data Engineering)
Establishing a solid foundation focused on reproducibility and scalability.

*   **Dependency Management**: Using `uv` for deterministic virtual environments.
*   **Vector Database**: Deploying **Qdrant** via Docker Compose with data persistence.
*   **Modular ETL (SOLID)**:
    *   **Abstraction**: `BaseLoader` and `BaseCleaner` interfaces for extensibility.
    *   **Extraction**: `PDFLoader` optimized with `pypdf`.
    *   **Cleaning**: `MedicalTextCleaner` injected as a dependency to facilitate testing.

### 🔹 Phase 2: Transformation and Retrieval Strategy
Transforming raw data into optimized structures for semantic search.

*   **Parent-Document Pattern**:
    *   *Child Chunks*: Small, optimized for vector search (cosine similarity).
    *   *Parent Chunks*: Large, optimized to provide full context to the LLM.
*   **Local Vectorization**: Using `sentence-transformers` for fast, cost-free inference.
*   **Batch Ingestion**: Bulk loading into Qdrant to optimize network I/O.

### 🔹 Phase 3: Intelligent Orchestration (Advanced RAG)
Evolution towards a conversational assistant with refined reasoning.

*   **LLM Integration**: Google Gemini 1.5 Flash for response synthesis.
*   **Conversational Memory**: Sliding window system to maintain chat context.
*   **Query Rewriting**: Rephrasing user questions based on history to improve retrieval.
*   **Two-Stage Retrieval**:
    1.  **Wide Fetch**: Fast vector search (High Recall).
    2.  **Deep Rerank**: Reordering with **FlashRank** (Cross-Encoder) for maximum semantic precision.

### 🔹 Phase 4: Validation and Data CI/CD
Ensuring reliability in production environments.

*   **E2E Testing Pipeline**: Orchestrator (`src/run_pipeline.py`) that sequentially validates:
    1.  Sanity Checks (Environment/DB).
    2.  Data Integrity (ETL).
    3.  Transformation Logic.
    4.  Retrieval and Reranking Quality.
    5.  Final Generation.

---

## 🛠️ Installation and Usage Guide

### Prerequisites
*   **Docker** and **Docker Compose** installed.
*   **Python 3.11+**.
*   **uv** (Recommended) or `pip`.
*   Google Gemini API Key (in `.env`).

### 1. Environment Setup

```bash
# Clone the repository
git clone <repo-url>
cd chatbotMedico

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml  # Or requirements.txt if generated
```

### 2. Launch Infrastructure

```bash
# Start Qdrant
docker-compose up -d
```

### 3. Run Full Pipeline (E2E Validation)

To execute the entire flow, from ingestion to chat testing, use the orchestrator:

```bash
python src/run_pipeline.py
```

This command will automatically execute:
*   Qdrant connection verification.
*   Sample medical paper download.
*   Processing, cleaning, and vectorization.
*   Search and response generation tests.

---

## 📂 Project Structure

```text
src/
├── core/           # Configuration and type definitions
├── ingestion/      # Loaders, Cleaners, and Splitters (ETL)
├── retrieval/      # Search logic and Reranking
├── generation/     # LLM integration and RAG chains
├── vector_store/   # Qdrant client and management
├── testing/        # Unit and integration tests
└── run_pipeline.py # Master orchestrator
```

---

> **Note**: This project demonstrates that an effective RAG system is much more than a 50-line script. It is a complete software engineering system requiring design, testing, and a solid architecture.

## 🧠 Phase 2: Transformation, Vectorization, and Retrieval Strategy

In this phase, raw data was transformed into an optimized structure for RAG, prioritizing semantic precision without sacrificing the context richness needed for the LLM.

### 🧩 Splitting Strategy (Parent-Document Pattern)

A hierarchical data architecture was implemented to resolve the trade-off between search precision and context window:

*   **Context/Index Decoupling**: Generation of small *Child Chunks* (optimized for cosine similarity) linked to large *Parent Chunks* (optimized for LLM comprehension).
*   **Relational Traceability**: Linking via UUIDs and metadata (`parent_id`) to ensure referential integrity between search indices and content storage.

### 💾 Vectorization and Storage (Batching)

*   **Local Embeddings**: Integration of `sentence-transformers` (all-MiniLM-L6-v2) for fast local inference, eliminating API costs for vectorization.
*   **Batch Ingestion**: Implementation of bulk loading (`batch_size=64`) in Qdrant to minimize network latency and optimize write throughput (I/O).
*   **Idempotency**: Upsert logic based on deterministic IDs to allow pipeline re-runs without generating duplicates.

### 🔍 Advanced Retrieval

*   **Query Optimization**: Using Filter Push-down in Qdrant to restrict vector search strictly to "child" fragments.
*   **Context Reconstruction**: Two-step retrieval logic: Approximate Vector Search (ANN) $\to$ Point Retrieval by ID (Lookup O(1)) to deliver the full parent document to the generative model.

## 🧠 Phase 3: Intelligent Orchestration and Optimization (Advanced RAG)

The system evolved from a simple search engine to a conversational assistant with memory and refined reasoning capabilities.

### 🤖 Generation and Memory (LLM Integration)

*   **Gemini 1.5 Integration**: Implementation of the `gemini-1.5-flash` model via `langchain-google-genai` for response synthesis, leveraging its low latency and wide context window.
*   **History Management (Conversational Memory)**: Development of a manual "Sliding Window" memory system.
*   **Query Rewriting**: Implementation of an intermediate step where the LLM rephrases the user's question based on chat history (e.g., transforming "And what are its risks?" to "What are the risks of iDML?") before querying the vector database.

### ⚖️ Reranking (Semantic Precision)

A second filtering stage was added to resolve the limitations of cosine similarity search (Bi-Encoders):

*   **Two-Stage Retrieval Architecture**:
    *   **Wide Fetch**: Qdrant retrieves ~20 candidates based on approximate vector similarity.
    *   **Deep Rerank**: FlashRank (lightweight Cross-Encoder running on CPU) reorders candidates by analyzing the deep interaction between the question and each document.
*   **Result**: Drastic improvement in the relevance of documents sent to the LLM, discarding "false positives" that look similar vectorially but not semantically.

### 🛡️ Robustness and Design Patterns

*   **SOLID Refactoring**: Application of Dependency Injection in the chatbot constructor to decouple the retrieval service.
*   **Failure Handling (Graceful Degradation)**: Implementation of custom try-except blocks and `VectorDBConnectionError` exceptions to ensure the bot reports infrastructure issues amicably instead of crashing.