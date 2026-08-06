import pyodide_http
import requests
from pyscript import document

# The GitHub workflow builder will overwrite this text block with your real key value
API_KEY = "REPLACE_WITH_GITHUB_SECRET"

pyodide_http.patch_all()

BASE_URL = "https://googleapis.com"

def send_message(event):
    input_element = document.querySelector("#msg")
    chat_box = document.querySelector("#box")
    user_text = input_element.value
    
    if not user_text.strip():
        return

    # Render your input text onto the screen bubble layout
    user_html = f'<div class="msg-bubble user-msg">{user_text}</div>'
    chat_box.innerHTML += user_html
    input_element.value = ""
    chat_box.scrollTop = chat_box.scrollHeight

    # Generate temporary thinking text block
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

    headers = {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers, timeout=30)
        data = response.json()
        bot_response = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        bot_response = f"Engine Connection Offline: {str(e)}"

    # Delete thinking indicator and render the true reply string
    loading_element = document.querySelector(f"#{loading_id}")
    if loading_element:
        loading_element.remove()

    bot_html = f'<div class="msg-bubble bot-msg">{bot_response}</div>'
    chat_box.innerHTML += bot_html
    chat_box.scrollTop = chat_box.scrollHeight
