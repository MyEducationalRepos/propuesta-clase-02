## 0. Repository init

- [x] 0.1 Run `git init` and create initial commit
- [x] 0.2 Create `.gitignore` with entries for `.env`, `__pycache__/`, `.venv/`, `*.pyc`, `.uv/`, `.DS_Store`

## 1. Project scaffolding

- [x] 1.1 Create `.env.copy` at project root with `GOOGLE_API_KEY=your-key-here` and inline comment linking to Google AI Studio
- [x] 1.2 Create root `.dockerignore` excluding `.git/`, `.DS_Store`, `openspec/`, `.agent/`, `.cursor/`, `.github/`, `*.md` (except READMEs referenced by COPY)

## 2. Directory restructuring

- [x] 2.1 Create `examples/adk/` and `examples/n8n/` directories
- [x] 2.2 Move `ejemplo_agente_adk.py` to `examples/adk/agente_triaje.py`
- [x] 2.3 Move `ejemplo_workflow_n8n.json` to `examples/n8n/workflow_triaje.json`
- [x] 2.4 Remove original files from project root after confirming copies

## 3. ADK containerization

- [x] 3.1 Create `examples/adk/pyproject.toml` with Python >=3.11, dependency: `google-adk`
- [x] 3.2 Update `examples/adk/agente_triaje.py` to validate `GOOGLE_API_KEY` exists in environment at startup, exit with clear error if missing (env injected by compose, no dotenv needed)
- [x] 3.3 Create `examples/adk/Dockerfile` using `python:3.11-slim`, install uv, copy project files, `uv sync`, set entrypoint to run the script
- [x] 3.4 Create `examples/adk/.dockerignore` excluding `__pycache__/`, `.venv/`, `README.md`
- [x] 3.5 Verify `google-adk` builds on ARM64 (Apple Silicon); if not, add `platform: linux/amd64` to compose service
- [x] 3.6 Verify all 6 test claims execute correctly inside the container

## 4. n8n containerization

- [x] 4.1 Create `examples/n8n/Dockerfile` extending official `docker.n8n.io/n8nio/n8n` image, copy `workflow_triaje.json` to `/home/node/workflows/`
- [x] 4.2 Create `examples/n8n/.dockerignore` excluding `README.md`
- [x] 4.3 Verify n8n starts and workflow is manually importable from inside the container via UI (Settings -> Import from File)

## 5. Docker Compose

- [x] 5.1 Create `docker-compose.yml` at project root with `adk` and `n8n` services, both using `env_file: .env` (path relative to compose file, not build context)
- [x] 5.2 Configure `adk` service: build context `examples/adk/`, no port needed (CLI output only)
- [x] 5.3 Configure `n8n` service: build context `examples/n8n/`, expose port `5678`
- [x] 5.4 Test `docker compose up adk` end-to-end with a valid API key
- [x] 5.5 Test `docker compose up n8n` and verify web UI at `http://localhost:5678`

## 6. Documentation

- [x] 6.1 Write `examples/adk/README.md` with: title, prerequisites (Docker only), numbered steps (configure .env, docker compose up adk), ReAct log walkthrough
- [x] 6.2 Write `examples/n8n/README.md` with: title, prerequisites (Docker only), import steps, node descriptions table, configuration checklist, curl test command
- [x] 6.3 Write `README.md` at project root with: title, description, prerequisites (Docker + API key), quick start (clone, .env, docker compose up), project structure tree

## 7. Verification

- [x] 7.1 Run `docker compose up adk` from a clean state (no local Python) and confirm all test claims produce output
- [x] 7.2 Run `docker compose up n8n` and confirm workflow import and web UI access
- [x] 7.3 Verify `.env` is excluded by `.gitignore`
- [x] 7.4 Review all READMEs for RAE orthography compliance and completeness
