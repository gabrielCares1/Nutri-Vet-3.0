# 🐾 NutriVet AI v3.0 - Edición Segura y Observable

> **Agente Clínico Autónomo para Asesoría Nutricional Veterinaria con Monitoreo en Tiempo Real**

NutriVet AI es un sistema avanzado de inteligencia artificial diseñado para brindar recomendaciones nutricionales precisas, basadas en literatura clínica oficial. En su versión 3.0, el sistema integra arquitectura **ReAct**, capacidades de **Generación Aumentada por Recuperación (RAG)** y una robusta capa de **Observabilidad y Seguridad**.

---

## 🏗️ Arquitectura del Sistema
El sistema implementa un patrón **ReAct (Reason + Act)**, permitiendo al agente razonar sobre las necesidades del usuario, invocar herramientas de forma autónoma y mantener el estado de la conversación.

### 🧠 Componentes Core
* **Cerebro (LLM):** GPT-4o (vía GitHub Models API).
* **Orquestador:** `AgentExecutor` (LangChain).
* **Memoria:** `ConversationBufferMemory` persistente en la sesión.
* **Motor RAG:** Integración con `ChromaDB` para vectorización de manuales clínicos (WSAVA).

### 🛡️ Capa de Observabilidad y Seguridad (Unidad 3)
* **Trazabilidad y Logs:** Registro persistente de latencia, inputs y errores críticos mediante la librería nativa `logging` (`nutrivet_agente.log`).
* **Monitor en Tiempo Real:** Dashboard visual interactivo en la barra lateral que procesa KPIs (Consultas Exitosas, Errores Críticos y Evolución de Latencia).
* **Filtros Éticos:** Protocolos de seguridad estrictos inyectados en el *System Prompt* para prevenir *Prompt Injection* y rechazar consultas humanas/no veterinarias.

---

## 🛠️ Herramientas Estructuradas (Structured Tools)
1. 🩺 **Consultor_Medico_RAG:** Recuperación semántica de datos clínicos, riesgos genéticos y alimentos prohibidos.
2. 🧮 **Calculadora_Nutricional:** Lógica determinista para el cálculo clínico de porciones diarias según el peso de la mascota.

---

## 🚀 Guía de Despliegue

### 1. Requisitos previos
Asegúrate de tener Python 3.10 o superior instalado en tu sistema.

### 2. Instalación
Clona el repositorio e instala las dependencias necesarias:
```bash
py -m pip install -r Requerimientos.txt
