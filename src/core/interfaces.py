from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.documents import Document

class BaseLoader(ABC):

    @abstractmethod
    def load(self, source_path: str) -> List[Document]:
        pass

class BaseCleaner(ABC):

    @abstractmethod
    def clean(self, text: str) -> str:
        pass