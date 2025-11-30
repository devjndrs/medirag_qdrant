import sys
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

def check_connection():
    print(f'Versión de Python: {sys.version}')
    try:
        client = QdrantClient(url='http://localhost:6333')
        collection_name = 'test_collection'
        if not client.collection_exists(collection_name):
            client.create_collection(collection_name=collection_name, vectors_config=VectorParams(size=4, distance=Distance.DOT))
            print('✅ Conexión con Qdrant exitosa y colección creada.')
        else:
            print('✅ Conexión con Qdrant exitosa (la colección ya existía).')
    except Exception as e:
        print(f'❌ Error conectando a Qdrant: {e}')
if __name__ == '__main__':
    check_connection()