from fastapi import APIRouter
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import user
from app.api.v1.endpoints import block

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(block.router)
