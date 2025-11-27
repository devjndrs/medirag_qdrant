import os
import logging
from typing import List
from langchain_core.documents import Document
from core.interfces import BaseLoader, BaseCleaner
from ingestion.cleners import MedicalTextCleaner

logger = logging.getLogger(__name__)

class PDFLoader(BaseLoader):
    """
    Implementación concreta para cargar PDFs.
    Usa 'Composition' para incluir la funcionalidad de limpieza.
    """
    
    def __init__(self, cleaner: BaseCleaner = None):
        # Inyección de dependencias: Si no me pasan un cleaner, uso el default.
        self.cleaner = cleaner if cleaner else MedicalTextCleaner()

    def load(self, source_path: str) -> List[Document]:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"El archivo {source_path} no existe.")
            
        logger.info(f"📄 Cargando archivo: {source_path}")
        
        # Usamos pypdf directamente para evitar la carga pesada de langchain_community
        # que trae dependencias como transformers/pytorch innecesariamente aquí.
        logger.info("Importing pypdf...")
        from pypdf import PdfReader
        logger.info("pypdf imported.")

        reader = PdfReader(source_path)
        raw_docs = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Construimos el Documento manualmente
                doc = Document(
                    page_content=text,
                    metadata={"source": source_path, "page": i}
                )
                raw_docs.append(doc)
        
        cleaned_docs = []
        for doc in raw_docs:
            # Aplicamos la limpieza al contenido de la página
            cleaned_content = self.cleaner.clean(doc.page_content)
            
            # Solo guardamos si queda contenido útil
            if len(cleaned_content) > 10:
                # Actualizamos el contenido limpio
                doc.page_content = cleaned_content
                
                # Enriquecemos metadatos (Data Engineering best practice: Lineage)
                doc.metadata["cleaned"] = True
                doc.metadata["original_length"] = len(raw_docs)
                cleaned_docs.append(doc)
                
        logger.info(f"✅ Procesadas {len(cleaned_docs)} páginas limpias de {len(raw_docs)} originales.")
        return cleaned_docs