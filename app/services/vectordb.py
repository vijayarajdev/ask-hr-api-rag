from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

def get_embeddings():
    if settings.LLM_PROVIDER.lower() == "openai":
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.GOOGLE_API_KEY
    )

def get_vectorstore():
    return Chroma(
        persist_directory=settings.CHROMA_PATH,
        embedding_function=get_embeddings()
    )