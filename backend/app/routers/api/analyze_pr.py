from backend.app.services.celery_tasks import analyze_pr_task
from backend.app.models import User

def initiate_analyze_pr(request, current_user_id:int):
    """
    Trigger Celery background task
    """
    task = analyze_pr_task.delay(request.repo_url, request.pr_number, current_user_id,request.github_token)
    return {"task_id": task.id, "status": "submitted"}