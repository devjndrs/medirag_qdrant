# 🩺 MediRAG: Advanced Medical RAG System

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red?style=for-the-badge&logo=qdrant&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge&logo=langchain&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📖 Introducción

**MediRAG** es un sistema de **Generación Aumentada por Recuperación (RAG)** de grado industrial diseñado para el dominio médico. A diferencia de los tutoriales básicos de RAG, este proyecto se centra en la **ingeniería de datos robusta**, la arquitectura modular y los patrones de diseño avanzados necesarios para desplegar sistemas de IA generativa en producción.

Este repositorio no es solo un chatbot; es una implementación de referencia de cómo construir pipelines de datos resilientes, escalables y mantenibles para aplicaciones de LLM.

---

## 🎯 Importancia para Equipos de ML e IA

En el ecosistema actual de IA Generativa, el **80% del éxito de un sistema RAG reside en la calidad de su ingeniería de datos**, no solo en el modelo de lenguaje elegido.

Para un equipo de ML/IA, adoptar un enfoque de ingeniería como el de MediRAG ofrece ventajas críticas:

### 🚀 Ventajas Competitivas
1.  **Reproducibilidad y Determinismo**: El uso de entornos gestionados (`uv`, Docker) y pipelines orquestados elimina el problema de "funciona en mi máquina".
2.  **Calidad de Datos Superior**: La implementación de estrategias de *Parent-Child Splitting* y *Reranking* asegura que el LLM reciba contexto preciso, reduciendo drásticamente las alucinaciones.
3.  **Mantenibilidad a Largo Plazo**: La arquitectura basada en principios **SOLID** y **Dependency Injection** permite cambiar componentes (ej. cambiar Qdrant por Pinecone, o Gemini por GPT-4) sin reescribir el núcleo del sistema.
4.  **Observabilidad y Testing**: Tratar los datos como código mediante tests de integridad y pipelines de validación E2E permite detectar degradación en la calidad de las respuestas antes de llegar a producción.

---

## 🏗️ Arquitectura y Fases del Proyecto

### 🔹 Fase 1: Infraestructura y Pipeline de Ingestión (Data Engineering)
Establecimiento de una base sólida enfocada en la reproducibilidad y escalabilidad.

*   **Gestión de Dependencias**: Uso de `uv` para entornos virtuales deterministas.
*   **Vector Database**: Despliegue de **Qdrant** vía Docker Compose con persistencia de datos.
*   **ETL Modular (SOLID)**:
    *   **Abstracción**: Interfaces `BaseLoader` y `BaseCleaner` para extensibilidad.
    *   **Extracción**: `PDFLoader` optimizado con `pypdf`.
    *   **Limpieza**: `MedicalTextCleaner` inyectado como dependencia para facilitar tests.

### 🔹 Fase 2: Transformación y Estrategia de Recuperación
Transformación de data cruda en estructuras optimizadas para búsqueda semántica.

*   **Parent-Document Pattern**:
    *   *Child Chunks*: Pequeños, optimizados para búsqueda vectorial (similitud coseno).
    *   *Parent Chunks*: Grandes, optimizados para dar contexto completo al LLM.
*   **Vectorización Local**: Uso de `sentence-transformers` para inferencia rápida y sin coste.
*   **Ingestión por Lotes**: Carga masiva en Qdrant para optimizar I/O de red.

### 🔹 Fase 3: Orquestación Inteligente (Advanced RAG)
Evolución hacia un asistente conversacional con razonamiento refinado.

*   **LLM Integration**: Google Gemini 1.5 Flash para síntesis de respuestas.
*   **Memoria Conversacional**: Sistema de ventana deslizante para mantener contexto del chat.
*   **Query Rewriting**: Reformulación de preguntas basada en el historial para mejorar el retrieval.
*   **Two-Stage Retrieval**:
    1.  **Wide Fetch**: Búsqueda vectorial rápida (High Recall).
    2.  **Deep Rerank**: Reordenamiento con **FlashRank** (Cross-Encoder) para máxima precisión semántica.

### 🔹 Fase 4: Validación y CI/CD de Datos
Garantía de fiabilidad en entornos productivos.

*   **Pipeline de Pruebas E2E**: Orquestador (`src/run_pipeline.py`) que valida secuencialmente:
    1.  Sanity Checks (Entorno/DB).
    2.  Integridad de Datos (ETL).
    3.  Lógica de Transformación.
    4.  Calidad de Retrieval y Reranking.
    5.  Generación Final.

---

## 🛠️ Guía de Instalación y Uso

### Prerrequisitos
*   **Docker** y **Docker Compose** instalados.
*   **Python 3.11+**.
*   **uv** (Recomendado) o `pip`.
*   API Key de Google Gemini (en `.env`).

### 1. Configuración del Entorno

```bash
# Clonar el repositorio
git clone <repo-url>
cd chatbotMedico

# Crear entorno virtual e instalar dependencias
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml  # O requirements.txt si se genera
```

### 2. Levantar Infraestructura

```bash
# Iniciar Qdrant
docker-compose up -d
```

### 3. Ejecutar Pipeline Completo (Validación E2E)

Para ejecutar todo el flujo, desde la ingesta hasta la prueba del chat, utiliza el orquestador:

```bash
python src/run_pipeline.py
```

Este comando ejecutará automáticamente:
*   Verificación de conexión a Qdrant.
*   Descarga del paper médico de muestra.
*   Procesamiento, limpieza y vectorización.
*   Pruebas de búsqueda y generación de respuesta.

---

## 📂 Estructura del Proyecto

```text
src/
├── core/           # Configuración y definiciones de tipos
├── ingestion/      # Loaders, Cleaners y Splitters (ETL)
├── retrieval/      # Lógica de búsqueda y Reranking
├── generation/     # Integración con LLM y cadenas RAG
├── vector_store/   # Cliente y gestión de Qdrant
├── testing/        # Tests unitarios y de integración
└── run_pipeline.py # Orquestador maestro
```

---

> **Nota**: Este proyecto demuestra que un sistema RAG efectivo es mucho más que un script de 50 líneas. Es un sistema de ingeniería de software completo que requiere diseño, pruebas y una arquitectura sólida.
