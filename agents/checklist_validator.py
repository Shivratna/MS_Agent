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
        You are a helpful application advisor reviewing a student's application timeline.
        Your job is to spot potential issues and explain them in simple, friendly language.
        
        **Program Requirements:**
        - Required Documents: {requirements.required_documents if requirements.required_documents else 'Not specified - may need to verify on official website'}
        - Test Requirements: {requirements.test_requirements if requirements.test_requirements else 'Not specified - may need to verify on official website'}
        - Special Notes: {requirements.special_notes or 'None'}
        
        **Generated Timeline Tasks:**
        {[f"{task.due_date}: {task.title}" for task in tasks]}
        
        **Your Task:**
        Review the timeline and identify any issues. Write warnings as if you're talking to a student directly.
        
        **Look for these common issues:**
        - Tasks scheduled too close together
        - Not enough time for certain activities (e.g., LORs need 3-4 weeks)
        - Missing requirements that should be verified
        - Any dates that seem off
        
        **Examples of GOOD warnings (student-friendly):**
        - "⏰ Heads up! You've scheduled tasks after the deadline. Make sure all tasks are completed before then."
        - "📋 We couldn't find specific document requirements online. Your first step should be to verify everything on the university's official website!"
        - "📝 Your timeline includes preparing test scores, but we're not sure if tests are actually required. Confirm this with the program."
        - "⚠️ Getting recommendation letters usually takes 3-4 weeks. Your timeline might be too tight - consider requesting them earlier."
        - "💡 Great news! The timeline looks solid. Just make sure to stick to the deadlines and you'll be all set!"
        
        **Examples of BAD warnings (too technical - AVOID):**
        - "The ProgramRequirements state 'required_documents=[]'..." ❌
        - "Logical error in data structure..." ❌
        - "Timeline tasks contradict provided schema..." ❌
        
        **Rules:**
        1. Write like you're helping a friend, not writing code documentation
        2. Use emojis (⏰ 📋 ⚠️ 💡) to make warnings scannable
        3. Focus on ACTIONABLE advice - what should the student do?
        4. If requirements were unclear, suggest checking the official university website
        5. If everything looks good, you can return a positive encouragement or empty list
        6. Keep warnings concise (1-2 sentences max each)
        
        Return a list of warnings (or empty list if no issues found).
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
