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
        
        # Inicializar modelo de embeddings local (se descarga la primera vez)
        print(f"🧠 Cargando modelo de embeddings: {settings.EMBEDDING_MODEL_NAME}...")
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Verifica si la colección existe, si no, la crea optimizada."""
        if not self.client.collection_exists(self.collection_name):
            print(f"🔨 Creando colección '{self.collection_name}' en Qdrant...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=settings.VECTOR_SIZE,
                    distance=models.Distance.COSINE
                )
            )

    def force_recreate_collection(self):
        """Borra y recrea la colección para limpiar datos corruptos."""
        print(f"🧨 Borrando colección '{self.collection_name}'...")
        self.client.delete_collection(self.collection_name)
        self._ensure_collection_exists()

    def upload_documents(self, docs: List[Document], batch_size=64):
        """
        Genera embeddings y sube documentos a Qdrant en lotes (Batching).
        Data Engineering: El batching reduce drásticamente la latencia de red.
        """
        total_docs = len(docs)
        print(f"🚀 Iniciando carga de {total_docs} documentos a Qdrant...")
        
        for i in range(0, total_docs, batch_size):
            batch = docs[i : i + batch_size]
            
            # 1. Extraer textos y metadatos
            texts = [d.page_content for d in batch]
            metadatas = [d.metadata for d in batch]
            
            # Añadir el texto al payload para poder recuperarlo después
            for j, meta in enumerate(metadatas):
                meta["page_content"] = texts[j]
            
            # 2. Generar Embeddings (Vectorización)
            # HuggingFace procesa listas de textos eficientemente
            vectors = self.embeddings.embed_documents(texts)
            
            # 3. Preparar puntos para Qdrant
            points = [
                models.PointStruct(
                    id=str(meta.get("doc_id")),  # ID único garantizado por el splitter
                    vector=vector,
                    payload=meta
                )
                for j, (vector, meta) in enumerate(zip(vectors, metadatas))
            ]
            
            # 4. Subir lote (Upsert)
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"   ✅ Lote {i // batch_size + 1} subido ({len(batch)} docs).")
            
        print("🎉 Ingestión completada exitosamente.")