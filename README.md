# RAG-Based Question Answering System

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** based Question Answering system using **FastAPI**. The system allows users to upload documents and ask natural language questions that are answered strictly using the uploaded document content.

The project is designed as an **API-first system** with an explicit implementation of document ingestion, chunking, embedding, retrieval, and answer generation logic. No black-box or default RAG templates are used.

---

## Features
- Upload documents in **PDF** and **TXT** formats
- Asynchronous document ingestion using background jobs
- Text chunking with overlap
- Embedding generation using SentenceTransformers
- Vector storage using FAISS (local vector database)
- Semantic similarity-based retrieval
- Confidence-based filtering to reduce hallucinations
- Answer generation using LLaMA via Groq
- Source citations attached to answers
- Metrics endpoint for monitoring system behavior

---

## Tech Stack
- **Backend**: FastAPI  
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`)  
- **Vector Store**: FAISS (CPU)  
- **LLM**: LLaMA (via Groq API)  
- **Validation**: Pydantic  
- **Metrics**: In-memory metrics tracking  
- **Language**: Python 3.10+

---

## Architecture
The system follows a modular RAG architecture consisting of:
- An asynchronous document ingestion pipeline
- A query-time retrieval and generation pipeline
- A metrics collection pipeline

📌 **Architecture Diagram:**  
`docs/architecture.png`

---

## API Endpoints

### 1. Upload Document
**POST** `/upload`

Uploads a document and triggers background ingestion.

Supported formats:
- PDF
- TXT

---

### 2. Ask Question
**POST** `/ask`

Request body:
```json
{
  "question": "What is the main topic of the document?"
}
METRICS

GET /metrics

Returns runtime metrics including:

- Total number of /ask requests
- Average response latency
- Average similarity score of retrieved chunks

All metrics are tracked in-memory and exposed via the /metrics endpoint.

------------------------------------------------------------

CHUNKING STRATEGY

A fixed chunk size with overlap is used to balance:

- Semantic completeness of text
- Retrieval precision
- Prompt size limitations of the LLM

Overlapping chunks help preserve context across chunk boundaries and reduce information loss during retrieval.

------------------------------------------------------------

RETRIEVAL FAILURE CASE

A known retrieval failure case occurs when:

- The user asks a vague, ambiguous, or out-of-scope question
- Retrieved chunks have similarity scores below the confidence threshold

In such situations, the system safely responds with:

"I don't know"

This prevents hallucinated or unsupported answers.

------------------------------------------------------------

METRICS TRACKED

The system tracks the following metrics:

- Total number of /ask requests
- Average response latency
- Average similarity score of retrieved chunks

All metrics are exposed via the /metrics endpoint.

------------------------------------------------------------

SETUP INSTRUCTIONS

1. Clone the repository

git clone <your-repo-url>
cd RAG-QA-System

2. Create a virtual environment

python -m venv venv
source venv/bin/activate
Windows: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Set environment variable

Linux / macOS:
export GROQ_API_KEY=your_api_key_here

Windows:
setx GROQ_API_KEY "your_api_key_here"

5. Run the application

uvicorn app.main:app --reload

------------------------------------------------------------

API DOCUMENTATION

Swagger UI is available at:

http://127.0.0.1:8000/docs

------------------------------------------------------------

CONSTRAINTS AND DESIGN CHOICES

- No heavy RAG frameworks were used
- Local FAISS vector database chosen for simplicity
- Explicit implementation of each pipeline stage
- API-first design with no mandatory UI layer

------------------------------------------------------------

FUTURE IMPROVEMENTS

- Hybrid retrieval (BM25 + embeddings)
- Persistent metrics storage
- Authentication and advanced rate limiting
- Streaming LLM responses
- Optional UI layer (Streamlit or frontend client)

------------------------------------------------------------

CONCLUSION

This project demonstrates a complete, explainable RAG-based Question Answering system with strong emphasis on retrieval quality, system transparency, metrics awareness, and evaluation readiness.
