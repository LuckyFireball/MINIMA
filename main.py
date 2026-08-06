import pyodide_http
import requests
from pyscript import document

# This placeholder will automatically be replaced with your actual GitHub Secret when you push code
API_KEY = "REPLACE_WITH_GITHUB_SECRET"

pyodide_http.patch_all()

# Set up the Gemini API endpoint directly from the browser
BASE_URL = f"https://googleapis.com{API_KEY}"

def send_message(event):
    input_element = document.querySelector("#msg")
    chat_box = document.querySelector("#box")
    user_text = input_element.value
    
    if not user_text.strip():
        return

    # Add User Message to UI
    user_html = f'<div class="msg-bubble user-msg">{user_text}</div>'
    chat_box.innerHTML += user_html
    input_element.value = ""
    chat_box.scrollTop = chat_box.scrollHeight

    # Add Temporary Loading State
    loading_id = "minima-loading-indicator"
    loading_html = f'<div id="{loading_id}" class="msg-bubble bot-msg">Thinking...</div>'
    chat_box.innerHTML += loading_html
    chat_box.scrollTop = chat_box.scrollHeight

    # Structure payload according to Google Gemini API requirements
    payload = {
        "contents": [{"parts": [{"text": user_text}]}],
        "systemInstruction": {
            "parts": [{
                "text": "Your name is Minima. You are a precise coding assistant. CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
            }]
        }
    }

    try:
        # Call Gemini API directly from the browser using your secret key safely injected
        response = requests.post(BASE_URL, json=payload, timeout=30)
        data = response.json()
        
        # Parse response text safely
        bot_response = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        bot_response = f"Engine Connection Offline: {str(e)}"

    # Remove Loading State and Append Final Bot Message
    loading_element = document.querySelector(f"#{loading_id}")
    if loading_element:
        loading_element.remove()

    bot_html = f'<div class="msg-bubble bot-msg">{bot_response}</div>'
    chat_box.innerHTML += bot_html
    chat_box.scrollTop = chat_box.scrollHeight
