import os
from fastapi import FastAPI, Request
from google import genai

app = FastAPI()

# Inicializar cliente de Gemini
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"status": "Astrid AI en línea", "version": "1.0"}

@app.post("/chat")
async def alexa_skill(request: Request):
    data = await request.json()
    req_type = data.get("request", {}).get("type", "")

    # Cuando abres la skill diciendo "abre oye astrid"
    if req_type == "LaunchRequest":
        texto_respuesta = "¡Hola! Soy Astrid. ¿En qué te puedo ayudar hoy?"
    
    # Cuando le haces una pregunta directamente
    elif req_type == "IntentRequest":
        # Intentamos obtener la frase del usuario o le enviamos un prompt general
        user_input = "Hola Astrid, preséntate brevemente"
        slots = data.get("request", {}).get("intent", {}).get("slots", {})
        
        for slot in slots.values():
            if "value" in slot:
                user_input = slot["value"]
                break

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Responde de forma concisa y natural para ser leída por voz: {user_input}"
            )
            texto_respuesta = response.text
        except Exception as e:
            texto_respuesta = "Lo siento, tuve un problema al conectarme con mi cerebro de Gemini."
    
    else:
        texto_respuesta = "Hasta luego."

    # Formato de respuesta que exige Alexa
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
