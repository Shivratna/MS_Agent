import json
from pydantic import BaseModel, Field
from typing import List, Optional
from models import ProgramRequirements
from utils.gemini_client import GeminiClient

class RequirementsSchema(BaseModel):
    required_documents: List[str] = Field(description="List of required documents (SOP, LORs, etc.)")
    test_requirements: List[str] = Field(description="List of required tests (GRE, TOEFL, etc.)")
    special_notes: Optional[str] = Field(description="Any special instructions or notes")

class RequirementsParserAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def parse(self, program_name: str, raw_text: str) -> ProgramRequirements:
        """
        Extracts structured requirements from raw text using Gemini.
        """
        prompt = f"""
        You are an admissions expert. Extract the application requirements for '{program_name}' from the text below.
        
        Raw Text:
        {raw_text}
        """

        try:
            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=RequirementsSchema
            )
            data = json.loads(response_text)
            return ProgramRequirements(program_name=program_name, **data)
        except Exception as e:
            print(f"Error in RequirementsParserAgent: {e}")
            return ProgramRequirements(
                program_name=program_name,
                required_documents=["Error parsing requirements"],
                test_requirements=[],
                special_notes=f"Failed to parse: {str(e)}"
            )
