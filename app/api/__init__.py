# Api endpoints
from .auth import router as auth_router
from .vault import router as vault_router

all_routers = [auth_router, vault_router]
