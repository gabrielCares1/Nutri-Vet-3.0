import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# --- 1. CONFIGURACIÓN DEL TOKEN ---
# Asegúrate de poner tu token de GitHub real aquí
os.environ["OPENAI_API_KEY"] = "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"

# --- 2. INGESTA Y PROCESAMIENTO DEL PDF ---
print("Cargando Asistente.pdf...")
loader = PyPDFLoader("Asistente.pdf")
docs = loader.load()

# Dividir el texto en fragmentos (chunks)
print("Dividiendo documentos...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# --- 3. VECTORIZACIÓN (AQUÍ ESTÁ LA CORRECCIÓN) ---
print("Vectorizando y creando ChromaDB...")
vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://models.inference.ai.azure.com" # Esta línea soluciona el AuthenticationError
    )
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 4. CREACIÓN DEL LLM (CEREBRO) ---
llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0,
    base_url="https://models.inference.ai.azure.com" # Apuntando también a GitHub/Azure
)

# --- 5. CONFIGURACIÓN DE LA CADENA RAG ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres NutriVet AI, un asistente veterinario experto. Usa exclusivamente este contexto clínico para responder a las preguntas de nutrición y riesgos genéticos: \n\n{context}\n\nSi la respuesta no está en el contexto, indica que no tienes información médica al respecto."),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, prompt)
cadena_rag = create_retrieval_chain(retriever, question_answer_chain)

print("Motor RAG inicializado con éxito. Listo para ser usado por app.py.")