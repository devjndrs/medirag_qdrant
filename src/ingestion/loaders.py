import os
import logging
import pypdf
from typing import List
from langchain_core.documents import Document
from core.interfaces import BaseLoader, BaseCleaner
from ingestion.cleaners import MedicalTextCleaner
logger = logging.getLogger(__name__)

class PDFLoader(BaseLoader):

    def __init__(self, cleaner: BaseCleaner=None):
        self.cleaner = cleaner if cleaner else MedicalTextCleaner()

    def load(self, source_path: str) -> List[Document]:
        if not os.path.exists(source_path):
            raise FileNotFoundError(f'El archivo {source_path} no existe.')
        print(f'📄 Cargando archivo (Lightweight): {source_path}')
        docs = []
        try:
            reader = pypdf.PdfReader(source_path)
            for i, page in enumerate(reader.pages):
                raw_text = page.extract_text() or ''
                cleaned_text = self.cleaner.clean(raw_text)
                if len(cleaned_text) > 50:
                    doc = Document(page_content=cleaned_text, metadata={'source': source_path, 'page': i + 1, 'cleaned': True, 'char_count': len(cleaned_text)})
                    docs.append(doc)
            print(f'✅ Procesadas {len(docs)} páginas útiles de {len(reader.pages)} totales.')
            return docs
        except Exception as e:
            print(f'❌ Error leyendo PDF: {e}')
            return []