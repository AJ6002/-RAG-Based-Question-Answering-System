# from fastapi import FastAPI, UploadFile, File, BackgroundTasks
# from groq import Groq
# import os
# import numpy as np
# import faiss

# from app.ingestion import read_pdf, read_txt, chunk_text
# from app.embeddings import embed_texts
# from app.vector_store import save_index, load_index
# from app.retrieval import retrieve
# from app.schemas import QuestionRequest, AnswerResponse

# # ------------------ APP SETUP ------------------

# app = FastAPI(title="RAG QA System")
# # client = Groq(api_key=os.getenv("GROQ_
# # API_KEY"))
# client = Groq(api_key="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")


# UPLOAD_DIR = "data/uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # ------------------ HEALTH CHECK ------------------

# @app.get("/")
# def health_check():
#     return {"status": "running"}

# # ------------------ DOCUMENT UPLOAD ------------------

# @app.post("/upload")
# async def upload_document(
#     file: UploadFile = File(...),
#     background_tasks: BackgroundTasks = BackgroundTasks()
# ):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     background_tasks.add_task(process_document, file_path)
#     return {"message": "Document uploaded. Processing started."}

# # ------------------ BACKGROUND INGESTION ------------------

# def process_document(file_path: str):
#     if file_path.endswith(".pdf"):
#         text = read_pdf(file_path)
#     else:
#         text = read_txt(file_path)

#     chunks = chunk_text(text)
#     embeddings = embed_texts(chunks)

#     index, metadata = load_index()

#     if index is None:
#         index = faiss.IndexFlatL2(len(embeddings[0]))

#     index.add(np.array(embeddings, dtype="float32"))

#     base_id = len(metadata)
#     for i, chunk in enumerate(chunks):
#         metadata.append({
#             "text": chunk,
#             "source": os.path.basename(file_path),
#             "chunk_id": base_id + i
#         })

#     save_index(index, metadata)

# # ------------------ QUESTION ANSWERING ------------------

# @app.post("/ask", response_model=AnswerResponse)
# def ask_question(payload: QuestionRequest):
#     retrieved = retrieve(payload.question)

#     # 🔴 EARLY REJECTION
#     if not retrieved:
#         return {
#             "answer": "I don't know.",
#             "citations": []
#         }

#     context = "\n".join([r["text"] for r in retrieved])

#     prompt = f"""
# Answer the question using ONLY the context below.
# If the answer is not present, say "I don't know".

# Context:
# {context}

# Question:
# {payload.question}
# """

#     completion = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )

#     answer = completion.choices[0].message.content

#     citations = [
#         {"source": r["source"], "chunk_id": r["chunk_id"]}
#         for r in retrieved
#     ]

#     return {
#         "answer": answer,
#         "citations": citations
#     }
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from groq import Groq
import os
import numpy as np
import faiss
import time
from fastapi import Request, Depends
from app.rate_limiter import rate_limiter

from app.ingestion import read_pdf, read_txt, chunk_text
from app.embeddings import embed_texts
from app.vector_store import save_index, load_index
from app.retrieval import retrieve
from app.schemas import QuestionRequest, AnswerResponse
from app.metrics import record_query, get_metrics

# ------------------ APP SETUP ------------------

app = FastAPI(title="RAG QA System")
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = Groq(api_key="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")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------ HEALTH CHECK ------------------

@app.get("/")
def health_check():
    return {"status": "running"}

# ------------------ METRICS ------------------

@app.get("/metrics")
def metrics_endpoint():
    return get_metrics()

# ------------------ DOCUMENT UPLOAD ------------------

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    background_tasks.add_task(process_document, file_path)
    return {"message": "Document uploaded. Processing started."}

# ------------------ BACKGROUND INGESTION ------------------

def process_document(file_path: str):
    if file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    else:
        text = read_txt(file_path)

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    index, metadata = load_index()

    if index is None:
        index = faiss.IndexFlatL2(len(embeddings[0]))

    index.add(np.array(embeddings, dtype="float32"))

    base_id = len(metadata)
    for i, chunk in enumerate(chunks):
        metadata.append({
            "text": chunk,
            "source": os.path.basename(file_path),
            "chunk_id": base_id + i
        })

    save_index(index, metadata)

# ------------------ QUESTION ANSWERING ------------------

@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest,
    request: Request,
    _: None = Depends(rate_limiter)):
    start_time = time.time()

    retrieved, max_similarity = retrieve(payload.question)

    latency_ms = (time.time() - start_time) * 1000

    # 🔴 REJECTED
    if not retrieved:
        record_query(
            similarity=None,
            latency_ms=latency_ms,
            rejected=True
        )
        return {
            "answer": "I don't know.",
            "citations": []
        }

    context = "\n".join([r["text"] for r in retrieved])

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{payload.question}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = completion.choices[0].message.content

    record_query(
        similarity=max_similarity,
        latency_ms=latency_ms,
        rejected=False
    )

    citations = [
        {"source": r["source"], "chunk_id": r["chunk_id"]}
        for r in retrieved
    ]

    return {
        "answer": answer,
        "citations": citations
    }
