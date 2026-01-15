from fastapi import FastAPI
from api import router as api_router
from auth.routes import router as auth_router

app = FastAPI(title="CTI IDS API")

app.include_router(auth_router, prefix="/api/auth")
app.include_router(api_router, prefix="/api")
