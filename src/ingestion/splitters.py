import uuid
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class MedicalTextSplitter:

    def __init__(self, parent_chunk_size=2000, child_chunk_size=400):
        self.parent_splitter = RecursiveCharacterTextSplitter(chunk_size=parent_chunk_size, chunk_overlap=200, separators=['\n\n', '\n', '.', ' ', ''])
        self.child_splitter = RecursiveCharacterTextSplitter(chunk_size=child_chunk_size, chunk_overlap=50)

    def split_documents(self, docs: List[Document]) -> List[Document]:
        all_chunks = []
        print('🔪 Iniciando proceso de Splitting (Parent-Child)...')
        for doc in docs:
            parent_chunks = self.parent_splitter.split_documents([doc])
            for parent in parent_chunks:
                parent_id = str(uuid.uuid4())
                parent.metadata['doc_id'] = parent_id
                parent.metadata['type'] = 'parent'
                all_chunks.append(parent)
                child_chunks = self.child_splitter.split_documents([parent])
                for child in child_chunks:
                    child.metadata['parent_id'] = parent_id
                    child.metadata['doc_id'] = str(uuid.uuid4())
                    child.metadata['type'] = 'child'
                    all_chunks.append(child)
        print(f'🧩 Splitting completado. Generados {len(all_chunks)} chunks totales.')
        return all_chunks