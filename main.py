from fastapi import FastAPI
from api.routes import router as api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_app")  # custom name

logger.info("This will always show")


app = FastAPI(title="AI Code Review Agent")
app.include_router(api_router)
