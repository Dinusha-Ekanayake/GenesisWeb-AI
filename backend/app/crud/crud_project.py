from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import uuid

from ..models.project import Project, ProjectStatus
from ..schemas.project import ProjectCreate

async def get_project(db: AsyncSession, project_id: uuid.UUID) -> Optional[Project]:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalars().first()

async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
    result = await db.execute(select(Project).offset(skip).limit(limit))
    return list(result.scalars().all())

async def create_project(db: AsyncSession, project_in: ProjectCreate) -> Project:
    db_obj = Project(
        title=project_in.title,
        user_prompt=project_in.user_prompt,
        status=ProjectStatus.PENDING
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
