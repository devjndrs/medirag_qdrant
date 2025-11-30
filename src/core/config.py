import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Qdrant
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    COLLECTION_NAME = "medirag_knowledge"
    
    # Embeddings (Seguimos usando HuggingFace local para ahorrar costos y latencia)
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    VECTOR_SIZE = 384
    
    # LLM (Gemini Configuration)
    # Necesitas obtener tu API Key en: https://aistudio.google.com/app/apikey
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # 'gemini-1.5-flash' es ideal para RAG (rápido y barato). 
    # Usa 'gemini-1.5-pro' si necesitas razonamiento muy complejo.
    LLM_MODEL_NAME = "gemini-2.5-pro" 
    TEMPERATURE = 0.0

settings = Settings()