import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from genesis_engine.models.planning import (
    ProposedApplicationPlan,
    TechnologyStack,
    FrontendStack,
    BackendStack,
    DatabaseStack,
    AiStack,
    AuthStack,
    DeploymentStack,
    TestingStack,
    LLMApplicationProposal,
)


# Deterministic fallback blueprints keyed by app_type
_FALLBACK_BLUEPRINTS: dict = {
    "crm": {
        "name": "CRM Application",
        "target_users": "Sales teams and account managers",
        "pages": ["Dashboard", "Customers", "Deals", "Activities", "Reports", "Team", "Settings"],
        "components": ["Navbar", "Sidebar", "CustomerCard", "DealCard", "ActivityFeed", "StatsCard", "DataTable", "FilterBar"],
        "entities": ["Customer", "Deal", "Activity", "User", "Team", "Note"],
        "api_routes": [
            "GET /customers", "POST /customers", "GET /customers/{id}", "PUT /customers/{id}",
            "GET /deals", "POST /deals", "PUT /deals/{id}",
            "GET /activities", "POST /activities",
            "GET /reports/summary",
        ],
        "auth_requirements": ["JWT authentication required for all routes", "Role-based access control"],
        "roles_permissions": ["admin: full access", "manager: read/write customers and deals", "salesperson: read/write own records only"],
        "navigation_structure": ["Dashboard", "Customers", "Deals", "Activities", "Reports", "Settings"],
        "architecture_summary": "A multi-tenant CRM with a FastAPI REST backend, PostgreSQL database, and Next.js frontend. Authentication via JWT. Role-based access controls sales data visibility.",
        "assumptions": ["Single-tenant deployment", "Email/password authentication", "No real-time updates required initially"],
        "warnings": ["Plan carefully for data isolation if adding multi-tenant support later", "Consider pagination early for large customer datasets"],
    },
    "portfolio": {
        "name": "Portfolio Website",
        "target_users": "Prospective clients, employers, and collaborators",
        "pages": ["Home", "About", "Projects", "Blog", "Contact"],
        "components": ["Navbar", "Footer", "ProjectCard", "BlogCard", "ContactForm", "HeroSection", "SkillBadge"],
        "entities": ["Project", "BlogPost", "ContactMessage"],
        "api_routes": [
            "GET /projects", "GET /projects/{id}",
            "GET /blog", "GET /blog/{slug}",
            "POST /contact",
        ],
        "auth_requirements": ["Optional: admin authentication for content management panel"],
        "roles_permissions": ["public: read-only access to all pages"],
        "navigation_structure": ["Home", "About", "Projects", "Blog", "Contact"],
        "architecture_summary": "A content-first portfolio site with a Next.js frontend and optional FastAPI backend for the contact form and content API. Deployable as static site or hybrid.",
        "assumptions": ["Content is mostly static or managed via API", "No user accounts for visitors"],
        "warnings": ["Consider static site generation for improved SEO", "Contact form requires server-side handling or a third-party service"],
    },
    "booking_platform": {
        "name": "Booking Platform",
        "target_users": "Customers making reservations and administrators managing inventory",
        "pages": ["Home", "Listings", "ListingDetail", "Booking", "BookingConfirmation", "UserDashboard", "AdminPanel"],
        "components": ["Navbar", "Footer", "ListingCard", "BookingCalendar", "PriceBreakdown", "ReviewCard", "SearchFilter"],
        "entities": ["Listing", "Booking", "User", "Review", "Payment", "Availability"],
        "api_routes": [
            "GET /listings", "GET /listings/{id}", "GET /listings/{id}/availability",
            "POST /bookings", "GET /bookings/{id}", "GET /bookings/user/{userId}",
            "POST /payments/intent", "POST /reviews",
        ],
        "auth_requirements": ["JWT authentication required for bookings and user dashboard", "Public access for listing search"],
        "roles_permissions": ["admin: manage all listings and bookings", "host: manage own listings", "guest: browse and book"],
        "navigation_structure": ["Home", "Listings", "My Bookings", "Admin"],
        "architecture_summary": "A two-sided booking marketplace with real-time availability, payment processing integration, and review system. FastAPI backend with PostgreSQL for transactional data.",
        "assumptions": ["Payments via Stripe or similar third-party service", "Single currency support initially", "Email notifications for booking confirmation"],
        "warnings": ["Availability and double-booking prevention requires careful transaction handling", "Payment integration significantly increases compliance scope (PCI DSS)"],
    },
    "task_management": {
        "name": "Task Management Dashboard",
        "target_users": "Teams and project managers tracking tasks and progress",
        "pages": ["Dashboard", "Projects", "TaskBoard", "TaskDetail", "TeamMembers", "Calendar", "Settings"],
        "components": ["Navbar", "Sidebar", "TaskCard", "StatusBadge", "KanbanColumn", "MemberAvatar", "PriorityBadge", "ProgressBar"],
        "entities": ["Project", "Task", "User", "Comment", "Label", "Milestone"],
        "api_routes": [
            "GET /projects", "POST /projects", "GET /projects/{id}",
            "GET /tasks", "POST /tasks", "PUT /tasks/{id}", "DELETE /tasks/{id}",
            "GET /users", "PUT /tasks/{id}/assign",
        ],
        "auth_requirements": ["JWT authentication required", "Project-level access control"],
        "roles_permissions": ["admin: full access", "member: read/write tasks in assigned projects", "viewer: read-only access"],
        "navigation_structure": ["Dashboard", "Projects", "My Tasks", "Team", "Settings"],
        "architecture_summary": "A Kanban-style task management app with FastAPI backend, PostgreSQL, and Next.js frontend. Real-time updates via WebSocket or polling for task status changes.",
        "assumptions": ["Team size is small to medium (< 100 members)", "No Gantt chart or resource planning in v1"],
        "warnings": ["Real-time collaboration features require careful state synchronization", "Consider optimistic UI updates for drag-and-drop"],
    },
    "blog_cms": {
        "name": "Blog / CMS",
        "target_users": "Readers and content editors",
        "pages": ["Home", "Blog", "PostDetail", "CategoryList", "About", "Contact", "AdminDashboard", "PostEditor"],
        "components": ["Navbar", "Footer", "PostCard", "TagBadge", "AuthorCard", "TableOfContents", "CommentSection", "SearchBar"],
        "entities": ["Post", "Author", "Category", "Tag", "Comment", "Media"],
        "api_routes": [
            "GET /posts", "GET /posts/{slug}", "POST /posts", "PUT /posts/{id}",
            "GET /categories", "GET /tags",
            "POST /comments", "GET /posts/{id}/comments",
        ],
        "auth_requirements": ["Public read access", "JWT authentication for admin and editors"],
        "roles_permissions": ["admin: full content management", "editor: create and edit posts", "reader: public read-only"],
        "navigation_structure": ["Home", "Blog", "Categories", "About", "Contact"],
        "architecture_summary": "A headless CMS with a FastAPI backend serving a Next.js frontend. Static generation for published posts with ISR. Admin dashboard for content management.",
        "assumptions": ["Server-side rendering or static generation for SEO", "Image hosting via CDN or object storage"],
        "warnings": ["SEO setup (metadata, sitemaps, canonical URLs) is critical for a blog", "Comment moderation should be planned to prevent spam"],
    },
    "ecommerce": {
        "name": "E-Commerce Store",
        "target_users": "Online shoppers and store administrators",
        "pages": ["Home", "ProductList", "ProductDetail", "Cart", "Checkout", "OrderConfirmation", "UserAccount", "OrderHistory", "AdminProducts"],
        "components": ["Navbar", "Footer", "ProductCard", "CartItem", "PriceTag", "QuantitySelector", "ReviewStars", "CategoryFilter", "SearchBar"],
        "entities": ["Product", "Category", "Order", "OrderItem", "User", "Cart", "Review", "Coupon"],
        "api_routes": [
            "GET /products", "GET /products/{id}", "GET /categories",
            "GET /cart", "POST /cart/items", "DELETE /cart/items/{id}",
            "POST /orders", "GET /orders/{id}", "GET /orders/user/{userId}",
            "POST /payments/intent",
        ],
        "auth_requirements": ["Guest checkout option", "JWT authentication for order history and account", "Admin authentication for product management"],
        "roles_permissions": ["admin: product and order management", "customer: browse, cart, and checkout", "guest: browse and checkout without account"],
        "navigation_structure": ["Home", "Products", "Cart", "Account", "Orders"],
        "architecture_summary": "A full e-commerce platform with product catalog, shopping cart, payment integration, and order management. FastAPI backend with PostgreSQL, Next.js storefront.",
        "assumptions": ["Payment via Stripe", "Inventory management is basic (in-stock / out-of-stock)", "Single currency and shipping zone in v1"],
        "warnings": ["PCI DSS compliance required for payment handling", "Inventory race conditions must be handled at the database level", "Search performance becomes critical at scale"],
    },
    "lms": {
        "name": "Learning Management System",
        "target_users": "Students and instructors",
        "pages": ["Home", "CourseCatalog", "CourseDetail", "LessonPlayer", "StudentDashboard", "InstructorDashboard", "Quizzes", "Progress"],
        "components": ["Navbar", "Sidebar", "CourseCard", "LessonList", "VideoPlayer", "QuizWidget", "ProgressBar", "CertificateCard"],
        "entities": ["Course", "Lesson", "Enrollment", "User", "Quiz", "Question", "Submission", "Certificate"],
        "api_routes": [
            "GET /courses", "GET /courses/{id}", "GET /courses/{id}/lessons",
            "POST /enrollments", "GET /enrollments/user/{userId}",
            "GET /lessons/{id}", "POST /lessons/{id}/complete",
            "GET /quizzes/{id}", "POST /quizzes/{id}/submit",
        ],
        "auth_requirements": ["JWT authentication required for enrollment and progress", "Public access for course catalog"],
        "roles_permissions": ["admin: full platform management", "instructor: create and manage courses", "student: enroll and access content"],
        "navigation_structure": ["Courses", "My Learning", "Instructor Studio", "Profile"],
        "architecture_summary": "An LMS with course catalog, video lesson delivery, quiz engine, and progress tracking. FastAPI backend with PostgreSQL. Video storage via external CDN.",
        "assumptions": ["Video content hosted externally (YouTube, Vimeo, or S3)", "Certificate generation is PDF-based"],
        "warnings": ["Video delivery bandwidth costs can be significant", "SCORM compliance may be required for enterprise clients"],
    },
    "saas_dashboard": {
        "name": "SaaS Dashboard",
        "target_users": "Business users monitoring metrics and managing subscriptions",
        "pages": ["Dashboard", "Analytics", "Users", "Billing", "Integrations", "Settings", "Profile"],
        "components": ["Navbar", "Sidebar", "MetricCard", "LineChart", "BarChart", "DataTable", "StatusBadge", "NotificationBell", "AvatarMenu"],
        "entities": ["Organization", "User", "Subscription", "Invoice", "Integration", "Event"],
        "api_routes": [
            "GET /analytics/summary", "GET /analytics/events",
            "GET /users", "POST /users/invite", "PUT /users/{id}/role",
            "GET /billing/subscription", "GET /billing/invoices",
            "GET /integrations", "POST /integrations/{name}/connect",
        ],
        "auth_requirements": ["JWT authentication required", "Organization-scoped data isolation", "RBAC for admin vs member"],
        "roles_permissions": ["owner: full access including billing", "admin: manage users and integrations", "member: read-only analytics and settings"],
        "navigation_structure": ["Dashboard", "Analytics", "Users", "Billing", "Integrations", "Settings"],
        "architecture_summary": "A multi-tenant SaaS dashboard with organization-scoped data, analytics, subscription management, and integration hooks. FastAPI with PostgreSQL and background task support.",
        "assumptions": ["Billing via Stripe", "Email via SendGrid or similar", "Metrics computed from stored events"],
        "warnings": ["Multi-tenancy requires strict data isolation at the query level", "Billing webhook handling requires idempotency"],
    },
    "web_application": {
        "name": "Web Application",
        "target_users": "General users",
        "pages": ["Home", "Dashboard", "Profile", "Settings"],
        "components": ["Navbar", "Footer", "Card", "Button", "Form", "DataTable"],
        "entities": ["User", "Record"],
        "api_routes": ["GET /records", "POST /records", "GET /records/{id}", "PUT /records/{id}"],
        "auth_requirements": ["JWT authentication required"],
        "roles_permissions": ["admin: full access", "user: access own records"],
        "navigation_structure": ["Home", "Dashboard", "Profile", "Settings"],
        "architecture_summary": "A general-purpose web application with a FastAPI backend and Next.js frontend. Authentication via JWT.",
        "assumptions": ["Standard CRUD operations", "Single tenant"],
        "warnings": ["Refine this plan by providing a more specific prompt describing the application's purpose and features"],
    },
}


