from backend.app.services.celery_tasks import analyze_pr_task

def initiate_analyze_pr(request):
    """
    Trigger Celery background task
    """
    task = analyze_pr_task.delay(request.repo_url, request.pr_number, request.github_token)
    return {"task_id": task.id, "status": "submitted"}