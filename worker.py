import openai
import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave API desde la variable de entorno
openai_api_key = os.getenv('OPENAI_API_KEY')

# Verificar si la clave API está cargada correctamente
if openai_api_key is None:
    raise ValueError("No se encontró la clave API de OpenAI. Asegúrese de que el archivo .env esté configurado correctamente.")

# Establecer la clave de API de OpenAI
openai.api_key = openai_api_key

def speech_to_text(audio_binary):
    """
    Convierte un archivo de audio binario en texto usando la API de Watson Speech-to-Text.
    """
    base_url = 'base_url = "https://sn-watson-stt.labs.skills.network"'
    api_url = base_url + '/speech-to-text/api/v1/recognize'
    
    params = {
        'model': 'en-US_Multimedia',
    }
    
    # Enviar una solicitud POST a la API
    response = requests.post(api_url, params=params, data=audio_binary).json()
    
    # Procesar la respuesta para obtener el texto transcrito
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognized text:', text)
        return text


def text_to_speech(text, voice=""):
    """
    Convierte el texto en un archivo de audio utilizando la API de Watson Text-to-Speech.
    """
    base_url = 'https://sn-watson-tts.labs.skills.network'
    api_url = f"{base_url}/text-to-speech/api/v1/synthesize?output=output_text.wav"

    # Agregar parámetro de voz si se especifica
    if voice and voice != "default":
        api_url += f"&voice={voice}"

    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    json_data = {
        'text': text,
    }

    try:
        # Enviar solicitud POST a la API
        response = requests.post(api_url, headers=headers, json=json_data)
        
        # Verificar si la respuesta fue exitosa
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        
        print('Respuesta de texto a voz:', response)
        return response.content  # Retorna el contenido del audio
    
    except requests.exceptions.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None  # Retorna None o maneja el error según sea necesario



def openai_process_message(user_message):
    prompt = "Act as a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations."
    
    try:
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=4000
        )
        
        response_text = openai_response['choices'][0]['message']['content']
        return response_text
    
    except Exception as e:
        print(f"Error al llamar a la API: {e}")
        return "Lo siento, ocurrió un error al procesar tu solicitud."