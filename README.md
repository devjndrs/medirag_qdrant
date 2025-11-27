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
