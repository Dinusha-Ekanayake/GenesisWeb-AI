from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class Permission(str, Enum):
    COMPILE = "compile"
    VALIDATE = "validate"
    DEPLOY = "deploy"
    DOWNLOAD_ARTIFACTS = "download_artifacts"
    READ_WORKSPACE = "read_workspace"
    MANAGE_PROJECTS = "manage_projects"
    MANAGE_USERS = "manage_users"

class User(BaseModel):
    username: str
    password_hash: str
    permissions: List[Permission]

class UserRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> Optional[User]:
        pass
