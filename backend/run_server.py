import os
import sys
import uvicorn

# Get the absolute path of the project root (parent of backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Add project root to sys.path so "backend" becomes importable
sys.path.append(PROJECT_ROOT)

from backend.app.main import app 

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=False)
