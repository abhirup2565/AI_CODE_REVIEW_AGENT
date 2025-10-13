from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from .analyze_pr import initiate_analyze_pr
from .status import get_status
from .result import get_result
from .user_tasks import get_user_tasks
from pydantic import BaseModel
from typing import Optional
from backend.app.routers.auth.dependencies import get_current_user
from backend.app.database.db import get_db

router_api = APIRouter(prefix="/api", tags=["API"])

# Review: change name and location
class PRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

@router_api.post("/analyze-pr")
async def analyze_pr(request:PRRequest, current_user=Depends(get_current_user)):
    return initiate_analyze_pr(request,current_user.id)

@router_api.get("/user_tasks")
async def user_tasks(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_user_tasks(db,current_user.id)    

@router_api.get("/status/{task_id}")
async def status(task_id: str, current_user=Depends(get_current_user)):
    return get_status(task_id)

@router_api.get("/results/{task_id}")
async def result(task_id: str, current_user=Depends(get_current_user), db:Session=Depends(get_db)):
    return get_result(task_id,db)