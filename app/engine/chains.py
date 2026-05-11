from langchain_core.output_parsers import StrOutputParser
from app.services.llm import get_llm
from app.services.vectordb import get_vectorstore
from app.engine.prompts import get_hr_prompt

def format_docs(docs):
    """Extracts text from LangChain Documents and joins them into a single string."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

def get_qa_chain():
    """
    Builds the answer generation chain and retriever.
    Retrieval is executed separately so the same documents are used for both
    answer generation and source attribution.
    """
    llm = get_llm()
    vectorstore = get_vectorstore()
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    prompt = get_hr_prompt()

    chain = prompt | llm | StrOutputParser()
    
    return chain, retriever