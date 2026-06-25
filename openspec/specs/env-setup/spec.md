## ADDED Requirements

### Requirement: .env.copy template exists at project root
The project SHALL include a `.env.copy` file at the repository root containing all required environment variables with placeholder values and inline comments explaining how to obtain each key.

#### Scenario: Participant copies env file
- **WHEN** a participant runs `cp .env.copy .env`
- **THEN** the resulting `.env` file contains `GOOGLE_API_KEY` with a placeholder value and a comment explaining where to get the key (Google AI Studio)

#### Scenario: No secrets in template
- **WHEN** `.env.copy` is committed to git
- **THEN** it SHALL contain only placeholder strings (no real API keys or credentials)

### Requirement: .gitignore excludes .env and Docker artifacts
The repository SHALL have a `.gitignore` that prevents `.env`, `__pycache__/`, `.venv/`, and `*.pyc` from being committed.

#### Scenario: .env is ignored by git
- **WHEN** a participant creates `.env` from `.env.copy` and runs `git status`
- **THEN** `.env` SHALL NOT appear as an untracked file

### Requirement: Docker Compose injects .env into containers
The `docker-compose.yml` SHALL use `env_file: .env` so that `GOOGLE_API_KEY` is available inside both containers without participants editing Dockerfiles.

#### Scenario: Key available in ADK container
- **WHEN** the ADK container starts with a valid `.env`
- **THEN** the Python script SHALL read `GOOGLE_API_KEY` from its environment and execute normally

#### Scenario: Missing .env produces clear error
- **WHEN** a participant runs `docker compose up` without creating `.env`
- **THEN** Docker Compose SHALL show a warning about the missing env file
