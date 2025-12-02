import json
from typing import Dict, Any
from utils.gemini_client import GeminiClient

class ResumeParserAgent:
    """Extracts student profile information from resume text."""
    
    def __init__(self, client: GeminiClient):
        self.client = client
        
    def parse(self, resume_text: str) -> Dict[str, Any]:
        """
        Parses resume text and extracts structured profile data.
        """
        prompt = """
        You are an expert admission counselor. Extract the following student profile information from the resume text below.
        
        **Resume Text:**
        """
        prompt += resume_text[:10000]
        prompt += """
        
        **Extract these fields:**
        - gpa: Float (scale of 4.0, normalize if needed. If not found, return 0.0)
        - undergrad_major: String (e.g., "Computer Science", "Mechanical Engineering")
        - work_experience_years: Float (Total years of full-time work exp. Exclude internships unless significant. If 0, return 0.0)
        - backlogs: Integer (Number of backlogs/fails mentioned. If not found, return 0)
        - research_papers: Integer (Count of published papers. If not found, return 0)
        - test_scores: Dictionary of scores (e.g., {"GRE": "320", "TOEFL": "100"})
        - interests: List of strings (Research interests or key skills)
        - target_degree: String (Infer from objective or background, e.g., "MS in Computer Science")
        
        **Return ONLY valid JSON in this format:**
        {
            "gpa": 3.8,
            "undergrad_major": "Computer Science",
            "work_experience_years": 2.5,
            "backlogs": 0,
            "research_papers": 1,
            "test_scores": {"GRE": "325", "TOEFL": "110"},
            "interests": ["Artificial Intelligence", "Data Science"],
            "target_degree": "MS in Computer Science"
        }
        
        If a field is not found, use reasonable defaults (0 or empty string/list).
        """
        
        try:
            response_text = self.client.generate_content(prompt=prompt).strip()
            print(f"[DEBUG] Raw response: {response_text[:200]}...")  # Debug first 200 chars
            
            # Clean response - handle multiple markdown formats
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join([line for line in lines if not line.startswith('```')])
                response_text = response_text.strip()
            
            # Remove any "json" language identifier
            if response_text.startswith('json'):
                response_text = response_text[4:].strip()
                
            print(f"[DEBUG] Cleaned response: {response_text[:200]}...")  # Debug after cleaning
            
            data = json.loads(response_text)
            
            # Ensure all required fields exist with defaults
            return {
                'gpa': data.get('gpa', 0.0),
                'undergrad_major': data.get('undergrad_major', ''),
                'work_experience_years': data.get('work_experience_years', 0.0),
                'backlogs': data.get('backlogs', 0),
                'research_papers': data.get('research_papers', 0),
                'test_scores': data.get('test_scores', {}),
                'interests': data.get('interests', []),
                'target_degree': data.get('target_degree', '')
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in ResumeParserAgent: {e}")
            print(f"Problematic text: {response_text}")
            return {}
        except Exception as e:
            print(f"Error in ResumeParserAgent: {e}")
            import traceback
            traceback.print_exc()
            return {}
