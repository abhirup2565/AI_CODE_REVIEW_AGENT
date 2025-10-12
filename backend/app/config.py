import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    SUPABASE_DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD")
    DATABASE_URL = f"postgresql+psycopg2://postgres.mqoswcczyvcilfesekbd:{SUPABASE_DB_PASSWORD}@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM=os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS=os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


settings = Settings()
