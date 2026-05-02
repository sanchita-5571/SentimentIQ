from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import create_access_token, decode_token
from db.sql_models import UserRecord
from db.sqlite import get_db_session
from models.user import User
from schemas.auth import LoginRequest, TokenResponse, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


# Dummy user for local-only access (no authentication required)
DUMMY_USER = User(
    _id="local-user",
    email="local@localhost",
    full_name="Local User",
    hashed_password="",
    is_active=True,
    created_at=datetime.now(),
    updated_at=datetime.now(),
)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: Session = Depends(get_db_session),
) -> User:
    # Allow local dev access - always return dummy user
    # This bypasses all token validation for local development
    return DUMMY_USER


async def get_current_active_user(
    token: str | None = Depends(oauth2_scheme),
    session: Session = Depends(get_db_session),
) -> User:
    # Allow local dev access - always return dummy user
    return DUMMY_USER


# Legacy endpoints (no-op for backwards compatibility)
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    session: Session = Depends(get_db_session),
) -> UserResponse:
    return UserResponse.model_validate(DUMMY_USER)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    session: Session = Depends(get_db_session),
) -> TokenResponse:
    # No authentication required - always return dummy user
    token = create_access_token(DUMMY_USER.id)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(DUMMY_USER),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return DUMMY_USER
