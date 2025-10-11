from celery import shared_task
from .pr_fetcher import get_pr_files
from .code_analysis import analyze_pr_files
from backend.app.celery_app import celery_app
from backend.app.database.db import SessionLocal
from backend.app.models import TaskResult, FileResult

celery_app = celery_app

@shared_task(bind=True)
def analyze_pr_task(self, repo_url: str, pr_number: int, github_token: str = None):
    """
    Fetch PR files, run AI analysis, and return structured results.
    """
    task_id = self.request.id
    db = SessionLocal()

    try:
        # Step 1: Fetch PR files
        self.update_state(state="PROGRESS", meta={"progress": "fetching PR files"})
        pr_files = get_pr_files(repo_url, pr_number, github_token)
        if not pr_files:
            return {"status": "no_files", "message": "No files found in PR."}

        self.update_state(state="PROGRESS", meta={"progress": f"{len(pr_files)} files fetched"})

        # Step 2: Run AI analysis
        self.update_state(state="PROGRESS", meta={"progress": "running AI analysis"})
        analysis_results = analyze_pr_files(task_id,pr_files)  # Already a dict from Pydantic model

        #Step 3: Storing in db
        #Storing PR data
        result_entry = TaskResult(
                task_id=analysis_results.get("task_id", task_id),
                status=analysis_results.get("status", "completed"),
                summary=analysis_results["results"]["summary"],
            )
        db.add(result_entry)
        db.commit()
        db.refresh(result_entry)
        #Storing individual file data
        for file_data in analysis_results["results"]["files"]:
            file_entry = FileResult(
                task_id=result_entry.id,
                file_name=file_data["name"],
                issues=file_data["issues"],
            )
            db.add(file_entry)
        db.commit()
        return {"status": "completed", "message": "Analysis is completed"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
