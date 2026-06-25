## Context

Class 2 of the Insurex AI program teaches agentic AI to insurance managers. Two working examples exist (ADK Python script, n8n workflow JSON) but lack setup documentation, environment configuration, and classroom-friendly structure. Participants have 30 minutes for the hands-on lab, zero developer background, and should not install anything beyond Docker on their machines.

## Goals / Non-Goals

**Goals:**
- Everything runs inside Docker containers -- zero host pollution
- Single `docker compose up` to start both examples
- `.env` is the only configuration participants touch
- READMEs written for managers: step-by-step, visual cues, no assumed CLI knowledge
- Lean Dockerfiles: minimal base images, no bloat

**Non-Goals:**
- Production-grade deployment (orchestration, TLS, cloud hosting)
- Building a web UI around the ADK agent
- Modifying the n8n workflow logic or adding new nodes
- Supporting models other than Google Gemini
- Writing automated tests for the teaching examples
- Persistent n8n data across container restarts (ephemeral is fine for a 30-min lab)

## Decisions

### 1. Docker Compose as the single entry point

One `docker-compose.yml` at the project root defines two services: `adk` (runs the Python script) and `n8n` (runs n8n with the pre-loaded workflow). Participants run `docker compose up adk` or `docker compose up n8n` depending on their track. Alternative: separate docker run commands. Rejected because compose centralizes env var injection and is simpler to document.

### 2. Directory layout: `examples/adk/` and `examples/n8n/`

Each example gets its own directory with Dockerfile, source files, and README. The compose file references these as build contexts. Alternative: monolithic Dockerfile. Rejected because it mixes unrelated concerns.

### 3. ADK container: python:3.11-slim + uv

Uses `python:3.11-slim` as base, installs uv inside the container, copies `pyproject.toml` and the script, runs `uv sync` at build time. The container runs the script directly. Participants never install Python or uv on their host.

### 4. n8n container: official n8n image

Uses the official `docker.n8n.io/n8nio/n8n` image. The workflow JSON is volume-mounted or copied in. Gemini API key is injected via environment variable from `.env`. Participants open the n8n web UI at `http://localhost:5678` to inspect and run the workflow.

### 5. `.env` shared across services

A single `.env` file at the project root is referenced by `docker-compose.yml` via `env_file`. Both services get `GOOGLE_API_KEY`. This avoids duplicating secrets.

### 6. Keep filenames in Spanish

The script and workflow keep Spanish names (`agente_triaje.py`, `workflow_triaje.json`) to match the lesson plan and slides. READMEs are in Spanish with RAE orthography.

## Risks / Trade-offs

- [Docker not installed on participant machines] -> README includes Docker Desktop install link. Instructor verifies during pre-class setup email.
- [Gemini API rate limits during class] -> Provide a fallback note suggesting participants pair up or use the instructor's live demo if rate-limited.
- [n8n image size (~400MB)] -> Acceptable for a lab. Instructor can pre-pull images on lab machines.
- [n8n credential configuration still manual in UI] -> README provides exact click path. The workflow JSON ships with placeholder credential IDs.
- [Docker Compose V2 vs V1 syntax] -> Use `docker compose` (V2, space) throughout. Note in README.
