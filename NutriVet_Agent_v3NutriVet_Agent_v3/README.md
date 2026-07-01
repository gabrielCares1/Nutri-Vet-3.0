NutriVet AI - Documentación Técnica v3.0
🏗️ Arquitectura del Sistema
NutriVet AI v3.0 implementa un patrón de Agente Autónomo con Ciclo de Razonamiento (ReAct).

Cerebro (LLM): Utiliza GPT-4o vía GitHub Models API para el procesamiento de lenguaje natural y la toma de decisiones.

Memoria (ConversationBufferMemory): Mantiene un estado persistente del historial de conversación en st.session_state, permitiendo al agente recordar datos de sesiones previas.

Herramientas (StructuredTools): * Consultor_Medico_RAG: Basado en ChromaDB y create_stuff_documents_chain para recuperación semántica.

Calculadora_Nutricional: Lógica determinista de Python encapsulada en un decorador @tool para cálculo clínico.

Orquestador: AgentExecutor coordina el flujo, analizando la intención del usuario y seleccionando la herramienta adecuada de forma autónoma.

🛠️ Justificación de Diseño
La separación entre la lógica del agente y las herramientas garantiza una arquitectura modular y escalable (Clean Architecture). Al utilizar StructuredTool, se mejora la robustez frente a errores de inferencia de argumentos, cumpliendo con los estándares de producción de agentes LLM modernos.

🚀 Guía de Despliegue
Instalar dependencias: py -m pip install -r Requerimientos.txt

Configurar entorno: Definir OPENAI_API_KEY (Token GitHub) en app.py.

Ejecución: py -m streamlit run app.py