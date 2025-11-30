🏗️ Fase 1: Infraestructura y Pipeline de Ingestión (Data Engineering)

En la etapa inicial del proyecto, se estableció una base sólida de ingeniería de datos enfocada en la reproducibilidad, escalabilidad y buenas prácticas de diseño de software.

🔧 Stack Tecnológico & Infraestructura

Gestión de Dependencias: Uso de uv (Astral) para un entorno virtual determinista y ultrarrápido, reemplazando herramientas tradicionales para optimizar tiempos de CI/CD.

Vector Database: Despliegue de Qdrant mediante Docker Compose, asegurando persistencia de datos (Volumes) y aislamiento del entorno.

Control de Versiones: Estrategia de Git ignorando artefactos pesados y secretos (.env), siguiendo flujos de trabajo estándar.

⚙️ Pipeline de Extracción (ETL)

Se implementó un módulo de ingestión de datos siguiendo estrictamente los principios SOLID para garantizar mantenibilidad:

Abstracción (Interfaces): Definición de contratos BaseLoader y BaseCleaner (Open/Closed Principle), permitiendo extender el sistema a nuevos formatos (CSV, SQL) sin modificar el código base.

Extracción Optimizada: Implementación de PDFLoader utilizando librerías ligeras (pypdf) para reducir el Cold Start y el consumo de memoria, evitando la sobrecarga de dependencias innecesarias.

Limpieza Modular: Estrategia de limpieza desacoplada (MedicalTextCleaner) inyectada como dependencia (Dependency Injection), facilitando pruebas unitarias y cambios en la lógica de preprocesamiento.

🧠 Fase 2: Transformación, Vectorización y Estrategia de Recuperación

En esta fase se transformó la data cruda en una estructura optimizada para RAG, priorizando la precisión semántica sin sacrificar la riqueza del contexto necesario para el LLM.

🧩 Estrategia de Splitting (Parent-Document Pattern)

Se implementó una arquitectura de datos jerárquica para resolver el compromiso entre precisión de búsqueda y ventana de contexto:

Desacoplamiento Contexto/Índice: Generación de Child Chunks pequeños (optimizados para similitud coseno) vinculados a Parent Chunks grandes (optimizados para comprensión del LLM).

Trazabilidad Relacional: Vinculación mediante UUIDs y metadatos (parent_id) para asegurar la integridad referencial entre índices de búsqueda y almacenamiento de contenido.

💾 Vectorización y Almacenamiento (Batching)

Embeddings Locales: Integración de sentence-transformers (all-MiniLM-L6-v2) para inferencia local rápida, eliminando costes de API para la vectorización.

Ingestión por Lotes: Implementación de carga masiva (batch_size=64) en Qdrant para minimizar la latencia de red y optimizar el throughput de escritura (I/O).

Idempotencia: Lógica de Upsert basada en IDs deterministas para permitir re-ejecuciones del pipeline sin generar duplicados.

🔍 Recuperación Avanzada (Retrieval)

Query Optimization: Uso de Filter Push-down en Qdrant para restringir la búsqueda vectorial estrictamente a los fragmentos "hijos".

Reconstrucción de Contexto: Lógica de recuperación en dos pasos: Búsqueda Vectorial Aproximada (ANN) $\to$ Recuperación de Puntos por ID (Lookup O(1)) para entregar el documento padre completo al modelo generativo.

🧠 Fase 3: Orquestación Inteligente y Optimización (RAG Avanzado)

Se evolucionó el sistema de un simple buscador a un asistente conversacional con memoria y capacidad de razonamiento refinada.

🤖 Generación y Memoria (LLM Integration)

Integración de Gemini 1.5: Implementación del modelo gemini-1.5-flash vía langchain-google-genai para la síntesis de respuestas, aprovechando su baja latencia y amplia ventana de contexto.

Gestión de Historial (Conversational Memory): Desarrollo de un sistema de memoria de ventana deslizante ("Sliding Window") manual.

Query Rewriting: Implementación de un paso intermedio donde el LLM reformula la pregunta del usuario basándose en el historial del chat (ej. transformar "¿Y cuáles son sus riesgos?" a "¿Cuáles son los riesgos del iDML?") antes de consultar la base vectorial.

⚖️ Reranking (Precisión Semántica)

Se añadió una segunda etapa de filtrado para resolver las limitaciones de la búsqueda por similitud coseno (Bi-Encoders):

Arquitectura Two-Stage Retrieval:

Wide Fetch: Qdrant recupera ~20 candidatos basándose en similitud vectorial aproximada.

Deep Rerank: FlashRank (Cross-Encoder ligero corriendo en CPU) reordena los candidatos analizando la interacción profunda entre la pregunta y cada documento.

Resultado: Mejora drástica en la relevancia de los documentos enviados al LLM, descartando "falsos positivos" que se parecen vectorialmente pero no semánticamente.

🛡️ Robustez y Patrones de Diseño

Refactorización SOLID: Aplicación de Dependency Injection en el constructor del chatbot para desacoplar el servicio de recuperación.

Manejo de Fallos (Graceful Degradation): Implementación de bloques try-except personalizados y excepciones VectorDBConnectionError para garantizar que el bot informe problemas de infraestructura amigablemente en lugar de colapsar.