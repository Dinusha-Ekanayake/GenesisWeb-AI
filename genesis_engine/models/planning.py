from pydantic import BaseModel, Field
from typing import List, Optional


class EntityFieldDef(BaseModel):
    name: str
    type: str = "string"
    required: bool = True


class EntityDefinition(BaseModel):
    name: str
    fields: List[EntityFieldDef] = Field(default_factory=list)


# --- Technology stack sub-models ---

class FrontendStack(BaseModel):
    framework: str = "nextjs"
    language: str = "typescript"
    router: str = "app_router"
    styling: str = "tailwind"
    component_library: Optional[str] = "shadcn_ui"


class BackendStack(BaseModel):
    framework: str = "fastapi"
    language: str = "python"
    api_style: str = "rest"
    orm: Optional[str] = "sqlalchemy"


class DatabaseStack(BaseModel):
    engine: str = "postgresql"
    hosting: str = "docker_local_or_managed"


class AiStack(BaseModel):
    enabled: bool = False
    framework: Optional[str] = None
    orchestration: Optional[str] = None
    model_provider: Optional[str] = None
    vector_store: Optional[str] = None


class AuthStack(BaseModel):
    provider: str = "custom_jwt"
    strategy: str = "email_password"


class DeploymentStack(BaseModel):
    containerization: str = "docker"
    frontend_host: str = "vercel"
    backend_host: str = "render_or_aws"
    database_host: str = "managed_postgresql"


class TestingStack(BaseModel):
    frontend: str = "vitest"
    backend: str = "pytest"
    e2e: str = "playwright"


class TechnologyStack(BaseModel):
    frontend: FrontendStack = Field(default_factory=FrontendStack)
    backend: BackendStack = Field(default_factory=BackendStack)
    database: DatabaseStack = Field(default_factory=DatabaseStack)
    ai: AiStack = Field(default_factory=AiStack)
    auth: AuthStack = Field(default_factory=AuthStack)
    deployment: DeploymentStack = Field(default_factory=DeploymentStack)
    testing: TestingStack = Field(default_factory=TestingStack)


# --- LLM structured output target (flat — no nested models) ---

class LLMApplicationProposal(BaseModel):
    """Flat schema for LLM structured output. No nested sub-models to avoid JSON schema issues."""
    name: str = Field(description="Application name derived from the prompt")
    description: str = Field(description="Brief description of what the application does")
    app_type: str = Field(description="One of: portfolio, crm, booking_platform, task_management, blog_cms, ecommerce, lms, saas_dashboard, web_application")
    target_users: str = Field(description="Who will use this application")
    pages: List[str] = Field(description="Page names for the application (page-level routes only, not components)")
    components: List[str] = Field(description="Reusable UI component names (Navbar, Card, etc. — not pages)")
    entities: List[str] = Field(description="Core data entity/model names (e.g. Customer, Order, User)")
    api_routes: List[str] = Field(description="Proposed API routes (e.g. 'GET /customers', 'POST /deals')")
    auth_requirements: List[str] = Field(description="Authentication and authorization requirements")
    roles_permissions: List[str] = Field(description="User roles and their permissions (e.g. 'admin: full access')")
    navigation_structure: List[str] = Field(description="Primary navigation items in display order")
    tools_libraries: List[str] = Field(description="Key tools and libraries beyond the core stack")
    deployment_target: str = Field(default="docker", description="Deployment target: docker, vercel, aws, gcp, azure")
    architecture_summary: str = Field(description="One paragraph summary of the proposed architecture")
    assumptions: List[str] = Field(description="Assumptions made about unstated requirements")
    warnings: List[str] = Field(description="Potential issues or risks the user should be aware of")
    # Tech stack hints (flat strings; TechnologyStack is constructed from these)
    frontend_framework: str = Field(default="nextjs", description="Frontend framework recommendation")
    frontend_styling: str = Field(default="tailwind", description="CSS/styling recommendation")
    backend_framework: str = Field(default="fastapi", description="Backend framework recommendation")
    database_engine: str = Field(default="postgresql", description="Database engine recommendation")
    auth_provider: str = Field(default="custom_jwt", description="Auth provider: custom_jwt, auth0, clerk, firebase_auth")
    ai_enabled: bool = Field(default=False, description="Whether AI/ML features are needed")


# --- Full planning output model ---

class ProposedApplicationPlan(BaseModel):
    project_id: str
    name: str
    description: str
    app_type: str
    target_users: str
    pages: List[str] = Field(default_factory=list)
    components: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    api_routes: List[str] = Field(default_factory=list)
    auth_requirements: List[str] = Field(default_factory=list)
    roles_permissions: List[str] = Field(default_factory=list)
    navigation_structure: List[str] = Field(default_factory=list)
    technology_stack: TechnologyStack = Field(default_factory=TechnologyStack)
    tools_libraries: List[str] = Field(default_factory=list)
    deployment_target: str = "docker"
    architecture_summary: str = ""
    assumptions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    entity_definitions: List[EntityDefinition] = Field(default_factory=list)
    validation_status: str = "PENDING"
    approval_status: str = "PENDING"
    generation_method: str = "llm"  # "llm" or "deterministic_fallback"
