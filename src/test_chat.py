from generation.rag_chain import MedicalChatBot
from retrieval.services import MedicalRetriever
import time

def main():
    print("🏥 Iniciando MediRAG AI (con Memoria)...")
    try:
        # 1. Instanciar dependencias (DIP)
        retriever = MedicalRetriever()
        
        # 2. Inyectar dependencias
        bot = MedicalChatBot(retriever_service=retriever)
        
        # Inicializamos la memoria local
        chat_history = [] 
        print("✅ Sistema listo. Escribe 'salir' para terminar o 'borrar' para limpiar memoria.\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    while True:
        query = input("\n🧑‍⚕️ Tú: ")
        
        if query.lower() in ["salir", "exit"]:
            break
        if query.lower() == "borrar":
            chat_history = []
            print("🧹 Memoria borrada.")
            continue
            
        # Generar respuesta pasando el historial
        try:
            answer, sources = bot.answer(query, chat_history)
            
            print(f"\n🤖 MediRAG:\n{answer}")
            
            # Actualizar historial (Usuario, IA)
            chat_history.append((query, answer))
            
            # Mantener solo los últimos 3 pares para no saturar el contexto (Sliding Window)
            if len(chat_history) > 3:
                chat_history.pop(0)
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()