from typing import List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from core.config import settings
from retrieval.services import MedicalRetriever, VectorDBConnectionError

class MedicalChatBot:

    def __init__(self, retriever_service: MedicalRetriever):
        self.retriever_service = retriever_service
        if not settings.GOOGLE_API_KEY:
            raise ValueError('⚠️ GOOGLE_API_KEY falta en .env')
        self.llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL_NAME, temperature=settings.TEMPERATURE, google_api_key=settings.GOOGLE_API_KEY)
        self.contextualize_q_system_prompt = 'Dada una historia de chat y la última pregunta del usuario \n        (que podría hacer referencia al contexto anterior), formula una pregunta independiente \n        que pueda entenderse sin el historial. NO respondas la pregunta, solo reformúlala si es necesario \n        o devuélvela tal cual si ya es explicita.'
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages([('system', self.contextualize_q_system_prompt), MessagesPlaceholder(variable_name='chat_history'), ('human', '{question}')])
        self.history_chain = self.contextualize_q_prompt | self.llm | StrOutputParser()
        self.qa_system_prompt = 'Eres un asistente médico experto. Usa los siguientes fragmentos de contexto recuperado para responder la pregunta.\n        Si no sabes la respuesta, di que no lo sabes. Usa un máximo de tres oraciones y sé conciso.\n        \n        Contexto:\n        {context}\n        '
        self.qa_prompt = ChatPromptTemplate.from_messages([('system', self.qa_system_prompt), MessagesPlaceholder(variable_name='chat_history'), ('human', '{question}')])

    def _format_docs(self, docs) -> str:
        formatted = []
        for i, doc in enumerate(docs):
            content = doc.page_content.replace('\n', ' ')
            meta = doc.metadata
            formatted.append(f'[Fuente: {meta.get('source')} (Pág {meta.get('page')})]: {content}')
        return '\n\n'.join(formatted)

    def answer(self, query: str, chat_history: List[Tuple[str, str]]=[]):
        lc_history = []
        for human, ai in chat_history:
            lc_history.append(HumanMessage(content=human))
            lc_history.append(AIMessage(content=ai))
        print(f'🤔 Pregunta original: {query}')
        if lc_history:
            refined_query = self.history_chain.invoke({'chat_history': lc_history, 'question': query})
            print(f'🔄 Pregunta reescrita (contextualizada): {refined_query}')
        else:
            refined_query = query
        try:
            relevant_docs = self.retriever_service.search(refined_query, k=4)
        except VectorDBConnectionError as e:
            print(f'⚠️ Fallo en recuperación: {e}')
            return ('⚠️ Error: No puedo acceder a mi memoria médica en este momento. Por favor verifica que el servicio de Qdrant esté activo.', [])
        if not relevant_docs:
            return ('No encontré información relevante.', [])
        context_str = self._format_docs(relevant_docs)
        qa_chain = self.qa_prompt | self.llm | StrOutputParser()
        response = qa_chain.invoke({'chat_history': lc_history, 'context': context_str, 'question': refined_query})
        return (response, relevant_docs)