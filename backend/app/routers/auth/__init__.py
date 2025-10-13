# backend/app/routers/auth.py
from fastapi import APIRouter, HTTPException,Response,Request ,Depends
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from backend.app.models.user_models import UserCreate, UserLogin
from backend.app.models import RefreshToken,BlockedAccessToken,TokenPair
from backend.app.services import  auth_service
from backend.app.models.user_models import User
from backend.app.database.db import get_db
from backend.app.config import settings
from backend.app.routers.auth.dependencies import get_current_user

router_auth = APIRouter(prefix="/auth", tags=["Authentication"])

@router_auth.post("/register")
async def register_user(user: UserCreate):
    existing = User.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(email=user.email)
    new_user.set_password(user.password)
    new_user.create()
    return {"message": "User created successfully", "email": new_user.email}

@router_auth.post("/login")
async def login_user(user: UserLogin,response: Response,response_model=TokenPair,db:Session=Depends(get_db)):
    db_user = User.get_by_email(user.email)
    if not db_user or not db_user.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = auth_service.create_access_token({"sub": str(db_user.id)})
    refresh_token, refresh_jti, refresh_exp = auth_service.create_refresh_token({"sub": str(db_user.id)})
    # Persist refresh token so it can be revoked later
    rt = RefreshToken(jti=refresh_jti, user_id=db_user.id, expires_at=refresh_exp, revoked=False)
    db.add(rt)
    db.commit()

    # Set refresh token in cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # set False for local dev, True in production (HTTPS)
        samesite="strict",  # or "lax" if cross-domain refresh needed
        max_age= int(settings.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60 * 60,
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_exp
    )

@router_auth.post("/refresh")
def refresh(request: Request, response: Response,db:Session=Depends(get_db), response_model=TokenPair):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found")
    payload = auth_service.verify_token(refresh_token)
    jti = payload.get("jti")
    sub = payload.get("sub")
    if not jti or not sub:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Check refresh token in DB
    stored = db.query(RefreshToken).filter_by(jti=jti, user_id=int(sub)).first()
    if not stored or stored.revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked or expired")

    # Rotate refresh token: revoke old and create a new one
    stored.revoked = True
    db.add(stored)

    new_access_token = auth_service.create_access_token({"sub": str(sub)})
    new_refresh_token, new_refresh_jti, new_refresh_exp = auth_service.create_refresh_token({"sub": str(sub)})

    new_rt = RefreshToken(jti=new_refresh_jti, user_id=int(sub), expires_at=new_refresh_exp, revoked=False)
    db.add(new_rt)
    db.commit()

    # Replace cookie with new one
    # compute max_age in seconds
    max_age_seconds = int((new_refresh_exp - datetime.now(timezone.utc)).total_seconds())
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=max_age_seconds,
    )

    return TokenPair(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        refresh_expires_at=new_refresh_exp
    )

@router_auth.post("/logout")
def logout(request: Request, response: Response,db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token. Please login again")
    
    payload = auth_service.verify_token(refresh_token)
    jti = payload.get("jti")
    sub = payload.get("sub")
    stored = db.query(RefreshToken).filter_by(jti=jti, user_id=int(sub)).first()
    if stored:
        stored.revoked = True
        db.add(stored)

    access_token = request.headers.get("Authorization")
    if access_token:
        token_str = access_token.replace("Bearer ", "")
        payload = auth_service.verify_token(token_str)
        jti = payload.get("jti")
        blocked = BlockedAccessToken( jti = jti)
        db.add(blocked)

    try:   
        db.commit()
    except Exception as db_err:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error during logout: {db_err}")
    # delete the cookie
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out successfully"}
