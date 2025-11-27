import json
from typing import List
from models import StudentProfile, Program
from utils.gemini_client import GeminiClient
from pydantic import BaseModel, Field

class ProgramSearchAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def search(self, profile: StudentProfile) -> List[Program]:
        """
        Uses Gemini AI to generate relevant program recommendations based on student profile.
        """
        
        prompt = f"""
        You are an expert study abroad counselor with extensive knowledge of Master's programs worldwide.
        
        Generate EXACTLY 3 realistic Master's program recommendations for this student:
        
        **Student Profile:**
        - Target Degree: {profile.target_degree}
        - Target Countries: {', '.join(profile.target_countries)}
        - GPA: {profile.gpa}/4.0
        - Interests: {', '.join(profile.interests)}
        - Budget: {profile.budget}
        - Target Intake: {profile.target_intake}
        - Test Scores: {profile.test_scores if profile.test_scores else 'Not provided'}
        
        **Generate 3 real, well-known programs that:**
        1. Match the student's target degree field
        2. Are in their target countries
        3. Align with their budget range
        4. Match their GPA level (realistic admissions chances)
        5. Are actual programs at real universities (not made up)
        
        **For each program provide:**
        - name: Full program name (e.g., "MS in Economics", "Master of Economics")
        - university: Real university name
        - country: Country name
        - tuition_range: Realistic tuition estimate (e.g., "$30,000-$40,000/year", "€500/semester")
        - application_deadline: Realistic deadline in YYYY-MM-DD format
        - eligibility_criteria: Brief criteria (GPA, tests, etc.)
        - match_reasoning: 1-2 sentences explaining why this program fits the student
        
        **Important:**
        - Use REAL universities and programs
        - Match the degree field they requested (don't suggest CS if they want Economics!)
        - Consider budget constraints
        - Provide realistic deadlines (typically 3-8 months from now)
        
        Return as JSON with a "programs" array containing exactly 3 programs.
        """

        try:
            class RankedProgram(BaseModel):
                name: str
                university: str
                country: str
                tuition_range: str
                application_deadline: str
                eligibility_criteria: str
                match_reasoning: str

            class ProgramList(BaseModel):
                programs: List[RankedProgram]

            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=ProgramList
            )
            
            data = json.loads(response_text)
            results = []
            for p_data in data.get('programs', [])[:3]:  # Ensure max 3
                results.append(Program(**p_data))
            
            if len(results) == 0:
                # Fallback if AI fails
                return self._get_fallback_programs(profile)
            
            return results

        except Exception as e:
            print(f"Error in ProgramSearchAgent: {e}")
            return self._get_fallback_programs(profile)
    
    def _get_fallback_programs(self, profile: StudentProfile) -> List[Program]:
        """Fallback generic programs if AI fails"""
        degree_field = profile.target_degree.split(' in ')[-1] if ' in ' in profile.target_degree else profile.target_degree
        
        return [
            Program(
                name=f"Master's in {degree_field}",
                university="University (AI search unavailable)",
                country=profile.target_countries[0] if profile.target_countries else "USA",
                tuition_range=profile.budget,
                application_deadline="2025-12-31",
                eligibility_criteria="GPA 3.0+",
                match_reasoning="Fallback program - AI search encountered an error. Please verify details."
            )
        ]
