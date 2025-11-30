import os
import urllib.request
import logging
import time
from ingestion.loaders import PDFLoader
from ingestion.cleaners import MedicalTextCleaner
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

def download_sample_paper():
    url = 'https://arxiv.org/pdf/2304.05354.pdf'
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/sample_medical_paper.pdf'
    if not os.path.exists(file_path):
        logger.info('⬇️ Descargando paper de muestra de Arxiv...')
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, file_path)
        logger.info('Descarga completada.')
    else:
        logger.info(f'El archivo ya existe: {file_path}')
    return file_path

def main():
    start_total = time.time()
    logger.info('Iniciando script de prueba de ingestión...')
    pdf_path = download_sample_paper()
    logger.info('Instanciando componentes...')
    cleaner = MedicalTextCleaner()
    loader = PDFLoader(cleaner=cleaner)
    logger.info('Ejecutando pipeline de carga...')
    start_load = time.time()
    docs = loader.load(pdf_path)
    end_load = time.time()
    logger.info(f'Carga y limpieza completada en {end_load - start_load:.2f} segundos.')
    logger.info('\n--- Muestra del contenido limpio (Página 1) ---')
    if docs:
        print(docs[0].page_content[:500] + '...')
        logger.info('\n--- Metadatos ---')
        print(docs[0].metadata)
    else:
        logger.warning('No se obtuvieron documentos.')
    end_total = time.time()
    logger.info(f'Ejecución total finalizada en {end_total - start_total:.2f} segundos.')
if __name__ == '__main__':
    main()