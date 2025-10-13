import requests
from typing import List,Dict

def get_pr_files(repo_url: str, pr_number: int, token: str = None) -> List[Dict]:
    """
    Convert repo URL → API endpoint
    """
    parts = repo_url.replace("https://github.com/", "").split("/") #Review: error catching Regex
    owner, repo = parts[0], parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "My-Celery-App"  # can be any string
    }
    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    files = response.json()

    ## Extract key information for each file
    # Return a list of dicts with filename and patch (diff)
    pr_files = []
    for file in files: #Review: Try Path Library
        pr_files.append({
            "filename": file["filename"],
            "extension": file["filename"].split(".")[-1],
            "status": file["status"],   # added, modified, removed
            "content": file.get("patch",None)  # the diff as string else empty
        })
    return pr_files