def _detect_app_type(prompt: str) -> str:
    kw = prompt.lower()
    if any(w in kw for w in ["crm", "customer relationship", "sales team", "deals pipeline", "leads", "pipeline"]):
        return "crm"
    if any(w in kw for w in ["portfolio", "personal website", "showcase", "resume site", "my work"]):
        return "portfolio"
    if any(w in kw for w in ["booking", "reservation", "hotel", "appointment", "schedule", "rooms", "availability"]):
        return "booking_platform"
    if any(w in kw for w in ["task", "todo", "kanban", "project management", "sprint", "backlog"]):
        return "task_management"
    if any(w in kw for w in ["blog", "cms", "content management", "articles", "posts", "publishing"]):
        return "blog_cms"
    if any(w in kw for w in ["shop", "store", "ecommerce", "e-commerce", "products", "cart", "checkout", "orders"]):
        return "ecommerce"
    if any(w in kw for w in ["lms", "learning", "courses", "lessons", "students", "quizzes", "e-learning"]):
        return "lms"
    if any(w in kw for w in ["saas", "dashboard", "analytics", "metrics", "subscription", "multi-tenant", "billing"]):
        return "saas_dashboard"
    return "web_application"


def _build_tech_stack(preferences: dict, llm_hints: dict = None) -> TechnologyStack:
    """Construct TechnologyStack from preferences dict and optional LLM hints.
    Preferences override LLM hints; both override defaults.
    """
    hints = llm_hints or {}
    pref_frontend = preferences.get("frontend", hints.get("frontend_framework", "nextjs"))
    pref_backend = preferences.get("backend", hints.get("backend_framework", "fastapi"))
    pref_database = preferences.get("database", hints.get("database_engine", "postgresql"))
    ai_enabled = hints.get("ai_enabled", False)

    return TechnologyStack(
        frontend=FrontendStack(
            framework=pref_frontend,
            language="typescript",
            router="app_router" if pref_frontend == "nextjs" else "react_router",
            styling=preferences.get("styling", "tailwind"),
            component_library=preferences.get("component_library", "shadcn_ui"),
        ),
        backend=BackendStack(
            framework=pref_backend,
            language="python" if pref_backend in ("fastapi", "django", "flask") else "typescript",
            api_style=preferences.get("api_style", "rest"),
            orm=preferences.get("orm", "sqlalchemy" if pref_backend in ("fastapi", "django") else None),
        ),
        database=DatabaseStack(
            engine=pref_database,
            hosting=preferences.get("db_hosting", "docker_local_or_managed"),
        ),
        ai=AiStack(
            enabled=ai_enabled,
            framework="langchain" if ai_enabled else None,
            model_provider=hints.get("ai_model_provider", None),
        ),
        auth=AuthStack(
            provider=hints.get("auth_provider", preferences.get("auth", "custom_jwt")),
            strategy=preferences.get("auth_strategy", "email_password"),
        ),
        deployment=DeploymentStack(
            containerization="docker",
            frontend_host="vercel" if pref_frontend == "nextjs" else "netlify",
            backend_host=preferences.get("backend_host", "render_or_aws"),
            database_host=f"managed_{pref_database}" if pref_database in ("postgresql", "mysql") else pref_database,
        ),
        testing=TestingStack(
            frontend="vitest",
            backend="pytest" if pref_backend in ("fastapi", "django", "flask") else "jest",
            e2e="playwright",
        ),
    )


