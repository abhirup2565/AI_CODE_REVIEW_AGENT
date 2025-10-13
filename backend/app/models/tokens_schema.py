from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    refresh_expires_at: datetime

class TokenPayload(BaseModel):
    sub: Optional[int]
    exp: Optional[int]
    jti: Optional[str]

    # class Config:
    #     orm_mode = True
