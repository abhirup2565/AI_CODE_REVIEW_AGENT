from fastapi import APIRouter,Depends
from .analyze_pr import initiate_analyze_pr,get_current_user
from .status import get_status
from .result import get_result
from pydantic import BaseModel
from typing import Optional

router_api = APIRouter(prefix="/api", tags=["API"])

class PRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

@router_api.post("/analyze-pr")
async def analyze_pr(request:PRRequest, user=Depends(get_current_user)):
    return initiate_analyze_pr(request)
    
@router_api.get("/status/{task_id}")
async def status(task_id: str):
    return get_status(task_id)

@router_api.get("/results/{task_id}")
async def result(task_id: str):
    return get_result(task_id)