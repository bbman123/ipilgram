from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.api.deps import get_current_user
from app.models.user import User, Role
from app.models.refresh_token import RefreshToken
from app.schemas.auth import (
    RefreshRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserRegister, db: Annotated[Session, Depends(get_db)]):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    user = User(
        email=body.email,
        full_name=body.full_name,
        hashed_password=hash_password(body.password),
        role=Role.pilgrim,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token, expires_at = create_refresh_token(data={"sub": user.id})

    db_token = RefreshToken(
        token=refresh_token, user_id=user.id, expires_at=str(expires_at)
    )
    db.add(db_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Annotated[Session, Depends(get_db)]):
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == body.refresh_token)
        .first()
    )
    if db_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked"
        )

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive"
        )

    db.delete(db_token)
    db.commit()

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token, expires_at = create_refresh_token(data={"sub": user.id})

    new_db_token = RefreshToken(
        token=refresh_token, user_id=user.id, expires_at=str(expires_at)
    )
    db.add(new_db_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    body: RefreshRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == body.refresh_token,
            RefreshToken.user_id == current_user.id,
        )
        .first()
    )
    if db_token:
        db.delete(db_token)
        db.commit()


@router.get("/me", response_model=UserResponse)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
