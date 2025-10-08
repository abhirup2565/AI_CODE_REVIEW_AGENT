import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

settings = Settings()
