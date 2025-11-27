import json
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from models import StudentProfile, Program, ProgramRequirements, Task
from utils.gemini_client import GeminiClient

class TaskSchema(BaseModel):
    title: str
    description: str
    due_date: str = Field(description="ISO date string YYYY-MM-DD")
    dependency: Optional[str] = Field(description="Task that must be done before this one, or None")

class TimelineSchema(BaseModel):
    tasks: List[TaskSchema]

class TimelinePlannerAgent:
    def __init__(self, client: GeminiClient):
        self.client = client

    def plan(self, profile: StudentProfile, program: Program, requirements: ProgramRequirements) -> List[Task]:
        """
        Generates a timeline of tasks for a specific program application.
        """
        today = date.today().isoformat()
        
        prompt = f"""
        You are a project manager for college applications.
        Create a detailed timeline of tasks for applying to:
        Program: {program.name} at {program.university}
        Deadline: {program.application_deadline}
        Today's Date: {today}
        
        Requirements:
        {requirements}
        
        Student Profile Context:
        {profile}
        
        Generate a list of tasks with due dates working backwards from the deadline.
        Include tasks for drafting SOPs, getting LORs, taking tests (if needed), and final submission.
        """

        try:
            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=TimelineSchema
            )
            data = json.loads(response_text)
            tasks = []
            for t_data in data.get('tasks', []):
                tasks.append(Task(**t_data))
            return tasks
        except Exception as e:
            print(f"Error in TimelinePlannerAgent: {e}")
            return [Task(title="Error", description="Failed to generate timeline", due_date=program.application_deadline)]
