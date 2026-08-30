from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

# 1. Configuración de Gemini API
API_KEY = "AQ.Ab8RN6IBz8ofjxtF5T56_zFuG20buEnQlKXXaQU33ZWkBh7PoA"
client = genai.Client(api_key=API_KEY)

configuracion = types.GenerateContentConfig(
    system_instruction=(
        "Tu nombre es Astrid. Eres un sistema de inteligencia artificial avanzado, "
        "diseñado para ser un asistente personal altamente eficiente, directo, sabio "
        "y servicial. Mantén tus respuestas breves y concisas (máximo 2 a 3 oraciones), "
        "ideales para ser leídas por un asistente de voz."
    ),
    temperature=0.7,
)

# Inicializar la app FastAPI
app = FastAPI(title="Astrid AI Server")

# Guardar la sesión de chat activa
chat = client.chats.create(
    model="gemini-3.5-flash",
    config=configuracion
)

# Modelo para validar los datos que recibe la API
class MensajeUsuario(BaseModel):
    texto: str

@app.get("/")
def estado_servidor():
    return {"status": "Astrid AI en línea", "version": "1.0"}

@app.post("/chat")
def interactuar_astrid(mensaje: MensajeUsuario):
    try:
        if not mensaje.texto.strip():
            raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")

        respuesta = chat.send_message(mensaje.texto)
        return {"respuesta": respuesta.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))