import os
import time
import logging
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Importamos tu motor RAG real
from Motor_IA import cadena_rag

# --- 1. CONFIGURACIÓN DE OBSERVABILIDAD Y LOGS (IL3.1 e IL3.2) ---
logging.basicConfig(
    filename='nutrivet_agente.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- 2. CONFIGURACIÓN INICIAL Y API KEY ---
os.environ["OPENAI_API_KEY"] = "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" # ¡Recuerda poner tu token!

# Configuramos la página en modo "wide" para que el dashboard se vea bien
st.set_page_config(page_title="NutriVet AI - Agente Clínico", page_icon="🐾", layout="wide") 

# --- 3. DASHBOARD VISUAL DE MÉTRICAS (IE5 - Unidad 3) ---
with st.sidebar:
    st.title("📊 Monitor de Observabilidad")
    st.markdown("Métricas del Agente en Tiempo Real")
    
    try:
        with open("nutrivet_agente.log", "r", encoding="utf-8") as f:
            logs = f.readlines()
            
        latencias = []
        errores = 0
        
        # Analizamos el archivo log línea por línea para extraer datos
        for linea in logs:
            if "ÉXITO" in linea:
                try:
                    # Buscamos la latencia exacta en el texto del log
                    partes = linea.split("|")
                    lat_str = partes[1].split(":")[1].replace("s", "").strip()
                    latencias.append(float(lat_str))
                except:
                    continue
            elif "ERROR CRÍTICO" in linea:
                errores += 1
                
        # Si hay datos, mostramos los gráficos
        if latencias:
            promedio = sum(latencias) / len(latencias)
            
            # KPIs principales
            col1, col2 = st.columns(2)
            col1.metric("Consultas Exitosas", len(latencias))
            col2.metric("Errores Críticos", errores)
            
            st.metric("Latencia Promedio", f"{promedio:.2f} s")
            
            # Gráfico de tendencia de velocidad
            st.subheader("Evolución de Latencia")
            st.line_chart(latencias)
            
            # Botón para limpiar logs (mantenimiento)
            if st.button("🧹 Limpiar Registros"):
                open("nutrivet_agente.log", "w").close()
                st.rerun()
        else:
            st.info("Aún no hay métricas. Haz una consulta en el chat para comenzar a registrar datos.")
            
    except FileNotFoundError:
        st.info("El archivo de trazabilidad se creará automáticamente tras la primera consulta.")

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🐾 NutriVet AI - Agente Clínico Autónomo")
st.write("¡Hola! Soy el Agente NutriVet. Pregúntame sobre riesgos genéticos, dietas para razas específicas, o pídeme que calcule la porción diaria según el peso de tu mascota.")

# --- 5. CONFIGURACIÓN DEL CEREBRO (LLM) ---
llm = ChatOpenAI(
    model="gpt-4o",
    base_url="https://models.inference.ai.azure.com",
    temperature=0.2 
)

# --- 6. HERRAMIENTAS ESTRUCTURADAS (V3.0 + Datos Reales) ---
@tool
def consultar_base_medica(query: str):
    """Úsalo SIEMPRE para buscar riesgos genéticos, dietas y alimentos prohibidos para razas."""
    return cadena_rag.invoke({"input": query})["answer"]

@tool
def calcular_porcion(peso: float):
    """Úsalo para calcular la porción diaria. El input DEBE ser el número del peso en kg."""
    gramos = peso * 25
    return f"Según el peso de {peso} kg, la porción recomendada es de {gramos} gramos."

tools = [consultar_base_medica, calcular_porcion]

# --- 7. CONFIGURACIÓN DE LA MEMORIA ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

# --- 8. PROMPT Y AGENTE ---
# IE6: Agregamos una regla ética de seguridad al system prompt
prompt_agente = ChatPromptTemplate.from_messages([
    ("system", "Eres NutriVet AI, un asistente veterinario experto. REGLA DE SEGURIDAD: Solo puedes responder preguntas sobre nutrición, genética y cuidados de mascotas. Si te preguntan sobre temas ilegales, humanos o ajenos a la veterinaria, debes negarte cortésmente."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agente = create_tool_calling_agent(llm, tools, prompt_agente)
agent_executor = AgentExecutor(agent=agente, tools=tools, memory=st.session_state.memory)

# --- 9. MOTOR DEL CHAT (Con Trazabilidad) ---
for message in st.session_state.memory.chat_memory.messages:
    if message.type == "human":
        with st.chat_message("user"):
            st.markdown(message.content)
    elif message.type == "ai":
        with st.chat_message("assistant"):
            st.markdown(message.content)

if prompt := st.chat_input("¿En qué te puedo ayudar hoy?"):
    st.chat_message("user").markdown(prompt)

    # Iniciar cronómetro de métricas
    inicio_tiempo = time.time()

    try:
        with st.spinner("Analizando protocolos clínicos..."):
            respuesta = agent_executor.invoke({"input": prompt})
        
        # Detener cronómetro
        fin_tiempo = time.time()
        latencia = round(fin_tiempo - inicio_tiempo, 2)

        # Registrar éxito en el log
        logging.info(f"ÉXITO | Latencia: {latencia}s | Input: '{prompt}' | Herramientas: Usadas")

        with st.chat_message("assistant"):
            st.markdown(respuesta["output"])
            
        # Refrescar la app para que el dashboard lateral se actualice inmediatamente
        st.rerun()

    except Exception as e:
        fin_tiempo = time.time()
        latencia = round(fin_tiempo - inicio_tiempo, 2)

        # Registrar error crítico
        logging.error(f"ERROR CRÍTICO | Latencia: {latencia}s | Input: '{prompt}' | Detalle: {str(e)}")
        
        st.error("Protocolo de seguridad activado: Hubo un problema al procesar tu consulta. El incidente ha sido registrado en los logs de observabilidad.")