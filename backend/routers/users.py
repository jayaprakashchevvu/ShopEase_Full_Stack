import hashlib
import os
import secrets
import shutil
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from email_service import send_reset_email
from modules import User
from pyd import ForgotPasswordRequest, ResetPasswordRequest, Token, UserCreate, UserResponse
from security import (
    create_access_token,
    get_admin_user,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": create_access_token({"sub": user.email}),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    return db.query(User).order_by(User.id).all()


@router.post("/profile-image")
def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    upload_folder = "uploads/profile"
    os.makedirs(upload_folder, exist_ok=True)

    extension = os.path.splitext(file.filename or "")[1].lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Use JPG, PNG or WebP images")

    filename = f"{current_user.id}{extension}"
    path = os.path.join(upload_folder, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_user.profile_image = f"/uploads/profile/{filename}"
    db.commit()
    db.refresh(current_user)

    return {"message": "Profile image uploaded successfully", "profile_image": current_user.profile_image}


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    message = "If an account exists with this email, a reset code has been sent."

    if not user:
        return {"message": message}

    code = f"{secrets.randbelow(1_000_000):06d}"
    user.reset_code_hash = hashlib.sha256(code.encode()).hexdigest()
    user.reset_code_expires = (
        datetime.now(timezone.utc) + timedelta(minutes=10)
    ).isoformat()
    db.commit()

    send_reset_email(user.email, code)
    return {"message": message}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not user.reset_code_hash or not user.reset_code_expires:
        raise HTTPException(status_code=400, detail="Invalid email or reset code")

    expires = datetime.fromisoformat(user.reset_code_expires)
    if datetime.now(timezone.utc) > expires:
        raise HTTPException(status_code=400, detail="Reset code has expired")

    code_hash = hashlib.sha256(request.code.encode()).hexdigest()
    if code_hash != user.reset_code_hash:
        raise HTTPException(status_code=400, detail="Invalid reset code")

    user.password = hash_password(request.new_password)
    user.reset_code_hash = None
    user.reset_code_expires = None
    db.commit()
    return {"message": "Password reset successfully"}
