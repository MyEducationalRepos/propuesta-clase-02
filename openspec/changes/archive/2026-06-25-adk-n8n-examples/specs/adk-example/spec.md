## ADDED Requirements

### Requirement: ADK example lives in examples/adk/
The ADK claims triage agent SHALL be located at `examples/adk/agente_triaje.py` with a Dockerfile at `examples/adk/Dockerfile` and a README at `examples/adk/README.md`.

#### Scenario: File structure after restructuring
- **WHEN** a participant navigates to `examples/adk/`
- **THEN** they SHALL find `agente_triaje.py`, `Dockerfile`, `pyproject.toml`, and `README.md`

### Requirement: Runs exclusively via Docker
The ADK example SHALL run via `docker compose up adk` with no local Python installation required. A `pyproject.toml` inside `examples/adk/` declares `google-adk` as dependency, installed by uv inside the container at build time. Environment variables are injected by Docker Compose via `env_file`; no `python-dotenv` needed.

#### Scenario: Participant runs via Docker
- **WHEN** a participant runs `docker compose up adk` from the project root
- **THEN** the container SHALL build, install deps, and execute all test claims with output streamed to the terminal

### Requirement: ADK README provides step-by-step guide
The `examples/adk/README.md` SHALL contain numbered steps to: (1) configure `.env`, (2) run `docker compose up adk`, (3) interpret the ReAct log output.

#### Scenario: Participant follows README from scratch
- **WHEN** a participant with Docker installed follows all numbered steps in order
- **THEN** they SHALL see the agent process at least one test claim and produce a structured triage output

### Requirement: ReAct log walkthrough section
The ADK README SHALL include a section explaining how to read the ReAct logs: what TOOL_CALL, TOOL_RESULT, and final response mean in the context of agentic AI.

#### Scenario: Participant reads log explanation
- **WHEN** a participant reads the ReAct walkthrough section
- **THEN** they SHALL find annotated descriptions of each log line type with references to the lesson plan concepts (tool use, reasoning, action)

### Requirement: Test claims included in script
The agent script SHALL include at least 4 test claims covering: standard triage, expired policy, high severity with reinsurer notice, and incomplete data.

#### Scenario: All test cases execute
- **WHEN** `docker compose up adk` runs
- **THEN** the container SHALL process all test claims sequentially and print results for each
