from celery import Celery
from services.github_service import get_pr_files
from services.ai_agent_sevice import analyze_pr_files
from celery import Celery,shared_task
from workers.utils.formatters import format_analysis_result
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
    # Step 1: Fetch PR files
    self.update_state(state="PROGRESS", meta={"progress": "fetching PR files"})
    pr_files = get_pr_files(repo_url, pr_number, github_token)
    if not pr_files:
        return {"status": "no_files", "message": "No files found in PR."}

    self.update_state(state="PROGRESS", meta={"progress": f"{len(pr_files)} files fetched"})

    # Step 2: Run AI analysis
    self.update_state(state="PROGRESS", meta={"progress": "running AI analysis"})
    analysis_results = analyze_pr_files(pr_files)  # Already a dict from Pydantic model

    # Step 3: Return results directly
    # LLM already provides 'results' with 'files' and 'summary'
    return analysis_results



    #storing in db
    #for task
    # db = SessionLocal()
    # task_record = TaskResult(
    #     task_id=self.request.id,
    #     status="completed",
    #     summary={
    #         "total_files": total_files,
    #         "total_issues": total_issues,
    #         "critical_issues": critical_issues
    #     }
    # )
    # db.add(task_record)
    # db.commit()
    # db.refresh(task_record)

    # # for files
    # for f in analysis_results:
    #     file_record = FileAnalysis(
    #         task_id=task_record.id,
    #         file_name=f["file"],
    #         issues=f["analysis"]
    #     )
    #     db.add(file_record)
    # db.commit()
    # db.close()
    #return {"status": "completed"}

# Skip DB operations for now
    return {
        "status": "completed",
        "summary": {
            "total_files": total_files,
            "total_issues": total_issues,
            "critical_issues": critical_issues
        },
        "details": analysis_results
    }