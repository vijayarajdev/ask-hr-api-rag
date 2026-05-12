import shutil
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from app.core.config import settings
from app.services.vectordb import get_embeddings

def build_database():
    embeddings = get_embeddings()
    db_path = settings.CHROMA_PATH

    print("Reading Markdown files...")
    # Read all .md files in the data/policies folder
    loader = DirectoryLoader("./data/policies", glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    documents = loader.load()
    
    if not documents:
        print(" Error: No markdown files found in ./data/policies/")
        return

    print(f"Splitting {len(documents)} documents into smaller chunks...")
    # Break long documents into smaller pieces so the AI can read them easily
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    db_dir = Path(db_path)
    if db_dir.exists():
        print(f"Existing database found at {db_path}. Rebuilding for idempotent ingest...")
        shutil.rmtree(db_dir)
    
    print(f"Saving to database at {db_path}...") 
    # This creates your local database folder
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    
    print(f"Success! Your database is built. Saved {len(chunks)} chunks to {db_path}.")

if __name__ == "__main__":
    build_database()