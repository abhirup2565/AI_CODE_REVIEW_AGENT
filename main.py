from fastapi import FastAPI
from api.routes import router as api_router
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_app")  # custom name

logger.info("This will always show")


app = FastAPI(title="AI Code Review Agent")
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)