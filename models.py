from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class StudentProfile:
    gpa: float
    target_degree: str
    target_countries: List[str]
    budget: str
    interests: List[str]
    target_intake: str
    undergrad_major: str = ""
    work_experience_years: float = 0.0
    backlogs: int = 0
    research_papers: int = 0
    test_scores: Optional[Dict[str, str]] = None

@dataclass
class Program:
    name: str
    university: str
    country: str
    tuition_range: str
    application_deadline: str
    eligibility_criteria: str
    match_reasoning: Optional[str] = None

@dataclass
class ProgramRequirements:
    program_name: str
    required_documents: List[str]
    test_requirements: List[str]
    special_notes: Optional[str] = None

@dataclass
class Task:
    title: str
    description: str
    due_date: str
    dependency: Optional[str] = None
    status: str = "Pending"

@dataclass
class QNAPair:
    """Q&A pair for curated student questions"""
    question: str  # Max 30 characters
    answer: str    # Max 30 words
    category: str  # e.g., "germany", "tests", "documents", "visa"
    status: str = "Pending"

@dataclass
class AgentOutput:
    success: bool
    data: any
    error: Optional[str] = None
