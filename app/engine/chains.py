from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.services.llm import get_llm
from app.services.vectordb import get_vectorstore
from app.engine.prompts import get_hr_prompt

def format_docs(docs):
    """Extracts text from LangChain Documents and joins them into a single string."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

def get_qa_chain():
    """
    Builds the RAG (Retrieval-Augmented Generation) pipeline.
    This chain is dynamic: it will use whichever provider is set in your .env.
    """
    # 1. Initialize our components from the services layer
    llm = get_llm()
    vectorstore = get_vectorstore()
    
    # 2. Configure the retriever (fetch top 3 most relevant policy chunks)
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # 3. Get the instruction template
    prompt = get_hr_prompt()

    # 4. Define the LCEL Chain
    # We pipe: Data Input -> Prompt -> LLM -> Clean String Output
    chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain, retriever