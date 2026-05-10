flowchart LR
  subgraph A[Presentation Layer]
    C[Client: Web, Mobile, Postman]
    SW[Swagger UI]
  end

  subgraph B[API Layer]
    APP[FastAPI App]
    ASK[/POST /api/v1/ask/]
    DEP[Dependency: preloaded chain + retriever]
  end

  subgraph C1[Application Layer]
    CHAIN[RAG Chain]
    PROMPT[Prompt Template]
    SCHEMA[Request/Response Schemas]
  end

  subgraph D[Service Layer]
    LLM[LLM Service\nOpenAI or Gemini]
    VEC[VectorDB Service\nEmbeddings + Chroma access]
    CFG[Config Service\nENV + provider paths]
  end

  subgraph E[Data and External]
    CHROMA[(Chroma Vector DB)]
    POLICIES[(HR Policy Markdown Files)]
    OAI[(OpenAI API)]
    GEM[(Gemini API)]
  end

  subgraph F[Offline Ingestion]
    ING[Ingest Script]
    SPLIT[Chunking]
    EMBED[Embedding]
    SAVE[Persist to Chroma]
  end

  C --> APP --> ASK
  SW --> APP
  ASK --> SCHEMA
  ASK --> DEP --> CHAIN
  CHAIN --> PROMPT
  CHAIN --> VEC --> CHROMA
  CHAIN --> LLM
  LLM --> OAI
  LLM --> GEM
  LLM --> CFG
  VEC --> CFG

  POLICIES --> ING --> SPLIT --> EMBED --> SAVE --> CHROMA
  CFG --> EMBED

  classDef api fill:#eaf4ff,stroke:#1f5aa6,stroke-width:1px;
  classDef app fill:#eefaf0,stroke:#2e7d32,stroke-width:1px;
  classDef data fill:#fff9e8,stroke:#9a6b00,stroke-width:1px;
  class APP,ASK,DEP api;
  class CHAIN,PROMPT,SCHEMA,LLM,VEC,CFG app;
  class CHROMA,POLICIES,OAI,GEM data;
