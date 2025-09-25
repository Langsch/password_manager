import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel

class Vault(BaseModel):
    id: int
    user_id: uuid.UUID
    passphrase: str
    password: str
    metadata: Optional[Dict[str, Any]] = None  # Changed from json.JSONDecoder


class VaultCreationPayload(BaseModel):
    user_id: uuid.UUID
    passphrase: str
