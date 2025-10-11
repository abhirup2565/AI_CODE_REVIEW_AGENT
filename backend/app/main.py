from fastapi import FastAPI
from .routers import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Code Review Agent")
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)