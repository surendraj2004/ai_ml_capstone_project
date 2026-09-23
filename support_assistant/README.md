# Zepto Support Assistant

A RAG-based customer support assistant for answering questions about
Zepto policies.

## Architecture

The system follows this flow:

User Query
    ↓
Intent Classification
    ↓
Policy Question?
    ↓
ChromaDB Retrieval
    ↓
Top 3 Relevant Chunks
    ↓
Answer Generation
    ↓
Pydantic Response
    ↓
FastAPI `/ask`

## Knowledge Base

The assistant uses 8 policy documents covering:

1. Delivery
2. Returns and Refunds
3. Membership
4. Order Tracking
5. Cancellation
6. Damaged and Missing Items
7. Gift Cards
8. Customer Support

## RAG Pipeline

### 1. Document Ingestion

Policy documents are stored as `.txt` files inside the `docs/` directory.

### 2. Chunking

The documents are divided into smaller overlapping text chunks.

### 3. Embedding

The system uses:

`all-MiniLM-L6-v2`

to convert text chunks and user queries into vector embeddings.

### 4. Vector Database

Embeddings are stored in ChromaDB.

### 5. Retrieval

For a policy-related question, the system retrieves the top 3
relevant chunks from ChromaDB.

### 6. Answer

The retrieved context is used to generate the response.

## LangGraph Flow

The LangGraph workflow contains:

- `classify_intent`
- `retrieve_and_answer`
- `direct_answer`

Policy questions are routed to retrieval.

General questions are routed to the direct-answer node.

## Mock LLM Mode

The application uses:

`MOCK_LLM=1`

by default.

In mock mode, the application works without requiring an external
LLM API.

For general questions, the deterministic response is:

"I can only answer questions about Zepto policies right now."

The current implementation does not include a real external LLM
generation call; `MOCK_LLM=0` does not add a real LLM provider by itself.

## API

Start the application with:

```bash
uvicorn main:app --host 0.0.0.0 --port 7860