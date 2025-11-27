import json
from typing import List
from pydantic import BaseModel, Field
from models import Task, ProgramRequirements
from utils.gemini_client import GeminiClient

class ValidationSchema(BaseModel):
    warnings: List[str] = Field(description="List of potential issues or warnings")

class ChecklistValidatorAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def validate(self, tasks: List[Task], requirements: ProgramRequirements) -> List[str]:
        """
        Reviews the generated tasks against requirements to find gaps or issues.
        """
        prompt = f"""
        You are a quality assurance auditor for college applications.
        Review the following generated task list against the program requirements.
        Identify any missing steps, unrealistic deadlines, or logical errors.
        
        Requirements:
        {requirements}
        
        Generated Tasks:
        {tasks}
        
        Return a list of warnings. If everything looks good, return an empty list.
        """

        try:
            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=ValidationSchema
            )
            data = json.loads(response_text)
            return data.get('warnings', [])
        except Exception as e:
            print(f"Error in ChecklistValidatorAgent: {e}")
            return ["Error validating checklist"]
