import os
from google import genai
from google.genai import types

class ChatbotApi:
    def __init__(self):
        # This reads THE_KEY directly from the GitHub build environment
        api_key = os.getenv("THE_KEY")
        
        if not api_key:
            raise ValueError("Error: THE_KEY is missing from the environment!")
            
        self.client = genai.Client(api_key=api_key)
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
