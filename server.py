import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# Allow your frontend HTML file to communicate safely with this server
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
        # Reads the GitHub secret securely from the server environment
        api_key = os.getenv("THE_KEY")
        if not api_key:
            raise ValueError("Configuration Error: THE_KEY secret is missing!")
        
        self.client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "Your name is Minima. You are a precise coding assistant. "
            "CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside "
            "proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
        )
        self.config = types.GenerateContentConfig(system_instruction=system_instruction)
        self.chat_session = self.client.chats.create(model="gemini-3.6-flash", config=self.config)

    def chat(self, message: str):
        try:
            response = self.chat_session.send_message(message)
            return {"response": response.text}
        except Exception as e:
            return {"response": f"API Error: {str(e)}"}

# Initialize engine instance
bot = ChatbotApi()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return bot.chat(request.message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
