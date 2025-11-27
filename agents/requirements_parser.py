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
        You are an expert at extracting university admission requirements from web content.
        
        **Program:** {program_name}
        
        **Web Content:**
        {raw_text[:8000]}  
        
        **Your Task:**
        Extract the following information. If something is not clearly stated, leave it empty rather than guessing.
        
        1. **Required Documents:** List ONLY documents explicitly required (e.g., "Statement of Purpose", "2 Letters of Recommendation", "Official Transcripts", "CV/Resume")
        2. **Test Requirements:** List ONLY tests explicitly required (e.g., "GRE General Test", "TOEFL iBT (minimum 90)", "IELTS (minimum 6.5)")
        3. **Special Notes:** Any important notes like:
           - Early application benefits
           - Interview requirements
           - Portfolio requirements
           - Specific formatting guidelines
           - "Check the official website for complete requirements" (if content seems incomplete)
        
        **Important Rules:**
        - If the text doesn't mention a requirement, DON'T include it
        - If you're unsure, add a note in special_notes suggesting the student verify on the official website
        - Be specific with test scores (include minimum scores if mentioned)
        - Don't add generic requirements that aren't explicitly stated
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
