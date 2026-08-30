import os
from fastapi import FastAPI, Request
import google.generativeai as genai

app = FastAPI()

# Configurar Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/")
def home():
    return {"status": "Astrid AI en línea", "version": "1.0"}

@app.post("/chat")
async def alexa_skill(request: Request):
    data = await request.json()
    req_type = data.get("request", {}).get("type", "")

    if req_type == "LaunchRequest":
        texto_respuesta = "¡Hola Joshua! Soy Astrid. Dime, ¿en qué te puedo ayudar?"

    elif req_type == "IntentRequest":
        # Extraer la frase del slot "query" si existe
        slots = data.get("request", {}).get("intent", {}).get("slots", {})
        user_input = ""
        
        for slot in slots.values():
            if "value" in slot and slot["value"]:
                user_input = slot["value"]
                break

        if not user_input:
            user_input = "Hola, preséntate brevemente."

        try:
            response = model.generate_content(
                f"Responde de forma concisa y natural para ser leída por voz: {user_input}"
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
