from fastapi import APIRouter, status
from app.core.create_vault import create_vault
from app.domain.vault import VaultCreationPayload

router = APIRouter(prefix="/vault", tags=["vault"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_vault(payload: VaultCreationPayload):
    return create_vault(payload.user_id, payload.passphrase)
