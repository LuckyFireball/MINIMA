import json
from pyscript import document, window
from pyodide.http import pyfetch

history = []

SYSTEM_INSTRUCTION = (
    "Your name is minima, When you generate code, you must wrap the code inside "
    "markdown code blocks (e.g., ```python ... ```)."
)

def add_message(text, is_bot):
    box = document.getElementById("box")
    bubble = document.createElement("div")
    bubble.className = "msg-bubble bot-msg" if is_bot else "msg-bubble user-msg"
    bubble.innerText = text
    box.appendChild(bubble)
    box.scrollTop = box.scrollHeight

async def send_message(event=None):
    msg_input = document.getElementById("msg")
    key_input = document.getElementById("apiKey")
    message = msg_input.value.strip()
    api_key = key_input.value.strip()

    if not message:
        return
    if not api_key:
        add_message("Please paste your Gemini API key above first.", True)
        return

    add_message(message, False)
    msg_input.value = ""

    contents = []
    for m in history:
        contents.append({"role": m["role"], "parts": [{"text": m["content"]}]})
    contents.append({"role": "user", "parts": [{"text": message}]})

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]}
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    try:
        response = await pyfetch(
            url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload)
        )
        data = await response.json()

        assistant_message = data["candidates"][0]["content"]["parts"][0]["text"]

        history.append({"role": "user", "content": message})
        history.append({"role": "model", "content": assistant_message})

        add_message(assistant_message, True)

    except Exception as e:
        add_message(f"Gemini API Error: {str(e)}", True)

send_btn = document.getElementById("sendBtn")
send_btn.addEventListener("click", send_message)

msg_input = document.getElementById("msg")
def on_enter(event):
    if event.key == "Enter":
        window.setTimeout(create_proxy_wrapper, 0)

from pyodide.ffi import create_proxy

async def enter_handler(event):
    if event.key == "Enter":
        await send_message()

msg_input.addEventListener("keypress", create_proxy(enter_handler))
