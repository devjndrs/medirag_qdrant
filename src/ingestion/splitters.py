import uuid
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class MedicalTextSplitter:
    """
    Se encarga de dividir los documentos en fragmentos (chunks) optimizados para RAG.
    Implementa la estrategia Parent-Document:
    - Divide en chunks grandes (Parent) para contexto.
    - Divide los Parents en chunks pequeños (Child) para búsqueda vectorial precisa.
    """
    
    def __init__(self, parent_chunk_size=2000, child_chunk_size=400):
        # Configuración para chunks grandes (Contexto)
        self.parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_chunk_size,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
        # Configuración para chunks pequeños (Búsqueda Vectorial)
        self.child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_chunk_size,
            chunk_overlap=50
        )

    def split_documents(self, docs: List[Document]) -> List[Document]:
        """
        Recibe documentos completos (páginas) y devuelve una lista plana de Chunks
        (tanto padres como hijos) listos para la BD.
        """
        all_chunks = []
        
        print("🔪 Iniciando proceso de Splitting (Parent-Child)...")
        
        for doc in docs:
            # 1. Crear Parent Chunks (Bloques grandes de contexto)
            parent_chunks = self.parent_splitter.split_documents([doc])
            
            for parent in parent_chunks:
                # Generar un ID único para el padre
                parent_id = str(uuid.uuid4())
                parent.metadata["doc_id"] = parent_id
                parent.metadata["type"] = "parent"
                
                # Añadir el padre a la lista final
                all_chunks.append(parent)
                
                # 2. Crear Child Chunks (Bloques pequeños derivados del padre)
                child_chunks = self.child_splitter.split_documents([parent])
                
                for child in child_chunks:
                    # El hijo apunta al padre via 'parent_id'
                    child.metadata["parent_id"] = parent_id
                    child.metadata["type"] = "child"
                    # Hereda metadatos originales (fuente, página, etc.)
                    
                    all_chunks.append(child)
        
        print(f"🧩 Splitting completado. Generados {len(all_chunks)} chunks totales.")
        return all_chunks