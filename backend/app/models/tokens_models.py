# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from backend.app.database.db import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, nullable=False, index=True)  # JWT ID for token
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)   # helps cleanup expired tokens
    revoked = Column(Boolean, default=False, index=True)
    user = relationship("User", backref="refresh_tokens")
    
# access token blocklist 
class BlockedAccessToken(Base):
    __tablename__ = "blocked_access_tokens"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))