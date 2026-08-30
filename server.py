import os
from fastapi import FastAPI, Request
from google import genai
from google.genai import types

app = FastAPI()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Configuración optimizada para velocidad y brevedad estricta
configuracion = types.GenerateContentConfig(
    system_instruction=(
        "Tu nombre es Astrid. Eres una asistente de IA concisa, directa y servicial. "
        "REGLA ESTRICTA: Responde SIEMPRE en un máximo de 2 a 3 oraciones cortas. "
        "Ve directo al grano sin introducciones ni despedidas para que la respuesta sea instantánea."
    ),
    temperature=0.7,
    max_output_tokens=150,  # Limite físico para evitar demoras
)

@app.get("/")
def home():
    return {"status": "Astrid AI en línea", "version": "1.0"}

@app.post("/chat")
async def alexa_skill(request: Request):
    data = await request.json()
    req_type = data.get("request", {}).get("type", "")

    if req_type == "LaunchRequest":
        texto_respuesta = "¡Hola! Soy Astrid. ¿En qué te puedo ayudar hoy?"

    elif req_type == "IntentRequest":
        slots = data.get("request", {}).get("intent", {}).get("slots", {})
        user_input = ""
        
        for slot in slots.values():
            if "value" in slot and slot["value"]:
                user_input = slot["value"]
                break

        if not user_input:
            user_input = "Preséntate en una sola oración."

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=user_input,
                config=configuracion
            )
            texto_respuesta = response.text
        except Exception:
            texto_respuesta = "Lo siento, la consulta tomó demasiado tiempo. Inténtalo de nuevo."

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
