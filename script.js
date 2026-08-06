import pyodide_http
import requests
import json

# The GitHub workflow will safely insert your AQ. key right here
API_KEY = "THE_KEY_WILL_BE_HERE"

pyodide_http.patch_all()

BASE_URL = "https://googleapis.com"

class ChatbotApi:
    def __init__(self):
        self.system_instruction = (
            "Your name is Minima. You are a precise coding assistant. "
            "CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside "
            "proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
        )

    def chat(self, message):
        payload = {
            "contents": [{"parts": [{"text": message}]}],
            "systemInstruction": {
                "parts": [{"text": self.system_instruction}]
            }
        }

        headers = {
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(BASE_URL, json=payload, headers=headers, timeout=30)
            data = response.json()
            bot_response = data["candidates"]["content"]["parts"][0]["text"]
            return {"response": bot_response}
        except Exception as e:
            return {"response": f"Engine Connection Offline: {str(e)}"}

# Initialize the global instance so your JavaScript file can see it
bot = ChatbotApi()
