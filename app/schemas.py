from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    question: str


class Citation(BaseModel):
    source: str
    chunk_id: int


class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]
