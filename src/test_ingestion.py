import os
import urllib.request
from src.ingestion.loaders import PDFLoader
from src.ingestion.cleaners import MedicalTextCleaner

def download_sample_paper():
    """Descarga un paper médico de muestra si no existe."""
    # Paper sobre "AI in Medicine" de Arxiv
    url = "https://arxiv.org/pdf/2304.05354.pdf" 
    os.makedirs("data/raw", exist_ok=True)
    file_path = "data/raw/sample_medical_paper.pdf"
    
    if not os.path.exists(file_path):
        print("⬇️ Descargando paper de muestra de Arxiv...")
        # Headers necesarios para que Arxiv no rechace la petición
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_path)
    
    return file_path

def main():
    # 1. Obtener datos
    pdf_path = download_sample_paper()
    
    # 2. Instanciar componentes (Dependency Injection manual)
    # Podemos cambiar MedicalTextCleaner por otra estrategia sin romper PDFLoader
    cleaner = MedicalTextCleaner()
    loader = PDFLoader(cleaner=cleaner)
    
    # 3. Ejecutar pipeline de carga
    docs = loader.load(pdf_path)
    
    # 4. Inspeccionar resultados (Sampling)
    print("\n--- Muestra del contenido limpio (Página 1) ---")
    print(docs[0].page_content[:500] + "...")
    print("\n--- Metadatos ---")
    print(docs[0].metadata)

if __name__ == "__main__":
    main()