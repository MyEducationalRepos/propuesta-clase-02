## ADDED Requirements

### Requirement: docker-compose.yml at project root
The project root SHALL contain a `docker-compose.yml` defining two services: `adk` and `n8n`, both consuming `.env` via `env_file`.

#### Scenario: Participant runs ADK example
- **WHEN** a participant runs `docker compose up adk`
- **THEN** Docker SHALL build the ADK image, inject `GOOGLE_API_KEY` from `.env`, and execute the triage script with output visible in the terminal

#### Scenario: Participant runs n8n example
- **WHEN** a participant runs `docker compose up n8n`
- **THEN** Docker SHALL start the n8n container and expose the web UI at `http://localhost:5678`

#### Scenario: Both services share .env
- **WHEN** `docker-compose.yml` references `env_file: .env`
- **THEN** both `adk` and `n8n` services SHALL receive `GOOGLE_API_KEY` without duplicating configuration

### Requirement: ADK Dockerfile is lean
The `examples/adk/Dockerfile` SHALL use `python:3.11-slim` as base, install uv, copy only necessary files (`pyproject.toml`, `agente_triaje.py`), and run `uv sync` at build time.

#### Scenario: Image size is reasonable
- **WHEN** the ADK image is built
- **THEN** the final image SHALL be under 500MB (slim base + minimal deps)

#### Scenario: No host Python required
- **WHEN** a participant has only Docker installed (no local Python)
- **THEN** `docker compose up adk` SHALL still execute successfully

### Requirement: n8n Dockerfile uses official image
The `examples/n8n/Dockerfile` SHALL extend the official `docker.n8n.io/n8nio/n8n` image and copy `workflow_triaje.json` and `workflow_triaje_chat.json` into the container for automatic import.

#### Scenario: Workflows available inside container
- **WHEN** the n8n container starts
- **THEN** both workflow JSON files SHALL be accessible inside the container at `/home/node/workflows/`

### Requirement: n8n container pre-loads workflows
The n8n Dockerfile SHALL copy workflow JSON files into the container and `init-workflows.sh` SHALL import and publish all workflows on startup. Both `workflow_triaje.json` (id `triaje-siniestros`) and `workflow_triaje_chat.json` (id `triaje-siniestros-chat`) SHALL be imported and published.

#### Scenario: Both workflows available on startup
- **WHEN** `docker compose up n8n` completes successfully
- **THEN** n8n SHALL contain two published workflows: **"Triaje de Siniestros — Agente IA"** and **"Triaje de Siniestros — Chat IA"**

#### Scenario: Init script imports chat workflow
- **WHEN** the n8n container starts with `workflow_triaje_chat.json` present in `/home/node/workflows/`
- **THEN** `init-workflows.sh` SHALL run `n8n import:workflow` and `n8n publish:workflow --id=triaje-siniestros-chat`

### Requirement: .dockerignore files prevent context bloat
Each example directory SHALL contain a `.dockerignore` excluding irrelevant files (READMEs, caches, venvs) from build context.

#### Scenario: Build context is minimal
- **WHEN** `docker compose build` runs
- **THEN** build context SHALL NOT include `.DS_Store`, `__pycache__/`, `.venv/`, or documentation files

### Requirement: ARM64 compatibility verified
The ADK container SHALL build and run on both x86_64 and ARM64 (Apple Silicon). If `google-adk` lacks ARM wheels, the compose service SHALL pin `platform: linux/amd64`.

#### Scenario: Build on Apple Silicon Mac
- **WHEN** a participant runs `docker compose build adk` on an M1/M2/M3 Mac
- **THEN** the image SHALL build successfully without wheel compilation errors
