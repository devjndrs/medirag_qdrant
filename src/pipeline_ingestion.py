import time
from ingestion.loaders import PDFLoader
from ingestion.splitters import MedicalTextSplitter
from vector_store.store import VectorDBService
import os

def run_pipeline():
    start_time = time.time()
    pdf_path = 'data/raw/sample_medical_paper.pdf'
    if not os.path.exists(pdf_path):
        print('⚠️ Archivo no encontrado. Ejecuta src/test_ingestion.py primero.')
        return
    print('\n--- PASO 1: EXTRACCIÓN ---')
    loader = PDFLoader()
    raw_docs = loader.load(pdf_path)
    print('\n--- PASO 2: TRANSFORMACIÓN (SPLITTING) ---')
    splitter = MedicalTextSplitter()
    chunks = splitter.split_documents(raw_docs)
    print('\n--- PASO 3: CARGA (VECTORIZACIÓN & STORAGE) ---')
    vector_db = VectorDBService()
    vector_db.force_recreate_collection()
    vector_db.upload_documents(chunks)
    end_time = time.time()
    print(f'\n⏱️ Pipeline finalizado en {end_time - start_time:.2f} segundos.')
if __name__ == '__main__':
    run_pipeline()