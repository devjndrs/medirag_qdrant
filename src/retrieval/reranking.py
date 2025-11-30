from typing import List
from langchain_core.documents import Document
from flashrank import Ranker, RerankRequest

class RerankerService:

    def __init__(self, model_name='ms-marco-MiniLM-L-12-v2'):
        print(f'⚖️ Inicializando Reranker ({model_name})...')
        self.ranker = Ranker(model_name=model_name, cache_dir='models')

    def rerank_documents(self, query: str, docs: List[Document], top_n: int=5) -> List[Document]:
        if not docs:
            return []
        passages = [{'id': d.metadata.get('doc_id', str(i)), 'text': d.page_content, 'meta': d.metadata} for i, d in enumerate(docs)]
        rerank_request = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerank_request)
        final_docs = []
        for res in results[:top_n]:
            original_meta = res['meta']
            original_meta['rerank_score'] = res['score']
            doc = Document(page_content=res['text'], metadata=original_meta)
            final_docs.append(doc)
        return final_docs