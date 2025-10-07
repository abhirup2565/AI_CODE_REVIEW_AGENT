from fastapi import APIRouter, HTTPException
from models.schemas import PRRequest
from workers.tasks import analyze_pr_task
from celery.result import AsyncResult
from workers.tasks import celery_app

router = APIRouter()

@router.post("/analyze-pr")
async def analyze_pr(request: PRRequest):
    # Trigger Celery background task
    task = analyze_pr_task.delay(request.repo_url, request.pr_number, request.github_token)
    return {"task_id": task.id, "status": "submitted"}


@router.get("/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "state": result.state, "meta": result.info}


@router.get("/results/{task_id}")
async def get_results(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.ready():
        return {"task_id": task_id, "result": result.get()}
    return {"task_id": task_id, "status": "pending"}