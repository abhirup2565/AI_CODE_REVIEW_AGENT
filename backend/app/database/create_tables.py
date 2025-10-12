# database/create_tables.py
from .db import Base, engine
from backend.app.models import TaskResult, FileResult , User, BlockedAccessToken, RefreshToken

# This will create all tables in the database if they don't exist
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")