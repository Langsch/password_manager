import uuid
import json
from pydantic import BaseModel

class Vault(BaseModel):
    id: int
    user_id: uuid.UUID
    passphrase: str
    password: str
    metadata: json.JSONDecoder
