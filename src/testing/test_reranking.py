from retrieval.services import MedicalRetriever

def main():
    try:
        retriever = MedicalRetriever()
        query = 'roles in decentralized learning'
        print('\n--- 🧪 TEST DE RETRIEVAL CON RERANKING ---')
        results = retriever.search(query, k=3)
        print(f'\n🏆 Top 3 Documentos Finales:\n')
        for i, doc in enumerate(results):
            score = doc.metadata.get('rerank_score', 0)
            doc_id = doc.metadata.get('doc_id')
            print(f'🥇 Rango #{i + 1} | Score de Relevancia: {score:.4f}')
            print(f'   ID: {doc_id}')
            print(f'   Snippet: {doc.page_content[:150]}...')
            print('-' * 50)
    except Exception as e:
        print(f'Error: {e}')
if __name__ == '__main__':
    main()