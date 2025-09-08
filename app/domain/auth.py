from pydantic import BaseModel

class RegistrationPayload(BaseModel):
    email: str
    password: str
    confirmation: str

class User(BaseModel):
    id: int
    email: str
    password: str
    created_at: str  # Or use datetime if you have proper types

class LoginPayload(BaseModel):
    email: str
    password: str
