import os
import requests

ULTRAMSG_INSTANCE_ID = os.getenv("WHATSAPP_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("WHATSAPP_TOKEN")

def send_whatsapp_message(to_number: str, message: str) -> None:
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": to_number,  
        "body": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Erro ao enviar mensagem UltraMsg:", response.text)
        response.raise_for_status()