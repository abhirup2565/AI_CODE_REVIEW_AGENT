from pydantic import BaseModel, Field
from typing import List, Optional

#   Define Pydantic PR_Models
class Issue(BaseModel):
    type: str = Field(..., description="Type of issue, e.g., 'bug', 'style', 'performance'")
    line: int = Field(..., description="Line number of the issue")
    description: str = Field(..., description="Brief description of the issue")
    suggestion: Optional[str] = Field(None, description="Optional suggestion for improvement")


class FileAnalysis(BaseModel):
    name: str
    issues: List[Issue]


class Summary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int


class AnalysisResult(BaseModel):
    files: List[FileAnalysis]
    summary: Summary


class PRResponse(BaseModel):
    task_id: str
    status: str
    results: AnalysisResult