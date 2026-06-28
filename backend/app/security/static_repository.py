from typing import Optional
from passlib.context import CryptContext
from backend.app.core.config import settings
from .repository import UserRepository, User, Permission

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StaticUserRepository(UserRepository):
    def __init__(self):
        # In a real app, these come from a DB or file.
        # For Phase 11.3, we bootstrap from settings.
        self._users = {
            settings.admin_bootstrap_username: User(
                username=settings.admin_bootstrap_username,
                password_hash=pwd_context.hash(settings.admin_bootstrap_password),
                permissions=[
                    Permission.COMPILE,
                    Permission.VALIDATE,
                    Permission.DEPLOY,
                    Permission.DOWNLOAD_ARTIFACTS,
                    Permission.READ_WORKSPACE,
                    Permission.MANAGE_PROJECTS,
                    Permission.MANAGE_USERS
                ]
            ),
            "developer": User(
                username="developer",
                password_hash=pwd_context.hash("devpassword"),
                permissions=[
                    Permission.COMPILE,
                    Permission.VALIDATE,
                    Permission.DEPLOY,
                    Permission.DOWNLOAD_ARTIFACTS,
                    Permission.READ_WORKSPACE,
                    Permission.MANAGE_PROJECTS
                ]
            ),
            "viewer": User(
                username="viewer",
                password_hash=pwd_context.hash("viewpassword"),
                permissions=[
                    Permission.READ_WORKSPACE,
                    Permission.DOWNLOAD_ARTIFACTS
                ]
            )
        }

    def get_user(self, username: str) -> Optional[User]:
        return self._users.get(username)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
