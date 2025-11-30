from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from core.config import settings

class VectorDBService:

    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = settings.COLLECTION_NAME
        print(f'🧠 Cargando modelo de embeddings: {settings.EMBEDDING_MODEL_NAME}...')
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        if not self.client.collection_exists(self.collection_name):
            print(f"🔨 Creando colección '{self.collection_name}' en Qdrant...")
            self.client.create_collection(collection_name=self.collection_name, vectors_config=models.VectorParams(size=settings.VECTOR_SIZE, distance=models.Distance.COSINE))

    def force_recreate_collection(self):
        print(f"🧨 Borrando colección '{self.collection_name}'...")
        self.client.delete_collection(self.collection_name)
        self._ensure_collection_exists()

    def upload_documents(self, docs: List[Document], batch_size=64):
        total_docs = len(docs)
        print(f'🚀 Iniciando carga de {total_docs} documentos a Qdrant...')
        for i in range(0, total_docs, batch_size):
            batch = docs[i:i + batch_size]
            texts = [d.page_content for d in batch]
            metadatas = [d.metadata for d in batch]
            for j, meta in enumerate(metadatas):
                meta['page_content'] = texts[j]
            vectors = self.embeddings.embed_documents(texts)
            points = [models.PointStruct(id=str(meta.get('doc_id')), vector=vector, payload=meta) for j, (vector, meta) in enumerate(zip(vectors, metadatas))]
            self.client.upsert(collection_name=self.collection_name, points=points)
            print(f'   ✅ Lote {i // batch_size + 1} subido ({len(batch)} docs).')
        print('🎉 Ingestión completada exitosamente.')