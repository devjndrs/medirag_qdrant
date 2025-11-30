from typing import List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from core.config import settings
from retrieval.services import MedicalRetriever, VectorDBConnectionError

class MedicalChatBot:
    """
    Clase principal que orquesta el flujo RAG usando Google Gemini.
    """
    
    def __init__(self, retriever_service: MedicalRetriever):
        # 1. Inyección de Dependencia (DIP)
        self.retriever_service = retriever_service
        
        if not settings.GOOGLE_API_KEY:
            raise ValueError("⚠️ GOOGLE_API_KEY falta en .env")
            
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL_NAME,
            temperature=settings.TEMPERATURE,
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # 1. Prompt para Contextualizar (Query Rewriting)
        # Este prompt reformula la pregunta del usuario usando el historial
        # para que tenga sentido por sí sola (standalone question).
        self.contextualize_q_system_prompt = """Dada una historia de chat y la última pregunta del usuario 
        (que podría hacer referencia al contexto anterior), formula una pregunta independiente 
        que pueda entenderse sin el historial. NO respondas la pregunta, solo reformúlala si es necesario 
        o devuélvela tal cual si ya es explicita."""
        
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", self.contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])
        
        self.history_chain = self.contextualize_q_prompt | self.llm | StrOutputParser()

        # 2. Prompt Principal (QA)
        self.qa_system_prompt = """Eres un asistente médico experto. Usa los siguientes fragmentos de contexto recuperado para responder la pregunta.
        Si no sabes la respuesta, di que no lo sabes. Usa un máximo de tres oraciones y sé conciso.
        
        Contexto:
        {context}
        """
        
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", self.qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"), # Incluimos historia para mantener tono
            ("human", "{question}"),
        ])

    def _format_docs(self, docs) -> str:
        formatted = []
        for i, doc in enumerate(docs):
            content = doc.page_content.replace("\n", " ")
            meta = doc.metadata
            formatted.append(f"[Fuente: {meta.get('source')} (Pág {meta.get('page')})]: {content}")
        return "\n\n".join(formatted)

    def answer(self, query: str, chat_history: List[Tuple[str, str]] = []):
        """
        Args:
            query: Pregunta actual.
            chat_history: Lista de tuplas (Usuario, IA) con la conversación previa.
        """
        # Convertir historial de tuplas a formato LangChain
        lc_history = []
        for human, ai in chat_history:
            lc_history.append(HumanMessage(content=human))
            lc_history.append(AIMessage(content=ai))

        print(f"🤔 Pregunta original: {query}")

        # 1. Reformular pregunta si hay historial
        if lc_history:
            refined_query = self.history_chain.invoke({
                "chat_history": lc_history,
                "question": query
            })
            print(f"🔄 Pregunta reescrita (contextualizada): {refined_query}")
        else:
            refined_query = query

        # 2. Recuperar documentos usando la pregunta REFINADA
        try:
            relevant_docs = self.retriever_service.search(refined_query, k=4)
        except VectorDBConnectionError as e:
            print(f"⚠️ Fallo en recuperación: {e}")
            return "⚠️ Error: No puedo acceder a mi memoria médica en este momento. Por favor verifica que el servicio de Qdrant esté activo.", []
        
        if not relevant_docs:
            return "No encontré información relevante.", []

        # 3. Generar respuesta final
        context_str = self._format_docs(relevant_docs)
        
        qa_chain = self.qa_prompt | self.llm | StrOutputParser()
        
        response = qa_chain.invoke({
            "chat_history": lc_history,
            "context": context_str,
            "question": refined_query # Pasamos la refinada al LLM para que enfoque su respuesta
        })
        
        return response, relevant_docs