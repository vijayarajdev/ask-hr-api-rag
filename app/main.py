from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A RAG-based HR Policy Assistant supporting Gemini and OpenAI",
    version="1.0.0"
)

# Configure CORS to allow cross-origin requests from web frontends
app.add_middleware(
    CORSMiddleware,
    # In production, replace ["*"] with your specific frontend domain(s)
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routes under the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1", tags=["HR Chat"])

@app.get("/health")
def health_check():
    return {"status": "online", "provider": settings.LLM_PROVIDER}