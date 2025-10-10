from celery import Celery
from services.github_service import get_pr_files
from services.ai_agent_sevice import analyze_pr_files
from celery import Celery,shared_task
from database.database import SessionLocal
from database.models import TaskResult, FileAnalysis

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# @celery_app.task(bind=True)
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
            file_entry = FileAnalysis(
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
