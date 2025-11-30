import time
from ingestion.loaders import PDFLoader
from ingestion.splitters import MedicalTextSplitter
from vector_store.store import VectorDBService
import os

def run_pipeline():
    start_time = time.time()
    
    # 1. Definir fuente de datos
    pdf_path = "data/raw/sample_medical_paper.pdf"
    if not os.path.exists(pdf_path):
        print("⚠️ Archivo no encontrado. Ejecuta src/test_ingestion.py primero.")
        return

    # 2. Extracción (Load)
    print("\n--- PASO 1: EXTRACCIÓN ---")
    loader = PDFLoader()
    raw_docs = loader.load(pdf_path)
    
    # 3. Transformación (Split)
    print("\n--- PASO 2: TRANSFORMACIÓN (SPLITTING) ---")
    splitter = MedicalTextSplitter()
    chunks = splitter.split_documents(raw_docs)
    
    # 4. Carga (Load to Vector DB)
    print("\n--- PASO 3: CARGA (VECTORIZACIÓN & STORAGE) ---")
    vector_db = VectorDBService()
    
    # Filtramos: ¿Queremos indexar padres e hijos? 
    # Estrategia Híbrida: Indexamos ambos.
    # - Hijos: Para búsqueda semántica precisa.
    # - Padres: Para tener el contexto completo disponible si el match es muy bueno.
    vector_db.force_recreate_collection()
    vector_db.upload_documents(chunks)
    
    end_time = time.time()
    print(f"\n⏱️ Pipeline finalizado en {end_time - start_time:.2f} segundos.")

if __name__ == "__main__":
    run_pipeline()