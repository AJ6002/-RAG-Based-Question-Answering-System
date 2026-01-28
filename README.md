# RAG-Based Question Answering System

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** based Question Answering system
using **FastAPI**. The system allows users to upload documents and ask natural language questions, and it
generates answers strictly grounded in the uploaded document content.

The focus of this project is on **clarity, explainability, and modular design** , avoiding black-box RAG
templates and explicitly implementing each stage of the pipeline.

## Key Features

```
Upload documents in PDF and TXT formats
Asynchronous document ingestion using background tasks
Text chunking with fixed size and overlap
Embedding generation using SentenceTransformers
Vector storage using FAISS (local vector database)
Semantic similarity-based retrieval
Confidence-based filtering to reduce hallucinations
Answer generation using LLaMA via Groq API
Source citations for every generated answer
Metrics endpoint for system observability
```
## Tech Stack

```
Backend Framework : FastAPI
Embedding Model : SentenceTransformers (all-MiniLM-L6-v2)
Vector Store : FAISS (CPU)
LLM : LLaMA (via Groq)
Validation : Pydantic
Metrics : In-memory aggregation
Language : Python 3.10+
```
## System Architecture

The system follows a modular RAG architecture with three main flows:

```
Document ingestion pipeline (asynchronous)
Query-time retrieval and answer generation pipeline
```
#### • • • • • • • • • • • • • • • • • • •


```
Metrics collection and exposure pipeline
```
<INSERT ARCHITECTURE DIAGRAM IMAGE HERE>

## API Design

### Upload Document

**POST** /upload

Uploads a document and triggers background ingestion.

Supported formats: - PDF - TXT

### Ask Question

**POST** /ask

Request Body:

#### {

```
"question":"What is the main topic of the document?"
}
```
Response:

#### {

```
"answer": "Generated answer based on document context",
"citations": [
{
"source": "example.pdf",
"chunk_id": 2
}
]
}
```
### Metrics

**GET** /metrics

#### •


Returns runtime metrics such as: - Total number of queries - Average response latency - Average similarity
score

#### <INSERT METRICS DESIGN IMAGE HERE>

## Chunking Strategy

A fixed chunk size with overlap is used to balance: - Semantic completeness - Retrieval precision - LLM
context window limits

Overlapping chunks help preserve context across boundaries and improve retrieval quality.

## Retrieval Failure Case

One observed failure case occurs when: - The user asks a vague or out-of-scope question - Retrieved chunks
have low similarity scores

In such scenarios, the system safely responds with **"I don't know"** instead of generating hallucinated
answers.

## Metrics Tracked

The system tracks the following metrics: - Total /ask request count - Average response latency - Average
similarity score of retrieved chunks

Metrics are exposed via the /metrics endpoint for transparency and evaluation.

## Setup Instructions

### 1. Clone the Repository

```
gitclone <your-repo-url>
cd RAG-QA-System
```
### 2. Create Virtual Environment

```
python -m venvvenv
```

Activate: - Windows: venv\\Scripts\\activate - Linux/Mac: source venv/bin/activate

### 3. Install Dependencies

```
pipinstall -r requirements.txt
```
### 4. Set Environment Variable

```
export GROQ_API_KEY=your_api_key_here
```
Windows:

```
setxGROQ_API_KEY"your_api_key_here"
```
### 5. Run the Server

```
uvicornapp.main:app--reload
```
API documentation is available at:

```
http://127.0.0.1:8000/docs
```
## Design Constraints and Choices

```
No heavy RAG frameworks used
Local FAISS vector store for simplicity
Explicit pipeline implementation
API-first design without UI
```
## Future Improvements

```
Hybrid retrieval (BM25 + embeddings)
Persistent metrics storage
Authentication and advanced rate limiting
```
#### • • • • • • •


```
Streaming LLM responses
Optional UI layer
```
## Conclusion

This project demonstrates a complete, explainable RAG-based Question Answering system with strong
emphasis on retrieval quality, system transparency, and evaluation readiness. It is designed to be easy to
understand, extend, and evaluate.



