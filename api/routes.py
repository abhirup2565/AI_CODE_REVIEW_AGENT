from fastapi import APIRouter, HTTPException
from models.schemas import PRRequest
from workers.tasks import analyze_pr_task
from celery.result import AsyncResult
from workers.tasks import celery_app
from database.database import SessionLocal
from database.models import TaskResult, FileAnalysis
from database.schemas import TaskResultResponse, AnalysisResult, FileResult, Issue, Summary
import logging

logger = logging.getLogger("ai_code_review_agent")
logger.setLevel(logging.INFO)
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
async def get_result(task_id: str):
    """
    Fetch task result:
    1. Check Redis (Celery backend) first.
    2. If task is still processing, return 202.
    3. If not in Redis, fetch from Postgres, cache in Redis via Celery backend, and return.
    """
    # Step 1: Check Redis (Celery backend)
    async_result = AsyncResult(task_id, app=celery_app)

    if not async_result.ready():
        # Task still running
        raise HTTPException(
            status_code=202,
            detail="Task is under processing. Please check again later."
        )
    
    elif async_result.ready() and async_result.result:
        # Task finished and result available in Redis
        return {"source": "redis", "task_id": task_id, "results": async_result.result}
    
    else:
        # Step 2: Fallback to Postgres
        db = SessionLocal()
        try:
            tasks = db.query(TaskResult).all()
            print("this is tasks id")
            logger.info("this is tasks id")
            for t in tasks:
                logger.info(f"Task ID: {t.task_id}")
            task_id = str(task_id.strip())
            task_entry = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
            if not task_entry:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found in Redis or Postgres"
                )

            # Transform files into desired JSON structure
            files_list = [
                {
                    "name": f.file_name,
                    "issues": f.issues  # Already JSON
                }
                for f in task_entry.files
            ]

            # Prepare summary
            summary = task_entry.summary or {
                "total_files": len(files_list),
                "total_issues": sum(len(f["issues"]) for f in files_list),
                "critical_issues": sum(
                    1 for f in files_list for i in f["issues"] if i.get("type") == "bug"
                )
            }

            response = {
                "task_id": task_entry.task_id,
                "status": task_entry.status,
                "results": {
                    "files": files_list,
                    "summary": summary
                }
            }

            # Step 3: Cache result in Redis via Celery backend
            # Use the backend API properly
            # celery_app.backend.store_result(
            #     task_id=task_id,
            #     result=response["results"],
            #     state="SUCCESS"
            # )

            return response

        finally:
            db.close()