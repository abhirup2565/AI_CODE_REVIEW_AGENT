from fastapi import FastAPI
from .routers import router_auth,router_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Code Review Agent")
app.include_router(router_api)
app.include_router(router_auth)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)