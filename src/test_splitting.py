from ingestion.loders import PDFLoader
from ingestion.splitters import MedicalTextSplitter
import os

def main():
    # 1. Cargar el PDF (reusando tu código optimizado)
    pdf_path = "data/raw/sample_medical_paper.pdf"
    if not os.path.exists(pdf_path):
        print("⚠️ Primero ejecuta el script del Día 2 para descargar el PDF.")
        return

    loader = PDFLoader()
    raw_docs = loader.load(pdf_path)
    
    # 2. Inicializar Splitter
    splitter = MedicalTextSplitter(parent_chunk_size=1000, child_chunk_size=200)
    
    # 3. Ejecutar Splitting
    chunks = splitter.split_documents(raw_docs)
    
    # 4. Análisis de Resultados (Data Engineering Check)
    parents = [d for d in chunks if d.metadata["type"] == "parent"]
    children = [d for d in chunks if d.metadata["type"] == "child"]
    
    print("\n--- 📊 Reporte de Estructura de Datos ---")
    print(f"Total Chunks: {len(chunks)}")
    print(f"Parents (Contexto): {len(parents)}")
    print(f"Children (Búsqueda): {len(children)}")
    print(f"Ratio Promedio: {len(children)/len(parents):.1f} hijos por padre")
    
    print("\n--- 🕵️ Inspección de Relación ---")
    # Tomamos el primer hijo y buscamos a su padre
    sample_child = children[0]
    parent_id = sample_child.metadata["parent_id"]
    
    # Buscar el padre en la lista
    found_parent = next((p for p in parents if p.metadata["doc_id"] == parent_id), None)
    
    print(f"Child Chunk (ID Padre: {parent_id}):")
    print(f"Texto: '{sample_child.page_content[:100]}...'")
    print("-" * 20)
    
    if found_parent:
        print(f"✅ Parent Chunk Encontrado (ID: {found_parent.metadata['doc_id']}):")
        print(f"Texto: '{found_parent.page_content[:100]}...'")
        
        # Verificación de integridad
        if sample_child.page_content in found_parent.page_content:
            print("✅ INTEGRIDAD OK: El texto del hijo está contenido en el padre.")
        else:
            print("⚠️ WARNING: El texto del hijo no coincide exactamente (puede ser por limpieza).")
    else:
        print("❌ ERROR: Padre no encontrado.")

if __name__ == "__main__":
    main()