# Dependency: protect routes using access token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.app.database.db import SessionLocal
from models import User,BlockedAccessToken
from .auth_service import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # adapt if you use /login

def get_current_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal
    payload = verify_access_token(token)
    # optional: check access token blocklist for immediate revocation
    jti = payload.get("jti")
    if jti:
        blocked = db.query(BlockedAccessToken).filter_by(jti=jti).first()
        if blocked:
            raise HTTPException(status_code=401, detail="Token revoked")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter_by(id=int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user