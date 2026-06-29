# Specification Authority

Genesis Engine frontend work must follow this authority order:

1. `genesis_complete_specification.md`
   - Definitive implementation contract.
   - If another source conflicts with this file, this file wins.

2. `genesis_product_architecture.md`
   - Product architecture and rationale.
   - Use this to understand why the system is organized around Organization, Project, and Run.

3. `genesis_engine_design_spec.md`
   - Original audit, enterprise feature list, and priority tiers.
   - Use this for background, prioritization, and feature intent.

4. Existing frontend code
   - Prototype code only.
   - It may reveal current implementation details and integration points, but it must not override the specifications.

## Product Definition

Genesis Engine is a Specification Compiler platform.

It is not:

- a chatbot
- a CRUD dashboard
- a generic admin panel
- a code generator UI

The core mental model is:

```text
You write specifications.
Genesis compiles them into deterministic, inspectable, deployable software artifacts.
```

The frontend must ultimately organize around:

```text
Organization -> Project -> Run
```

A Run is the atomic unit of work.
