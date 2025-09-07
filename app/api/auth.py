from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/ping", status_code=status.HTTP_200_OK)
def ping():
    return {"status": "ok"}

@router.post("/login", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def login():
    return {"detail": "login not implemented yet"}
