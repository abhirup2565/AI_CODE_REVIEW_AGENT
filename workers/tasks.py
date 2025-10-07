from celery import Celery
import time

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

@celery_app.task(bind=True)
def analyze_pr_task(self,repo_url: str, pr_number: int, github_token: str = None):
    """
    Dummy long-running PR analysis simulation.
    """
    self.update_state(state="PROGRESS", meta={"progress": "fetching PR files"})
    time.sleep(2)  # simulate network delay
    self.update_state(state="PROGRESS", meta={"progress": "analyzing code"})
    time.sleep(3)
    return {
        "status": "completed",
        "repo_url": repo_url,
        "pr_number": pr_number,
        "summary": f"Analysis of PR #{pr_number} done successfully!"
    }