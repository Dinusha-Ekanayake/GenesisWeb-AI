from fastapi import APIRouter
from .genesis_controller import router as genesis_router
from .auth_controller import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(genesis_router)
