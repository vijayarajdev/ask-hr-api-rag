from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.api.dependencies import get_qa_engine
from app.core.config import settings

router = APIRouter()

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
        # 1. Generate the Answer
        # The chain handles: Input -> Context Retrieval -> Prompt -> LLM
        answer = await chain.ainvoke(request.query)

        # 2. Fetch the Source Documents
        # We run the retriever separately to get the metadata/filenames
        docs = await retriever.ainvoke(request.query)
        
        # Extract unique filenames from the metadata
        sources = list(set([
            doc.metadata.get("source", "Unknown Policy") 
            for doc in docs
        ]))

        # 3. Return the structured response
        return ChatResponse(
            answer=answer,
            sources=sources,
            model_used=settings.LLM_PROVIDER
        )

    except Exception as e:
        # Catch errors (like API timeouts or missing keys) gracefully
        raise HTTPException(
            status_code=500, 
            detail=f"The AI Engine encountered an error: {str(e)}"
        )