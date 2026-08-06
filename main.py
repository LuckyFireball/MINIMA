import pyodide_http
import requests
from pyscript import document

pyodide_http.patch_all()

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

    try:
        # Route to your secure host executing your GitHub Secret
        response = requests.post(
            "http://localhost:8000/chat", 
            json={"message": user_text},
            timeout=30
        )
        data = response.json()
        bot_response = data.get("response", "Error parsing engine data.")
    except Exception as e:
        bot_response = f"Engine Connection Offline: {str(e)}"

    # Remove Loading State and Append Final Bot Message
    loading_element = document.querySelector(f"#{loading_id}")
    if loading_element:
        loading_element.remove()

    bot_html = f'<div class="msg-bubble bot-msg">{bot_response}</div>'
    chat_box.innerHTML += bot_html
    chat_box.scrollTop = chat_box.scrollHeight
