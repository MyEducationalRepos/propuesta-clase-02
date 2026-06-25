## ADDED Requirements

### Requirement: n8n container pre-loads workflow

The n8n Dockerfile SHALL copy workflow JSON files into the container and `init-workflows.sh` SHALL import and publish all workflows on startup. Both `workflow_triaje.json` (id `triaje-siniestros`) and `workflow_triaje_chat.json` (id `triaje-siniestros-chat`) SHALL be imported and published.

#### Scenario: Both workflows available on startup

- **WHEN** `docker compose up n8n` completes successfully
- **THEN** n8n SHALL contain two published workflows: **"Triaje de Siniestros — Agente IA"** and **"Triaje de Siniestros — Chat IA"**

#### Scenario: Init script imports chat workflow

- **WHEN** the n8n container starts with `workflow_triaje_chat.json` present in `/home/node/workflows/`
- **THEN** `init-workflows.sh` SHALL run `n8n import:workflow` and `n8n publish:workflow --id=triaje-siniestros-chat`
