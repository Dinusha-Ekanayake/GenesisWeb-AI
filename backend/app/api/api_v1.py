from fastapi import APIRouter
from .endpoints import projects
from .genesis_controller import router as genesis_router

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(genesis_router)
