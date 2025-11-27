import json
from typing import List
from models import StudentProfile, Program
from utils.gemini_client import GeminiClient

# Mock Data
MOCK_PROGRAMS = [
    {
        "name": "MS in Computer Science",
        "university": "Technical University of Munich",
        "country": "Germany",
        "tuition_range": "0 - 1500 EUR/semester",
        "application_deadline": "2025-05-31",
        "eligibility_criteria": "GPA > 3.0, GRE optional, IELTS 6.5"
    },
    {
        "name": "MS in Data Science",
        "university": "RWTH Aachen",
        "country": "Germany",
        "tuition_range": "0 EUR/semester",
        "application_deadline": "2025-03-01",
        "eligibility_criteria": "GPA > 3.2, GRE required, TOEFL 90"
    },
    {
        "name": "Master of Computer Science",
        "university": "University of Illinois Urbana-Champaign",
        "country": "USA",
        "tuition_range": "$40,000 - $50,000/year",
        "application_deadline": "2025-01-15",
        "eligibility_criteria": "GPA > 3.5, GRE required, TOEFL 100"
    },
    {
        "name": "MS in AI",
        "university": "University of Amsterdam",
        "country": "Netherlands",
        "tuition_range": "15,000 EUR/year",
        "application_deadline": "2025-04-01",
        "eligibility_criteria": "GPA > 3.0, Strong Math background"
    },
    {
        "name": "MS in Software Engineering",
        "university": "San Jose State University",
        "country": "USA",
        "tuition_range": "$20,000 - $30,000/year",
        "application_deadline": "2025-02-20",
        "eligibility_criteria": "GPA > 3.0, GRE optional"
    }
]

class ProgramSearchAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def search(self, profile: StudentProfile) -> List[Program]:
        """
        Filters and ranks mock programs based on the student profile using Gemini.
        """
        # 1. Basic filtering (Python side) - e.g., Country
        filtered_programs = [
            p for p in MOCK_PROGRAMS 
            if any(c.lower() in p['country'].lower() for c in profile.target_countries) 
            or "Any" in profile.target_countries
        ]
        
        if not filtered_programs:
            # Fallback if strict filtering fails
            filtered_programs = MOCK_PROGRAMS

        # 2. Ranking with Gemini
        prompt = f"""
        You are an expert study abroad counselor.
        Rank the following programs for this student profile.
        Select the top 3 best fits.
        For each selected program, provide a brief 'match_reasoning' explaining why it fits.

        Student Profile:
        {profile}

        Available Programs:
        {json.dumps(filtered_programs, indent=2)}

        Return a JSON list of the top 3 programs with their original fields plus 'match_reasoning'.
        """

        try:
            # We can use a schema for strict output, or just ask for JSON
            # Using schema for robustness
            from pydantic import BaseModel, Field
            class RankedProgram(BaseModel):
                name: str
                university: str
                country: str
                tuition_range: str
                application_deadline: str
                eligibility_criteria: str
                match_reasoning: str

            class RankedList(BaseModel):
                programs: List[RankedProgram]

            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=RankedList
            )
            
            data = json.loads(response_text)
            results = []
            for p_data in data.get('programs', []):
                results.append(Program(**p_data))
            return results

        except Exception as e:
            print(f"Error in ProgramSearchAgent: {e}")
            # Fallback: return first 3 filtered
            return [Program(**p) for p in filtered_programs[:3]]
