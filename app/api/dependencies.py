import logging
from typing import Any

from fastapi import HTTPException

from app.engine.chains import get_qa_chain

logger = logging.getLogger(__name__)
QA_CHAIN: Any = None
RETRIEVER: Any = None


def initialize_qa_engine() -> None:
    """
    Initializes the QA chain and retriever once at application startup.
    """
    global QA_CHAIN, RETRIEVER
    if QA_CHAIN is not None and RETRIEVER is not None:
        return

    QA_CHAIN, RETRIEVER = get_qa_chain()
    logger.info("QA engine initialized")

def get_qa_engine():
    """
    Dependency function used by FastAPI routes to access 
    the pre-loaded AI engine.
    """
    if QA_CHAIN is None or RETRIEVER is None:
        raise HTTPException(
            status_code=503,
            detail="AI engine is still initializing. Please try again shortly."
        )

    return QA_CHAIN, RETRIEVER