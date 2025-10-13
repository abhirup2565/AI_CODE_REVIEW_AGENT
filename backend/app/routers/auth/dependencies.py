# app/auth/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.app.database.db import get_db
from backend.app.models import BlockedAccessToken,User
from backend.app.services.auth_service import verify_token
from jose import JWTError

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing access token")

    token = auth_header.replace("Bearer ", "")

    try:
        payload = verify_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    jti = payload.get("jti")
    sub = payload.get("sub")

    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    blocked = db.query(BlockedAccessToken).filter_by(jti=jti).first()
    if blocked:
        raise HTTPException(status_code=401, detail="Access token revoked")
    
    current_user = db.query(User).filter_by(id=sub).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user

def guest_only(request: Request):
    """
    Allows access only if the user is NOT logged in.
    Checks for a valid access token in Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        try:
            payload = verify_token(token)
            # If token is valid, user is already logged in
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already logged in"
            )
        except JWTError:
            # Token invalid or expired → treat as guest
            pass
    # No token → OK to proceed
    return True