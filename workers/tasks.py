from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def analyze_pr_task(repo_url: str, pr_number: int, github_token: str = None):
    # Placeholder for actual AI review logic
    print(f"Analyzing PR #{pr_number} from {repo_url}")
    return {"status": "completed", "details": "Analysis done!"}