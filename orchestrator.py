import json
from typing import Dict, Any, Generator
from dataclasses import asdict
from utils.gemini_client import GeminiClient
from agents.profile_intake import ProfileIntakeAgent
from agents.program_search import ProgramSearchAgent
from agents.requirements_parser import RequirementsParserAgent
from agents.timeline_planner import TimelinePlannerAgent
from agents.checklist_validator import ChecklistValidatorAgent
from models import StudentProfile, Program, ProgramRequirements, Task
import requests
from bs4 import BeautifulSoup
from googlesearch import search

class Orchestrator:
    def __init__(self):
        self.client = GeminiClient()
        self.profile_agent = ProfileIntakeAgent(self.client)
        self.search_agent = ProgramSearchAgent(self.client)
        self.requirements_agent = RequirementsParserAgent(self.client)
        self.timeline_agent = TimelinePlannerAgent(self.client)
        self.validator_agent = ChecklistValidatorAgent(self.client)

    def _fetch_program_details_real(self, program: Program) -> str:
        """
        Uses Google Search to find the program page and extracts text.
        """
        query = f"{program.university} {program.name} admission requirements"
        try:
            # Search for the first result
            results = list(search(query, num_results=1, advanced=True))
            if not results:
                return "No results found."
            
            url = results[0].url
            
            # Fetch page content
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Extract text
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
                
            text = soup.get_text()
            
            # Clean up text (simple)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit length for Gemini
            return text[:10000] 
            
        except Exception as e:
            # Fall back to mock data if scraping fails
            return self._fetch_program_details_mock(program)

    def _fetch_program_details_mock(self, program: Program) -> str:
        """
        Simulates fetching program details page content.
        """
        prompt = f"""
        Generate a realistic 'Admission Requirements' page text for:
        Program: {program.name}
        University: {program.university}
        Country: {program.country}
        
        Include details about SOP, LORs (how many), standardized tests (GRE/TOEFL scores), 
        transcripts, and any specific deadlines or special notes.
        Make it look like raw text copied from a website.
        """
        return self.client.generate_content(prompt)

    def run(self, student_data: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        yield {"type": "status", "agent": "ProfileIntake", "message": "Analyzing student profile..."}
        
        # 1. Process Profile
        profile = self.profile_agent.process(student_data)
        yield {"type": "status", "agent": "ProgramSearch", "message": f"Searching programs for {profile.target_degree}..."}

        # 2. Search Programs
        programs = self.search_agent.search(profile)
        yield {"type": "status", "agent": "ProgramSearch", "message": f"Found {len(programs)} top matches."}

        results = {
            "profile": profile,
            "shortlist": []
        }

        # 3. Process each program
        for i, prog in enumerate(programs):
            yield {"type": "status", "agent": "RequirementsParser", "message": f"Fetching requirements for {prog.university}..."}
            
            try:
                # Fetch details (Real or Mock)
                raw_text = self._fetch_program_details_real(prog)
                
                # Parse Requirements
                yield {"type": "status", "agent": "RequirementsParser", "message": f"Extracting requirements for {prog.name}..."}
                reqs = self.requirements_agent.parse(prog.name, raw_text)
                
                # Plan Timeline
                yield {"type": "status", "agent": "TimelinePlanner", "message": f"Planning timeline for {prog.university}..."}
                timeline = self.timeline_agent.plan(profile, prog, reqs)
                
                # Validate
                yield {"type": "status", "agent": "ChecklistValidator", "message": "Validating application plan..."}
                warnings = self.validator_agent.validate(timeline, reqs)
                
                prog_result = {
                    "program": asdict(prog),
                    "requirements": asdict(reqs),
                    "timeline": [asdict(t) for t in timeline],
                    "warnings": warnings
                }
                results["shortlist"].append(prog_result)
            except Exception as e:
                # Log error but continue processing other programs
                results["shortlist"].append({
                    "program": asdict(prog),
                    "error": str(e)
                })

        # Convert profile to dict as well
        results["profile"] = asdict(profile)
        yield {"type": "result", "data": results}
