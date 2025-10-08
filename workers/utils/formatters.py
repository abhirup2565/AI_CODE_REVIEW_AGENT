def format_analysis_result(task_id, files=None, summary=None, status="completed", error=None):
    """
    Ensures all analysis results follow the same structured format.
    """
    if error:
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(error),
            "results": None
        }

    return {
        "task_id": task_id,
        "status": status,
        "results": {
            "files": files or [],
            "summary": summary or {
                "total_files": 0,
                "total_issues": 0,
                "critical_issues": 0
            }
        }
    }
