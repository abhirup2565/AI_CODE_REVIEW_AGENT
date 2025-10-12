from backend.app.services.celery_tasks import analyze_pr_task
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.app.services.auth_service import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    return payload["sub"]

def initiate_analyze_pr(request):
    """
    Trigger Celery background task
    """
    task = analyze_pr_task.delay(request.repo_url, request.pr_number, request.github_token)
    return {"task_id": task.id, "status": "submitted"}