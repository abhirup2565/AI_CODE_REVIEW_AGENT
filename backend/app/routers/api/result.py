from fastapi import  HTTPException
from celery.result import AsyncResult
from backend.app.services.celery_tasks import celery_app
from backend.app.database.db import SessionLocal
from backend.app.models import TaskResult


import logging
logger = logging.getLogger("Results_API")
logger.setLevel(logging.INFO)

def get_result(task_id: str):
    """
    Fetch task result:
    1. Check Redis (Celery backend) first.
    2. If task is still processing, return 202.
    3. If not in Redis, fetch from Postgres and return.
    """
    # Step 1: Check Redis (Celery backend)
    async_result = AsyncResult(task_id, app=celery_app)

    if not async_result.ready():
        # Task still running
        raise HTTPException(
            status_code=202,
            detail="Task is under processing. Please check again later."
        )
    
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