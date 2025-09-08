from fastapi import APIRouter, status
from app.core.register_user import register_user
from app.core.login import authenticate
from app.domain.auth import User, RegistrationPayload, LoginPayload

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {"status": "ok"}


@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginPayload):
    return authenticate(payload.email, payload.password)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegistrationPayload):
    return register_user(payload.email, payload.password, payload.confirmation)
