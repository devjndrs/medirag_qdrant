from retrieval.services import MedicalRetriever

def main():
    # Instanciar el servicio
    retriever = MedicalRetriever()
    
    # Pregunta de prueba (basada en el paper iDML que descargamos)
    # El paper habla de "decentralized machine learning". Probemos eso.
    query = "How does decentralized machine learning work?"
    
    print("\n--- 🧪 TEST DE RETRIEVAL (Parent-Document) ---")
    results = retriever.search(query, k=4)
    
    print(f"\n✅ Resultados recuperados: {len(results)}\n")
    
    for i, doc in enumerate(results):
        print(f"📄 DOCUMENTO {i+1} (ID Padre: {doc.metadata.get('doc_id')})")
        print(f"Tipo: {doc.metadata.get('type')}")
        print("-" * 40)
        # Mostramos los primeros 300 caracteres para verificar que es el bloque grande
        print(doc.page_content[:300] + "...") 
        print(f"\n[Longitud total del texto: {len(doc.page_content)} caracteres]")
        print("=" * 60)

if __name__ == "__main__":
    main()