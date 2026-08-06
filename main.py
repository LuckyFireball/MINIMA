import pyodide_http
import requests
from pyscript import document

# The GitHub workflow will safely insert your AQ. key on this line
API_KEY = "THE_KEY_WILL_BE_HERE"

pyodide_http.patch_all()

BASE_URL = "https://googleapis.com"

def send_message(event):
    input_element = document.querySelector("#msg")
    chat_box = document.querySelector("#box")
    user_text = input_element.value
    
    if not user_text.strip():
        return

    # Render user text onto the screen
    user_html = f'<div class="msg-bubble user-msg">{user_text}</div>'
    chat_box.innerHTML += user_html
    input_element.value = ""
    chat_box.scrollTop = chat_box.scrollHeight

    # Thinking state
    loading_id = "minima-loading"
    loading_html = f'<div id="{loading_id}" class="msg-bubble bot-msg">Thinking...</div>'
    chat_box.innerHTML += loading_html
    chat_box.scrollTop = chat_box.scrollHeight

    payload = {
        "contents": [{"parts": [{"text": user_text}]}],
        "systemInstruction": {
            "parts": [{
                "text": "Your name is Minima. You are a precise coding assistant. CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
            }]
        }
    }

    # Pass your AQ. key inside the safe custom header layout
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

    # Clear loading indicator and show the bot reply
    loading_element = document.querySelector(f"#{loading_id}")
    if loading_element:
        loading_element.remove()

    bot_html = f'<div class="msg-bubble bot-msg">{bot_response}</div>'
    chat_box.innerHTML += bot_html
    chat_box.scrollTop = chat_box.scrollHeight
