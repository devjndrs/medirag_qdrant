from typing import List
from qdrant_client import QdrantClient, models
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from core.config import settings
from retrieval.reranking import RerankerService

class VectorDBConnectionError(Exception):
    """Excepción personalizada para fallos de conexión."""
    pass

class MedicalRetriever:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        self.collection = settings.COLLECTION_NAME
        
        # Inicializamos el Reranker (Composición)
        self.reranker = RerankerService()

    def search(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieval en dos etapas:
        1. Vector Search: Recupera candidatos (k * 4) -> Alta Recall.
        2. Reranking: Reordena y corta a k -> Alta Precision.
        """
        try:
            # Pasa 1: Recuperar un pool amplio de candidatos (ej. 20 si k=5)
            fetch_k = k * 4 
            print(f"🔍 Vector Search (Broad): '{query}' buscando {fetch_k} candidatos...")

            query_vector = self.embeddings.embed_query(query)

            # Buscar HIJOS
            search_result = self.client.query_points(
                collection_name=self.collection,
                query=query_vector,
                query_filter=models.Filter(
                    must=[models.FieldCondition(key="type", match=models.MatchValue(value="child"))]
                ),
                limit=fetch_k
            )

            if not search_result.points:
                return []

            # Obtener IDs de PADRES únicos
            parent_ids = set()
            for hit in search_result.points:
                p_id = hit.payload.get("parent_id")
                if p_id:
                    parent_ids.add(p_id)
            
            if not parent_ids:
                return []

            # Recuperar PADRES (Docs completos)
            parent_points = self.client.retrieve(
                collection_name=self.collection,
                ids=list(parent_ids)
            )

            # Convertir a Documentos
            candidate_docs = [
                Document(
                    page_content=point.payload.get("page_content", ""),
                    metadata=point.payload
                )
                for point in parent_points
            ]
            
            print(f"📊 Candidatos únicos recuperados: {len(candidate_docs)}")

            # Paso 2: Reranking (El paso Pro)
            print("⚖️ Ejecutando Reranking...")
            reranked_docs = self.reranker.rerank_documents(query, candidate_docs, top_n=k)
            
            return reranked_docs

        except Exception as e:
            # Capturamos errores de conexión y lanzamos nuestra excepción custom
            # (Tal como definimos en el refactor del Día 7)
            if "Connection refused" in str(e) or "Cannot connect" in str(e):
                print(f"❌ Error crítico de DB: {e}")
                raise VectorDBConnectionError("No se pudo conectar a Qdrant.")
            else:
                print(f"❌ Error inesperado en retrieval: {e}")
                raise e