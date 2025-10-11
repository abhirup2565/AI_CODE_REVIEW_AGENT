from celery.result import AsyncResult
from backend.app.services.celery_tasks import celery_app

def get_status(task_id: str):
    """
    Fetches status of ongoing Celergy Operation Using task_id
    """
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "state": result.state, "meta": result.info}