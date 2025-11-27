import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from orchestrator import Orchestrator

app = FastAPI(title="MS Application Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class StudentProfileRequest(BaseModel):
    gpa: float
    target_degree: str
    target_countries: List[str]
    budget: str
    interests: List[str]
    target_intake: str
    test_scores: Optional[Dict[str, str]] = None

from fastapi.responses import StreamingResponse
import json
import asyncio

# API Endpoint
@app.post("/api/generate-plan-stream")
async def generate_plan_stream(profile: StudentProfileRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")

    async def event_generator():
        try:
            # Convert Pydantic model to dict for Orchestrator
            student_data = profile.model_dump()
            
            # Initialize Orchestrator
            orchestrator = Orchestrator()
            
            # Run Agent Workflow (Generator)
            for update in orchestrator.run(student_data):
                # Helper to serialize Pydantic models
                def pydantic_encoder(obj):
                    if hasattr(obj, 'dict'):
                        return obj.dict()
                    return str(obj)

                # Yield SSE format
                yield f"data: {json.dumps(update, default=pydantic_encoder)}\n\n"
                # Small delay to ensure UI updates are visible
                await asyncio.sleep(0.1)
                
        except Exception as e:
            error_msg = {"type": "error", "message": str(e)}
            yield f"data: {json.dumps(error_msg)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Legacy Endpoint (Optional, kept for compatibility if needed)
@app.post("/api/generate-plan")
async def generate_plan(profile: StudentProfileRequest):
    # ... implementation ...
    pass

# Serve Static Files (Frontend)
# Ensure static directory exists
os.makedirs("static", exist_ok=True)
# Mount static files at root must be last to avoid shadowing API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
