import json
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from models import StudentProfile
from utils.gemini_client import GeminiClient

class TestScore(BaseModel):
    name: str = Field(description="Name of the test (e.g., GRE, TOEFL)")
    score: str = Field(description="Score obtained")

class StudentProfileSchema(BaseModel):
    gpa: float = Field(description="GPA on a 4.0 scale")
    target_degree: str = Field(description="Target degree (e.g., MS in CS)")
    target_countries: List[str] = Field(description="List of target countries")
    budget: str = Field(description="Budget range or limit")
    interests: List[str] = Field(description="Academic and research interests")
    target_intake: str = Field(description="Target intake (e.g., Fall 2025)")
    test_scores: List[TestScore] = Field(default_factory=list, description="List of test scores")

class ProfileIntakeAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def process(self, raw_data: dict) -> StudentProfile:
        """
        Normalizes raw student data into a structured StudentProfile using Gemini.
        """
        prompt = f"""
        You are an expert education counselor. Analyze the following raw student profile data and extract a structured profile.
        Normalize GPA to 4.0 scale if possible, or keep as is if unsure.
        Standardize country names.
        
        Raw Data:
        {json.dumps(raw_data, indent=2)}
        """
        
        try:
            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=StudentProfileSchema
            )
            data = json.loads(response_text)
            
            # Convert list of TestScore back to dict for StudentProfile
            test_scores_dict = {}
            for ts in data.get('test_scores', []):
                # Handle case where data might be dict or object depending on how json.loads behaves with pydantic schema output
                # The output from Gemini is JSON, so it will be a list of dicts
                if isinstance(ts, dict):
                    test_scores_dict[ts.get('name')] = ts.get('score')
            
            # Remove test_scores from data to avoid double passing
            if 'test_scores' in data:
                del data['test_scores']
                
            return StudentProfile(test_scores=test_scores_dict, **data)
        except Exception as e:
            print(f"Error in ProfileIntakeAgent: {e}")
            # Fallback: try to map directly if LLM fails, or re-raise
            # For MVP, we'll just re-raise or return a partial profile
            raise e
