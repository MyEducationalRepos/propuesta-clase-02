## Why

The existing ADK script and n8n JSON are raw reference files with no setup guide, no environment configuration, and no visual walkthrough. Insurance professionals (the target audience) need a self-contained, runnable lab they can follow step-by-step in 30 minutes without developer assistance. Without Docker encapsulation, participants would need to install Python, uv, and n8n locally, scattering dependencies across their machines. A Docker-first approach guarantees identical environments and zero local pollution.

## What Changes

- Add `.env.copy` with placeholder guidance for `GOOGLE_API_KEY`.
- Add `docker-compose.yml` orchestrating both examples: ADK container (Python) and n8n container (pre-loaded workflow).
- Add per-example `Dockerfile`s: lean, single-purpose, no bloat.
- Restructure examples into dedicated directories (`examples/adk/`, `examples/n8n/`) with per-example READMEs.
- Add a visual step-by-step guide (`examples/adk/README.md`) showing how to run the ADK agent, read ReAct logs, and interpret tool calls.
- Add an n8n import guide (`examples/n8n/README.md`) with configuration checklist.
- Add a top-level `README.md` linking to both examples and the lesson plan.
- Participant workflow: `cp .env.copy .env`, fill in key, `docker compose up`.

## Capabilities

### New Capabilities
- `env-setup`: `.env.copy` template, `.gitignore`, and environment configuration guide for Google API keys.
- `docker-infra`: Dockerfiles, docker-compose.yml, and container orchestration for both examples.
- `adk-example`: Restructured ADK claims triage agent with Dockerfile, setup instructions, and ReAct log walkthrough.
- `n8n-example`: n8n container with pre-loaded workflow, import guide, configuration checklist, and testing instructions.
- `project-readme`: Top-level README tying lesson plan and both examples together.

### Modified Capabilities

(none -- no existing specs)

## Impact

- New files: `.env.copy`, `.gitignore`, `docker-compose.yml`, `README.md`, `examples/adk/Dockerfile`, `examples/adk/README.md`, `examples/n8n/Dockerfile`, `examples/n8n/README.md`.
- Existing `ejemplo_agente_adk.py` moves to `examples/adk/agente_triaje.py`.
- Existing `ejemplo_workflow_n8n.json` moves to `examples/n8n/workflow_triaje.json`.
- Only host dependency: Docker (and Docker Compose).
