import os
from fastapi import FastAPI, Request
from google import genai
from google.genai import types

app = FastAPI()

# Inicializar cliente con la clave almacenada en Render
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Personalidad de Astrid usando tu configuración de PyCharm
configuracion = types.GenerateContentConfig(
    system_instruction=(
        "Tu nombre es Astrid. Eres un sistema de inteligencia artificial avanzado, "
        "diseñado para ser un asistente personal altamente eficiente, directo, sabio "
        "y servicial. Mantén tus respuestas claras, concisas y con un tono natural y elegante "
        "apropiado para ser leído por voz."
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

    # Saludo neutro para cualquier usuario
    if req_type == "LaunchRequest":
        texto_respuesta = "¡Hola! Soy Astrid, tu asistente de inteligencia artificial. ¿En qué te puedo ayudar hoy?"

    elif req_type == "IntentRequest":
        slots = data.get("request", {}).get("intent", {}).get("slots", {})
        user_input = ""
        
        for slot in slots.values():
            if "value" in slot and slot["value"]:
                user_input = slot["value"]
                break

        if not user_input:
            user_input = "Hola, preséntate brevemente."

        try:
            # Modelo gemini-3.6-flash probado en tu entorno
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_input,
                config=configuracion
            )
            texto_respuesta = response.text
        except Exception as e:
            texto_respuesta = f"Error al consultar Gemini: {str(e)}"

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
