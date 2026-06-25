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
The `examples/n8n/Dockerfile` SHALL extend the official `docker.n8n.io/n8nio/n8n` image and copy `workflow_triaje.json` into the container for easy import.

#### Scenario: Workflow available inside container
- **WHEN** the n8n container starts
- **THEN** the workflow JSON SHALL be accessible inside the container for manual import via the n8n UI (Settings -> Import from File)

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
