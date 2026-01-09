"""
Submission Endpoints
Handle code submission and execution in the sandbox.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.grader.runner import run_code_in_sandbox


router = APIRouter()


class SubmissionRequest(BaseModel):
    code: str
    language: str = "python"
    lab_id: Optional[str] = None


class SubmissionResponse(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: Optional[float] = None


@router.post("/run", response_model=SubmissionResponse)
async def run_code(request: SubmissionRequest):
    """
    Execute code in a secure sandbox environment.
    Returns stdout/stderr and execution status.
    """
    try:
        result = await run_code_in_sandbox(
            code=request.code,
            language=request.language
        )
        
        return SubmissionResponse(
            success=result["success"],
            output=result["output"],
            error=result.get("error"),
            execution_time=result.get("execution_time")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution error: {str(e)}"
        )


@router.post("/submit")
async def submit_code(request: SubmissionRequest):
    """
    Submit code for grading.
    Runs tests and returns results.
    """
    # Run the code first
    result = await run_code_in_sandbox(
        code=request.code,
        language=request.language
    )
    
    # TODO: Add test case execution and grading logic
    
    return {
        "submission_id": "demo-submission-001",
        "status": "completed",
        "execution_result": result,
        "tests_passed": 0,
        "tests_total": 0,
        "feedback": "Submission received. Test grading not yet implemented."
    }
