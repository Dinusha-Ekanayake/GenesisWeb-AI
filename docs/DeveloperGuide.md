# Developer Guide

## System Requirements
- Python 3.10+
- Node.js 18+

## Quick Start
1. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Creating a Plugin
Genesis Engine is highly modular. To add a new framework target (e.g., Svelte, Django), subclass `GeneratorPlugin` from `genesis_engine/plugins/base.py` and register it in `orchestrator.py`.

## Core Philosophy
- **Determinism:** If you provide the same JSON spec, you must receive the exact same hash and ZIP file. Never use non-seeded random numbers in plugins.
- **Dependency Light:** Genesis Engine attempts to avoid external infrastructure (Redis, Postgres) for core compilation to maintain portability.
