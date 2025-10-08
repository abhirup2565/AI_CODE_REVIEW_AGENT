from fastapi import APIRouter, HTTPException
from models.schemas import PRRequest
from workers.tasks import analyze_pr_task
from celery.result import AsyncResult
from workers.tasks import celery_app
from database.database import SessionLocal
from database.models import TaskResult, FileAnalysis
from database.schemas import TaskResultResponse, AnalysisResult, FileResult, Issue, Summary

router = APIRouter()

@router.post("/analyze-pr")
async def analyze_pr(request: PRRequest):
    # Trigger Celery background task
    task = analyze_pr_task.delay(request.repo_url, request.pr_number, request.github_token)
    return {"task_id": task.id, "status": "submitted"}


@router.get("/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    print(result)
    return {"task_id": task_id, "state": result.state, "meta": result.info}


@router.get("/results/{task_id}", response_model=TaskResultResponse)
def get_results(task_id: str):
    db = SessionLocal()
    task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    files = []
    for f in task.files:
        issues = [Issue(**i) for i in f.issues]
        files.append(FileResult(name=f.file_name, issues=issues))
    summary = Summary(**task.summary)
    db.close()

    return TaskResultResponse(task_id=task_id, status=task.status, results=AnalysisResult(files=files, summary=summary))
    