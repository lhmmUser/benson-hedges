import httpx
from app.config import get_settings


class WhatsappClient:
    def __init__(self):
        settings = get_settings()
        self.token = settings.ACCESS_TOKEN
        self.phone_id = settings.PHONE_NUMBER_ID
        self.api = f"https://graph.facebook.com/v19.0/{self.phone_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def send_text(self, to: str, message: str):
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message},
        }
        try:
            r = httpx.post(self.api, headers=self.headers, json=payload, timeout=10)
            return r.json()
        except Exception as e:
            print("WhatsApp send error:", e)
            return None
