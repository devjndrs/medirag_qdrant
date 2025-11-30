from generation.rag_chain import MedicalChatBot
from retrieval.services import MedicalRetriever
import time

def main():
    print('🏥 Iniciando MediRAG AI (con Memoria)...')
    try:
        retriever = MedicalRetriever()
        bot = MedicalChatBot(retriever_service=retriever)
        chat_history = []
        print("✅ Sistema listo. Escribe 'salir' para terminar o 'borrar' para limpiar memoria.\n")
    except Exception as e:
        print(f'❌ Error: {e}')
        return
    while True:
        query = input('\n🧑\u200d⚕️ Tú: ')
        if query.lower() in ['salir', 'exit']:
            break
        if query.lower() == 'borrar':
            chat_history = []
            print('🧹 Memoria borrada.')
            continue
        try:
            answer, sources = bot.answer(query, chat_history)
            print(f'\n🤖 MediRAG:\n{answer}')
            chat_history.append((query, answer))
            if len(chat_history) > 3:
                chat_history.pop(0)
        except Exception as e:
            print(f'❌ Error: {e}')
if __name__ == '__main__':
    main()