from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(title="AI Code Review Agent")
app.include_router(api_router)
