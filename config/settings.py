import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
    DATABASE_URL = f"postgresql+psycopg2://postgres.mqoswcczyvcilfesekbd:{SUPABASE_DB_PASSWORD}@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

settings = Settings()
