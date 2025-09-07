from fastapi import FastAPI
from app.api import all_routers

app = FastAPI(title="Password Manager API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

# Include all API routers
for router in all_routers:
    app.include_router(router)
