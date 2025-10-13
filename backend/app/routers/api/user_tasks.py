from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from backend.app.models import TaskResult

class User_Tasks_Response(BaseModel):
    task_id:str
    status:str

def get_user_tasks(db:Session ,user_id: int) ->  List[User_Tasks_Response]:
    """
    Fetches all the task for individual users
    """
    tasks = db.query(TaskResult).filter_by(user_id=user_id).all()
    # Convert ORM objects to Pydantic models
    return [User_Tasks_Response(task_id=t.task_id, status=t.status) for t in tasks]

    