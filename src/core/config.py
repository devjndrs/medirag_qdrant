import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
    COLLECTION_NAME = 'medirag_knowledge'
    EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
    VECTOR_SIZE = 384
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    LLM_MODEL_NAME = 'gemini-2.5-pro'
    TEMPERATURE = 0.0
settings = Settings()