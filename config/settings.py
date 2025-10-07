import os

class Settings:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

settings = Settings()
