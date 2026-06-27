import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from ..db.session import Base

class ProjectStatus(str, enum.Enum):
    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    DESIGNING = "DESIGNING"
    GENERATING = "GENERATING"
    TESTING = "TESTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    user_prompt = Column(Text, nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.PENDING)
    requirements = Column(JSONB, nullable=True)
    architecture = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
