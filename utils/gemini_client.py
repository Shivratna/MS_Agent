import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def generate_content(self, prompt: str, system_instruction: str = None, response_schema=None) -> str:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json" if response_schema else "text/plain",
            response_schema=response_schema
        )
        
        import time
        import random
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                if "503" in str(e) or "429" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        print(f"Gemini API overloaded. Retrying in {wait_time:.1f}s...")
                        time.sleep(wait_time)
                        continue
                raise e
