# AskHR Production API 🏢🤖

A production-ready Retrieval-Augmented Generation (RAG) API built with FastAPI and LangChain. This application acts as a professional HR assistant, answering employee questions based purely on your company's internal policy documents.

## ✨ Features
- **Multi-LLM Support**: Seamlessly toggle between OpenAI (`gpt-4o`) and Google Gemini (`gemini-2.5-flash`).
- **Local Vector Database**: Uses ChromaDB to securely store and retrieve document embeddings locally.
- **Asynchronous & Fast**: Built on FastAPI with asynchronous LangChain (`ainvoke`) execution so your API never blocks.
- **Docker-Ready**: Includes a production-ready `Dockerfile` and `docker-compose.yml` for easy containerized deployment.
- **Interactive Docs**: Automatic Swagger UI documentation for easy API testing.

## 📋 Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional, for containerized running)
- Valid API Keys (OpenAI and/or Google Gemini)

## ⚙️ Setup & Installation

1. **Clone the repository and navigate to the directory:**
   ```bash
   cd ask-hr-api-rag
   ```

2. **Create your `.env` file:**
   Create a `.env` file in the root of the project with the following variables. You only need to provide the API key for the provider you plan to use.
   ```env
   # Choose your provider: "gemini" or "openai"
   LLM_PROVIDER=gemini

   # Provide your API keys
   GOOGLE_API_KEY="your_google_api_key_here"
   OPENAI_API_KEY="your_openai_api_key_here"
   ```

3. **Install Dependencies (Local Development):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## 📚 Data Ingestion (Building the Database)

Before starting the API, you need to populate the vector database with your HR policies.

1. Place your policy documents (as `.md` Markdown files) inside the `./data/policies` folder.
2. Run the ingestion script:
   ```bash
   export PYTHONPATH=.
   python scripts/ingest.py
   ```

*Note: The script dynamically reads your `LLM_PROVIDER` environment variable and saves the database to either `./data/chroma_db_gemini` or `./data/chroma_db_openai`. This prevents dimension mismatch errors when switching between models.*

## 🚀 Running the API

### Option 1: Using Docker Compose (Recommended)
```bash
docker-compose up --build
```
This will start the API on `http://localhost:8000` and mount your local `./data` folder so the vector database persists.

### Option 2: Running Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 💬 API Usage

Once the server is running, you can test the HR Assistant by sending a `POST` request to the `/ask` endpoint.

**Endpoint:** `POST /api/v1/ask`

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the company policy on international travel?"}'
```

**Response Example:**
```json
{
  "answer": "According to the company policy, employees traveling internationally must submit their requests at least 30 days in advance...",
  "sources": [
    "travel_policy.md"
  ],
  "model_used": "gemini"
}
```

### API Documentation
You can view and interact with the automatically generated Swagger UI documentation by visiting `http://localhost:8000/docs` in your browser.