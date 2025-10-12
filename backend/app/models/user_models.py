from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime,timezone
from pydantic import BaseModel, EmailStr
from werkzeug.security import generate_password_hash,check_password_hash
from backend.app.database.db import Base,SessionLocal

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    #Functions Related to db
    def __repr__(self):
        return f"<User {self.id}>"

    # Set password
    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    # Check password
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    # Save user
    def save(self):
        db = SessionLocal()
        try:
            db.add(self)
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    # Class method: get user by email
    @classmethod
    def get_by_email(cls, email: str):
        db = SessionLocal()
        try:
            return db.query(cls).filter(cls.email == email).first()
        finally:
            db.close()


# Pydantic Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
