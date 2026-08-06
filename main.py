import os
from google import genai
from google.genai import types

API_KEY = "REPLACE_WITH_GITHUB_SECRET"

class ChatbotApi:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        system_instruction = (
            "Your name is Minima. You are a precise coding assistant. "
            "CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside "
            "proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
        )
        self.config = types.GenerateContentConfig(system_instruction=system_instruction)
        self.chat_session = self.client.chats.create(model="gemini-3.6-flash", config=self.config)

    def chat(self, message):
        try:
            response = self.chat_session.send_message(message)
            return {"response": response.text}
        except Exception as e:
            return {"response": f"Error: {str(e)}"}

if __name__ == "__main__":
    bot = ChatbotApi()
    print("Minima Engine Initialized. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        result = bot.chat(user_input)
        print(f"\nMinima: {result['response']}\n")
