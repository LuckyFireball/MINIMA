import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# Allow your PyScript front-end to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatbotApi:
    def __init__(self):
        api_key = os.getenv("THE_KEY")
        if not api_key:
            raise ValueError("THE_KEY missing from environment")
        self.client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "Your name is Minima. You are a precise coding assistant. "
            "CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside "
            "proper markdown code blocks with the correct language identifier (e.g., ```python ... ```). "
            "Ensure every code block has a clear beginning and ending so it can be easily copied."
        )
        self.config = types.GenerateContentConfig(system_instruction=system_instruction)
        self.chat_session = self.client.chats.create(model="gemini-3.6-flash", config=self.config)

    def chat(self, message: str):
        try:
            response = self.chat_session.send_message(message)
            return {"response": response.text}
        except Exception as e:
            return {"response": f"Google AI Studio Error: {str(e)}"}

# Initialize bot instance
bot = ChatbotApi()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return bot.chat(request.message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
