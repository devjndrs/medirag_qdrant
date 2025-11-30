from typing import List
from langchain_core.documents import Document
from flashrank import Ranker, RerankRequest

class RerankerService:
    """
    Servicio encargado de reordenar documentos basándose en relevancia semántica profunda.
    Usa FlashRank (Cross-Encoder ligero) optimizado para CPU.
    """
    
    def __init__(self, model_name="ms-marco-MiniLM-L-12-v2"):
        print(f"⚖️ Inicializando Reranker ({model_name})...")
        # FlashRank descarga el modelo automáticamente y lo cachea.
        self.ranker = Ranker(model_name=model_name, cache_dir="models")

    def rerank_documents(self, query: str, docs: List[Document], top_n: int = 5) -> List[Document]:
        """
        Recibe una lista amplia de candidatos (ej. 20) y devuelve los mejores N (ej. 5).
        """
        if not docs:
            return []

        # 1. Convertir formato LangChain a formato FlashRank (Lista de diccionarios)
        passages = [
            {"id": d.metadata.get("doc_id", str(i)), "text": d.page_content, "meta": d.metadata} 
            for i, d in enumerate(docs)
        ]

        # 2. Crear Request de Reranking
        rerank_request = RerankRequest(query=query, passages=passages)
        
        # 3. Ejecutar Reranking
        results = self.ranker.rerank(rerank_request)
        
        # 4. Filtrar y Reconstruir Documentos LangChain
        # FlashRank devuelve los resultados ya ordenados por score.
        final_docs = []
        for res in results[:top_n]:
            # Recuperamos la metadata original
            original_meta = res["meta"]
            # Añadimos el score de relevancia calculado por el reranker (útil para debug)
            original_meta["rerank_score"] = res["score"]
            
            doc = Document(
                page_content=res["text"],
                metadata=original_meta
            )
            final_docs.append(doc)
            
        return final_docs