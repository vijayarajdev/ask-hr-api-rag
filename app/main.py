import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app import __version__
from app.api.dependencies import initialize_qa_engine
from app.api.routes import router as api_router
from app.core.config import settings

logger = logging.getLogger(__name__)

# Dynamically resolve the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_qa_engine()
    logger.info("Application startup complete")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A RAG-based HR Policy Assistant supporting Gemini and OpenAI",
    version=__version__,
    lifespan=lifespan,
)

# Configure CORS to allow cross-origin requests from web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routes under the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1", tags=["HR Chat"])

@app.get("/health")
def health_check():
    return {"status": "online", "provider": settings.LLM_PROVIDER}

@app.get("/")
async def serve_index():
    return FileResponse(BASE_DIR / "index.html")

@app.get("/chat-widget.js")
async def serve_widget():
    return FileResponse(BASE_DIR / "chat-widget.js")