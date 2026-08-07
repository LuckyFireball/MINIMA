import pyodide_http
import requests
from pyscript import document
from js import formatMarkdownText, showLoadingIndicator, removeLoadingIndicator, appendMessage

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
        self.msg_input = document.querySelector("#msg")

    def handle_send(self, event=None):
        user_text = self.msg_input.value.strip()
        if not user_text:
            return

        appendMessage(user_text, False)
        self.msg_input.value = ""

        animation_id = showLoadingIndicator()

        payload = {
            "contents": [{"parts": [{"text": user_text}]}],
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
            bot_response = data["candidates"]["content"]["parts"]["text"]
        except Exception as e:
            bot_response = f"Engine Connection Offline: {str(e)}"

        removeLoadingIndicator(animation_id)
        appendMessage(bot_response, True)

    def check_enter(self, event):
        if event.key == "Enter":
            self.handle_send()

# Instantiate the global object so your HTML py-hooks can touch it instantly
bot = ChatbotApi()
