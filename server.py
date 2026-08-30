import os
from fastapi import FastAPI, Request
from google import genai
from google.genai import types

app = FastAPI()

# Inicializar cliente con la API Key configurada en Render
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Configuración de personalidad original de Astrid
configuracion = types.GenerateContentConfig(
    system_instruction=(
        "Tu nombre es Astrid. Eres un sistema de inteligencia artificial avanzado, "
        "diseñado para ser un asistente personal altamente eficiente, directo, sabio "
        "y servicial. Mantén tus respuestas claras, concisas, naturales y listas para ser leídas por voz."
    ),
    temperature=0.7,
)

@app.get("/")
def home():
    return {"status": "Astrid AI en línea", "version": "1.0"}

@app.post("/chat")
async def alexa_skill(request: Request):
    data = await request.json()
    req_type = data.get("request", {}).get("type", "")

    # Saludo inicial al abrir la skill
    if req_type == "LaunchRequest":
        texto_respuesta = "¡Hola! Soy Astrid. ¿En qué te puedo ayudar hoy?"

    elif req_type == "IntentRequest":
        # Extraer el texto de la variable/slot capturada por Alexa
        slots = data.get("request", {}).get("intent", {}).get("slots", {})
        user_input = ""
        
        for slot in slots.values():
            if "value" in slot and slot["value"]:
                user_input = slot["value"]
                break

        # Si por alguna razón la entrada llega vacía, pide aclaración en lugar de inventar
        if not user_input:
            texto_respuesta = "No logré escucharte bien, ¿podrías repetirlo?"
        else:
            try:
                # Consulta directa a Gemini 3.6 Flash
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=user_input,
                    config=configuracion
                )
                texto_respuesta = response.text
            except Exception as e:
                texto_respuesta = f"Error al procesar la solicitud: {str(e)}"

    else:
        texto_respuesta = "Hasta luego."

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto_respuesta
            },
            "shouldEndSession": False
        }
    }
