# Genesis Engine Architecture

## Overview
Genesis Engine is a deterministic AI compiler that transforms high-level JSON specifications into production-grade multi-tier applications (Next.js + FastAPI + PostgreSQL).

## Key Components

1. **Planning Engine (`genesis_engine/core/planning_engine.py`)**
   - Ingests `ProjectSpecification`.
   - Generates deterministic acyclic dependency graphs (Feature, Component, API, Database, Dependency, Page).
   - Resolves conflicts using deterministic traversal, logging architectural decisions.

2. **Rule Engine (`genesis_engine/planning/rule_engine.py`)**
   - Validates all generated graphs.
   - Enforces graph integrity, prevents circular dependencies, and ensures no rules are violated.

3. **Generation Engine (`genesis_engine/core/generation_engine.py`)**
   - Applies the validated graphs and generates physical code using Plugins.

4. **Build Orchestrator (`genesis_engine/deployment/build_orchestrator.py`)**
   - Packages the workspace into deterministic ZIP deployments.

5. **Control Plane (`backend/app/api/genesis_controller.py`)**
   - A FastAPI service wrapping the compiler, protected by Role-Based Access Control.

6. **Telemetry Event Bus**
   - Streams build status and compilation events in real-time to the dashboard via Server-Sent Events (SSE).
