from app.engine.chains import get_qa_chain

# We initialize the chain and retriever at the module level.
# This acts as a singleton, preventing the app from re-reading 
# the ChromaDB from the hard drive on every single API call.
QA_CHAIN, RETRIEVER = get_qa_chain()

def get_qa_engine():
    """
    Dependency function used by FastAPI routes to access 
    the pre-loaded AI engine.
    """
    return QA_CHAIN, RETRIEVER