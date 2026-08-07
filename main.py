#all imports
import os
import sys
from google import genai
from google.genai import types

# This variable automatically receives your secret during the GitHub build stage
API_KEY = os.getenv("THE_KEY")

class ChatbotApi:
    def __init__(self):
        if not API_KEY:
            raise ValueError("Error: THE_KEY secret is completely missing from the build environment!")
            
        self.client = genai.Client(api_key=API_KEY)
        self.system_instruction = (
            "Your name is Minima. You are a precise coding assistant. "
            "CRITICAL: Whenever you generate, show, or mention code, you MUST wrap it inside "
            "proper markdown code blocks with the correct language identifier (e.g., ```python ... ```)."
        )
        self.config = types.GenerateContentConfig(system_instruction=self.system_instruction)
        self.chat_session = self.client.chats.create(model="gemini-3.6-flash", config=self.config)

    def chat(self, message):
        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            return f"Google Studio Core Processing Error: {str(e)}"

if __name__ == "__main__":
    try:
        bot = ChatbotApi()
        print("=" * 50)
        print(" MINIMA AI ENGINE INITIALIZED SUCCESSFULLY")
        print(" Type 'exit' and press Enter to close the application.")
        print("=" * 50 + "\n")
        
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("\nShutting down engine. Goodbye!")
                break
                
            print("\nMinima is thinking...")
            result = bot.chat(user_input)
            print(f"\nMinima:\n{result}\n")
            print("-" * 50)
            
    except Exception as e:
        print(f"\n[Initialization Crash] {e}")
        input("\nPress Enter to close...")
