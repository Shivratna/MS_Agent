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
        from datetime import datetime, timedelta
        
        today = date.today()
        today_str = today.isoformat()
        
        # Parse the deadline
        try:
            deadline = datetime.strptime(program.application_deadline, "%Y-%m-%d").date()
        except:
            deadline = today + timedelta(days=180)  # Default to 6 months if parsing fails
        
        # Calculate minimum time needed (4 months for a typical application)
        min_time_needed = timedelta(days=120)
        time_until_deadline = deadline - today
        
        # Check if deadline has passed or not enough time
        intake_adjusted = False
        original_deadline = program.application_deadline
        
        if time_until_deadline.days < 0:
            # Deadline has passed - move to next year's intake
            deadline = deadline.replace(year=deadline.year + 1)
            intake_adjusted = True
            adjustment_reason = f"The {original_deadline} deadline has already passed"
        elif time_until_deadline < min_time_needed:
            # Not enough time - move to next intake
            deadline = deadline.replace(year=deadline.year + 1)
            intake_adjusted = True
            adjustment_reason = f"Only {time_until_deadline.days} days until the {original_deadline} deadline - not enough time for a complete application"
        
        adjusted_deadline = deadline.isoformat()
        
        prompt = f"""
        You are an expert application advisor creating a realistic, backward-planned timeline.
        
        **CRITICAL RULES:**
        1. ALL task dates MUST be BETWEEN today ({today_str}) and the deadline ({adjusted_deadline})
        2. NO dates in the past - today is {today_str}
        3. Work BACKWARDS from the deadline - final tasks should be closest to the deadline
        4. Be realistic about how long each task takes (e.g., getting LORs takes 2-4 weeks)
        5. Build in buffer time before the deadline (submit at least 2-3 days early)
        6. Tasks should be in CHRONOLOGICAL ORDER (earliest date first)
        
        **Application Details:**
        - Program: {program.name} at {program.university}
        - Application Deadline: {adjusted_deadline}
        - Today's Date: {today_str}
        - Days Available: {(deadline - today).days} days
        
        **Requirements:**
        - Required Documents: {requirements.required_documents if requirements.required_documents else 'Standard documents (transcripts, CV, SOP, LORs)'}
        - Test Requirements: {requirements.test_requirements if requirements.test_requirements else 'Check if GRE/TOEFL needed'}
        - Special Notes: {requirements.special_notes if requirements.special_notes else 'None'}
        
        **Student Context:**
        - GPA: {profile.gpa}
        - Target Degree: {profile.target_degree}
        - Test Scores: {profile.test_scores if profile.test_scores else 'None provided - may need to schedule tests'}
        
        **Generate a timeline with tasks in chronological order (earliest first).** Include:
        - Verifying specific requirements (if special_notes mentions checking official sources)
        - Obtaining transcripts and certificates (2-3 weeks)
        - Preparing CV/Resume (1-2 weeks)
        - Drafting and finalizing Statement of Purpose (3-4 weeks total)
        - Requesting and receiving Letters of Recommendation (plan 4-6 weeks from request to receipt)
        - Taking required tests (only if test_requirements lists them OR student hasn't provided scores)
        - Completing online application (1 week)
        - Final review and submission (2-3 days before deadline)
        
        **Important:** 
        - Only include tasks that are actually required
        - Ensure ALL dates are between {today_str} and {adjusted_deadline}
        - If a task would need to start before today, start it today or as soon as possible
        """

        try:
            response_text = self.client.generate_content(
                prompt=prompt,
                response_schema=TimelineSchema
            )
            data = json.loads(response_text)
            tasks = []
            
            for t_data in data.get('tasks', []):
                task = Task(**t_data)
                # Validate task date
                try:
                    task_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    if task_date < today:
                        # If task is in the past, move it to today
                        task.due_date = today_str
                    elif task_date > deadline:
                        # If task is after deadline, move it to deadline
                        task.due_date = adjusted_deadline
                except:
                    pass  # Keep original date if parsing fails
                
                tasks.append(task)
            
            # If we adjusted the intake, add a warning task
            if intake_adjusted:
                warning_task = Task(
                    title=f"⚠️ Intake Adjusted to {adjusted_deadline}",
                    description=f"{adjustment_reason}. We've automatically planned for the next intake cycle ({adjusted_deadline}). Please verify this date with the university.",
                    due_date=today_str,
                    dependency=None
                )
                tasks.insert(0, warning_task)
            
            return tasks
            
        except Exception as e:
            print(f"Error in TimelinePlannerAgent: {e}")
            return [Task(
                title="Error", 
                description=f"Failed to generate timeline: {str(e)}", 
                due_date=adjusted_deadline
            )]