class PlanningService:
    """
    Planning-only service that produces a ProposedApplicationPlan from a natural
    language prompt. No workspace files are written; no code is generated.
    The plan requires explicit user approval before generation begins.
    """

    def propose(self, prompt: str, preferences: dict, project_id: str) -> ProposedApplicationPlan:
        """Convert a natural language prompt into a proposed application plan.
        Tries LLM first; falls back to deterministic keyword analysis on any failure.
        Does NOT write to disk, does NOT call the compiler or generator.
        """
        llm_output = None
        generation_method = "llm"

        try:
            llm_output = self._call_llm(prompt)
        except Exception:
            generation_method = "deterministic_fallback"

        if llm_output is not None:
            return self._build_plan_from_llm(llm_output, preferences, project_id)
        else:
            return self._build_plan_from_fallback(prompt, preferences, project_id)

    def _call_llm(self, prompt: str) -> LLMApplicationProposal:
        """Call the LLM with structured output. Raises on any failure."""
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise RuntimeError("langchain_openai is not installed")

        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        base_url = os.environ.get("OPENAI_BASE_URL", None)
        model_name = os.environ.get("GENESIS_PLANNING_MODEL", "gpt-4-turbo")

        kwargs = {"model": model_name, "temperature": 0}
        if base_url:
            kwargs["base_url"] = base_url

        llm = ChatOpenAI(**kwargs)
        structured_llm = llm.with_structured_output(LLMApplicationProposal)

        from langchain_core.prompts import ChatPromptTemplate
        system_prompt = (
            "You are an expert software architect and product designer. "
            "Given a natural language description of an application, produce a detailed, structured proposal. "
            "Derive ALL fields from the user's prompt — do not invent features not implied by the prompt. "
            "Separate pages (route-level views) from components (reusable UI modules). "
            "Keep page names clean PascalCase words (e.g. 'CustomerList', not 'Customer List Page'). "
            "Derive entities from the problem domain, not from the tech stack. "
            "API routes should follow REST conventions with appropriate HTTP methods."
        )
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{prompt}"),
        ])
        result: LLMApplicationProposal = (chat_prompt | structured_llm).invoke({"prompt": prompt})
        return result

    def _build_plan_from_llm(
        self,
        llm_output: LLMApplicationProposal,
        preferences: dict,
        project_id: str,
    ) -> ProposedApplicationPlan:
        llm_hints = {
            "frontend_framework": llm_output.frontend_framework,
            "backend_framework": llm_output.backend_framework,
            "database_engine": llm_output.database_engine,
            "auth_provider": llm_output.auth_provider,
            "ai_enabled": llm_output.ai_enabled,
        }
        tech_stack = _build_tech_stack(preferences, llm_hints)

        return ProposedApplicationPlan(
            project_id=project_id,
            name=llm_output.name,
            description=llm_output.description,
            app_type=llm_output.app_type,
            target_users=llm_output.target_users,
            pages=llm_output.pages,
            components=llm_output.components,
            entities=llm_output.entities,
            api_routes=llm_output.api_routes,
            auth_requirements=llm_output.auth_requirements,
            roles_permissions=llm_output.roles_permissions,
            navigation_structure=llm_output.navigation_structure,
            technology_stack=tech_stack,
            tools_libraries=llm_output.tools_libraries,
            deployment_target=llm_output.deployment_target,
            architecture_summary=llm_output.architecture_summary,
            assumptions=llm_output.assumptions,
            warnings=llm_output.warnings,
            validation_status="PENDING",
            approval_status="PENDING",
            generation_method="llm",
        )

    def _build_plan_from_fallback(
        self,
        prompt: str,
        preferences: dict,
        project_id: str,
    ) -> ProposedApplicationPlan:
        app_type = _detect_app_type(prompt)
        blueprint = _FALLBACK_BLUEPRINTS.get(app_type, _FALLBACK_BLUEPRINTS["web_application"])
        tech_stack = _build_tech_stack(preferences)

        # Derive a name from the prompt (first ~60 chars, trimmed at word boundary)
        words = prompt.strip().split()
        name_words = []
        length = 0
        for w in words:
            if length + len(w) > 50:
                break
            name_words.append(w)
            length += len(w) + 1
        derived_name = " ".join(name_words).strip(".,:;!?") or blueprint["name"]

        warnings = list(blueprint["warnings"]) + [
            "FALLBACK: This plan was generated deterministically because the LLM was unavailable. "
            "It is based on keyword matching and a template for the detected app type. "
            "Review all sections carefully before approving."
        ]

        return ProposedApplicationPlan(
            project_id=project_id,
            name=derived_name,
            description=prompt[:300],
            app_type=app_type,
            target_users=blueprint["target_users"],
            pages=blueprint["pages"],
            components=blueprint["components"],
            entities=blueprint["entities"],
            api_routes=blueprint["api_routes"],
            auth_requirements=blueprint["auth_requirements"],
            roles_permissions=blueprint["roles_permissions"],
            navigation_structure=blueprint["navigation_structure"],
            technology_stack=tech_stack,
            tools_libraries=[],
            deployment_target="docker",
            architecture_summary=blueprint["architecture_summary"],
            assumptions=blueprint["assumptions"],
            warnings=warnings,
            validation_status="PENDING",
            approval_status="PENDING",
            generation_method="deterministic_fallback",
        )
