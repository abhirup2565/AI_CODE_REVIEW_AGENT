# database/create_tables.py
from .database import Base, engine
from .models import TaskResult, FileAnalysis

# This will create all tables in the database if they don't exist
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")