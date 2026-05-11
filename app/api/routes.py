import logging

from fastapi import APIRouter, Depends, HTTPException
from app.engine.chains import format_docs
from app.models.schemas import ChatRequest, ChatResponse
from app.api.dependencies import get_qa_engine
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ask", response_model=ChatResponse)
async def ask_hr(
    request: ChatRequest, 
    engine_bundle = Depends(get_qa_engine)
):
    """
    The main endpoint for the HR Assistant.
    1. Receives the query.
    2. Invokes the LCEL chain for the answer.
    3. Invokes the retriever to identify which policies were used.
    """
    chain, retriever = engine_bundle

    try:
        # 1. Retrieve once and reuse the same context for answer + sources.
        docs = await retriever.ainvoke(request.query)
        context = format_docs(docs)
        answer = await chain.ainvoke({
            "context": context,
            "question": request.query,
        })
        
        # Extract unique filenames from the metadata
        sources = sorted(set([
            doc.metadata.get("source", "Unknown Policy") 
            for doc in docs
        ]))

        # 2. Return the structured response
        return ChatResponse(
            answer=answer,
            sources=sources,
            model_used=settings.LLM_PROVIDER
        )

    except Exception:
        logger.exception("AI engine failure in /api/v1/ask")
        raise HTTPException(
            status_code=500, 
            detail="The AI Engine encountered an internal error. Please try again later."
        )