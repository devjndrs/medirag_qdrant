import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from src.core.interfaces import BaseLoader, BaseCleaner
from src.ingestion.cleaners import MedicalTextCleaner

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
            
        print(f"📄 Cargando archivo: {source_path}")
        
        # Usamos PyPDFLoader de Langchain (que usa pypdf por debajo)
        loader = PyPDFLoader(source_path)
        raw_docs = loader.load()
        
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
                
        print(f"✅ Procesadas {len(cleaned_docs)} páginas limpias de {len(raw_docs)} originales.")
        return cleaned_docs