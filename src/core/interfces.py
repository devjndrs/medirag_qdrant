from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.documents import Document

class BaseLoader(ABC):
    """
    Interface (Contrato) para cualquier cargador de documentos.
    Si mañana quieres cargar CSVs, creas una clase que herede de esta
    sin romper el código existente.
    """
    
    @abstractmethod
    def load(self, source_path: str) -> List[Document]:
        """Carga documentos desde una fuente y devuelve una lista de Documents de LangChain."""
        pass

class BaseCleaner(ABC):
    """
    Interface para estrategias de limpieza de texto.
    """
    @abstractmethod
    def clean(self, text: str) -> str:
        pass