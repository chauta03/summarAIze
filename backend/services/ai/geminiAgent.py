import os
import google.generativeai as genai
from dotenv import load_dotenv
from services.ai.prompt import SUMMARIZATION_PROMPT

class GeminiAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")  # or gemini-1.5-pro if you prefer

    def generateSumary(self, script: str) -> str:
        prompt = f"{SUMMARIZATION_PROMPT.strip()}\n\n{script.strip()}"
        response = self.model.generate_content(prompt)
        return response.text
