from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm():
    if settings.LLM_PROVIDER.lower() == "openai":
        return ChatOpenAI(
            model="gpt-4o", 
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0,
        google_api_key=settings.GOOGLE_API_KEY
    )