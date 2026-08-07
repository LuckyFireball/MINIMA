import pyodide_http
import requests
from pyscript import document, when

# The GitHub workflow safely substitutes your AQ. key right here
API_KEY = "THE_KEY_WILL_BE_HERE"

pyodide_http.patch_all()

BASE_URL = "https://googleapis.com"
SYSTEM_INSTRUCTION = (
    "Your name is Minima. You are a precise coding assistant. "
    "CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside "
    "proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
)

def append_message_to_ui(text, is_bot):
    chat_box = document.querySelector("#box")
    bubble = document.createElement("div")
    bubble.className = "msg-bubble bot-msg" if is_bot else "msg-bubble user-msg"
    
    # Render basic linebreaks if markdown blocks aren't present
    bubble.innerHTML = text.replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;")
    chat_box.appendChild(bubble)
    chat_box.element.scrollTop = chat_box.element.scrollHeight

def process_chat_cycle():
    msg_input = document.querySelector("#msg")
    user_text = msg_input.element.value.strip()
    
    if not user_text:
        return
        
    # Show user message and wipe text box
    append_message_to_ui(user_text, is_bot=False)
    msg_input.element.value = ""
    
    # Render loading bubble
    chat_box = document.querySelector("#box")
    loader = document.createElement("div")
    loader.className = "msg-bubble bot-msg"
    loader.id = "minima-loader"
    loader.textContent = "Thinking..."
    chat_box.appendChild(loader)
    chat_box.element.scrollTop = chat_box.element.scrollHeight
    
    payload = {
        "contents": [{"parts": [{"text": user_text}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]}
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
        
    # Remove loader bubble and display final response text
    loader_el = document.querySelector("#minima-loader")
    if loader_el:
        loader_el.element.remove()
        
    append_message_to_ui(bot_response, is_bot=True)

# Native PyScript events: Listen directly to elements using pure Python tags!
@when("click", "#sendBtn")
def click_handler(event):
    process_chat_cycle()

@when("keydown", "#msg")
def key_handler(event):
    if event.key == "Enter":
        process_chat_cycle()
