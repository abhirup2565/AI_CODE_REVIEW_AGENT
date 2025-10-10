from sqlalchemy import Column, Integer, String, JSON, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from database.database import Base

class TaskResult(Base):
    __tablename__ = "task_results"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    task_id = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    summary = Column(JSON, nullable=True)
    files = relationship("FileAnalysis", back_populates="task", cascade="all, delete")

class FileAnalysis(Base):
    __tablename__ = "file_analysis"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task_results.id"))
    file_name = Column(String,nullable=False)
    issues = Column(JSON, nullable=False)
    task = relationship("TaskResult", back_populates="files")