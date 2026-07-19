import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
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

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/auth", tags=["Auth"])

limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new pilgrim account",
    description="Create a new user account with pilgrim role. Email must be unique.",
    responses={
        201: {"description": "Account created successfully"},
        400: {"description": "Email already registered"},
        422: {"description": "Validation error"},
    },
)
@limiter.limit("5/minute")
def register(request: Request, body: UserRegister, db: Annotated[Session, Depends(get_db)]):
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
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and obtain tokens",
    description="Login with email and password to receive an access token and refresh token pair.",
    responses={
        200: {"description": "Login successful, tokens returned"},
        401: {"description": "Invalid email or password"},
        403: {"description": "Account is inactive"},
    },
)
@limiter.limit("10/minute")
def login(request: Request, body: UserLogin, db: Annotated[Session, Depends(get_db)]):
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
        token=hash_password(refresh_token),
        user_id=user.id,
        expires_at=expires_at,
    )
    db.add(db_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new access/refresh token pair. The old refresh token is revoked (rotation).",
    responses={
        200: {"description": "New token pair issued"},
        401: {"description": "Invalid, expired, or revoked refresh token"},
    },
)
def refresh(body: RefreshRequest, db: Annotated[Session, Depends(get_db)]):
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    user_id = int(payload.get("sub"))
    db_tokens = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).all()
    matched_token = None
    for dt in db_tokens:
        if verify_password(body.refresh_token, dt.token):
            matched_token = dt
            break

    if matched_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive"
        )

    db.delete(matched_token)
    db.commit()

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    refresh_token, expires_at = create_refresh_token(data={"sub": user.id})

    new_db_token = RefreshToken(
        token=hash_password(refresh_token),
        user_id=user.id,
        expires_at=expires_at,
    )
    db.add(new_db_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke refresh token",
    description="Invalidate a refresh token to log out. The access token remains valid until expiry.",
    responses={
        204: {"description": "Refresh token revoked successfully"},
        401: {"description": "Authentication required"},
    },
)
def logout(
    body: RefreshRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    db_tokens = db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id,
    ).all()
    for db_token in db_tokens:
        if verify_password(body.refresh_token, db_token.token):
            db.delete(db_token)
            db.commit()
            return


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the authenticated user's profile information.",
    responses={
        200: {"description": "User profile returned"},
        401: {"description": "Authentication required"},
    },
)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return UserResponse.model_validate(current_user)
