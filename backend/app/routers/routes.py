from fastapi import APIRouter
from .analyze_pr import initiate_analyze_pr
from .status import get_status
from .result import get_result
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class PRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

@router.post("/analyze-pr")
async def analyze_pr(request:PRRequest):
    return initiate_analyze_pr(request)
    
@router.get("/status/{task_id}")
async def status(task_id: str):
    return get_status(task_id)

@router.get("/results/{task_id}")
async def result(task_id: str):
    return get_result(task_id)