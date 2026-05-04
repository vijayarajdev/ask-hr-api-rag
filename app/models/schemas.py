from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    """
    Validation schema for the user's incoming question.
    """
    query: str = Field(..., examples=["What is the company policy on international travel?"])

class ChatResponse(BaseModel):
    """
    Validation schema for the AI's response. 
    This remains the same whether using Gemini or OpenAI.
    """
    answer: str = Field(..., description="The generated response from the LLM.")
    sources: List[str] = Field(
        default_factory=list, 
        description="A list of document filenames (e.g., pto_policy.md) used to generate the answer."
    )
    model_used: Optional[str] = Field(
        None, 
        description="Optional field to tell the user which provider (Gemini/OpenAI) answered the query."
    )

class IngestResponse(BaseModel):
    """
    Optional: If you decide to add an /ingest endpoint later.
    """
    status: str
    message: str
    chunks_processed: int