from fastapi import APIRouter, HTTPException
from models.schemas import PRRequest

router = APIRouter()

@router.post("/analyze-pr")
async def analyze_pr(request: PRRequest):
    # calling Celery task here
    return {
        "message": "PR request received",
        "repo_url": request.repo_url,
        "pr_number": request.pr_number
    }