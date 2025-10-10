from pydantic import BaseModel
from typing import List, Optional

class Issue(BaseModel):
    type: str
    line: int
    description: str
    suggestion: str

class FileResult(BaseModel):
    name: str
    issues: List[Issue]

class Summary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int

class AnalysisResult(BaseModel):
    files: List[FileResult]
    summary: Summary

class TaskResultResponse(BaseModel):
    task_id: str
    status: str
    results: Optional[AnalysisResult]
