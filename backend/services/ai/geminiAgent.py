import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from services.ai.prompt import SUMMARIZATION_PROMPT

class GeminiAgent:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    def generateSumary(self, script: str) -> str:
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[
                types.Part.from_text(text=SUMMARIZATION_PROMPT),
                types.Part.from_text(text=script)
            ]
        )
        
        return response.text
