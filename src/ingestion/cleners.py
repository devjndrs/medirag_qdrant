import re
from src.core.interfaces import BaseCleaner

class MedicalTextCleaner(BaseCleaner):
    """
    Estrategia concreta para limpiar textos médicos.
    Elimina referencias, espacios extraños y encabezados repetitivos.
    """
    
    def clean(self, text: str) -> str:
        # 1. Normalizar espacios (eliminar saltos de línea múltiples y tabulaciones)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 2. Eliminar patrones comunes de referencias bibliográficas tipo [1], [12]
        # Esto reduce "ruido" para el modelo de embeddings.
        text = re.sub(r'\[\d+\]', '', text)
        
        # 3. Eliminar URLs (opcional, depende si quieres mantener enlaces)
        text = re.sub(r'http\S+', '', text)
        
        # 4. Eliminar caracteres no imprimibles o basura común en PDFs
        text = text.replace('•', '')
        
        return text