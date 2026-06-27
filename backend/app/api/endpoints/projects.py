from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from ...db.session import get_db
from ...schemas.project import ProjectCreate, ProjectResponse
from ...crud import crud_project
from ...core.workspace import WorkspaceManager

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new project.
    This initializes the database record and generates the physical workspace directories.
    """
    # 1. Save to Database
    project = await crud_project.create_project(db=db, project_in=project_in)
    
    # 2. Initialize Physical Workspace
    try:
        WorkspaceManager.create_project_workspace(str(project.id))
    except Exception as e:
        # If disk creation fails, log the error. In full production, rollback DB state.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize workspace directories: {str(e)}"
        )
        
    return project

@router.get("/", response_model=List[ProjectResponse])
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all projects.
    """
    projects = await crud_project.get_projects(db=db, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def read_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific project by ID.
    """
    project = await crud_project.get_project(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
