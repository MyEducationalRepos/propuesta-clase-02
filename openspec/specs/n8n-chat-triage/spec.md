## ADDED Requirements

### Requirement: Chat triage workflow JSON exists

The chat workflow SHALL be located at `examples/n8n/workflow_triaje_chat.json` with a stable workflow id `triaje-siniestros-chat` and display name **"Triaje de Siniestros — Chat IA"**.

#### Scenario: File present in examples directory

- **WHEN** a participant navigates to `examples/n8n/`
- **THEN** they SHALL find `workflow_triaje_chat.json` alongside `workflow_triaje.json`

### Requirement: Chat Trigger as entry point

The chat workflow SHALL use n8n's Chat Trigger node (`@n8n/n8n-nodes-langchain.chatTrigger`) as its sole trigger. The user message SHALL flow to the AI Agent via `$json.chatInput`. The Chat Trigger `responseMode` SHALL be `lastNode` so the chat widget receives the agent triage text when logging nodes run after the agent.

#### Scenario: Participant sends a claim in chat

- **WHEN** a participant types a claim description in the n8n chat panel and sends it
- **THEN** the AI Agent node SHALL receive the message as input and produce a triage response visible in the chat

#### Scenario: Documented example returns structured reply

- **WHEN** a participant pastes the README example claim for POL-2024-003 (robo en farmacia, 300 UF)
- **THEN** the chat panel SHALL display a structured triage answer containing policy status, severity, and liquidador (not `[No response received]`)

### Requirement: Same agent logic as batch workflow

The chat workflow SHALL reuse the same system prompt, Gemini 2.5 Flash model settings, `Buscar_Poliza` tool, `Buscar_Liquidador` tool, severity conditional branch, and local markdown logging nodes as `workflow_triaje.json`.

#### Scenario: Chat triage uses policy lookup

- **WHEN** a participant submits a chat message mentioning a valid policy number (e.g. `POL-2024-003`)
- **THEN** the agent SHALL invoke the policy tool and return a structured triage response including policy status, severity, and assigned liquidator

#### Scenario: High severity triggers reinsurance alert log

- **WHEN** a chat-submitted claim is classified as Alta severity
- **THEN** the workflow SHALL append a row to `data/alertas_reaseguro.md` in addition to `data/log_triaje.md`

### Requirement: Chat workflow README section

The `examples/n8n/README.md` SHALL include a numbered subsection explaining how to: (1) open **"Triaje de Siniestros — Chat IA"**, (2) activate the workflow, (3) open the chat panel, (4) submit a new claim, and (5) read the agent reply. The section SHALL include at least one example claim text participants can paste.

#### Scenario: Participant follows chat instructions

- **WHEN** a participant follows the chat workflow README steps
- **THEN** they SHALL be able to submit a custom claim and see the agent's triage answer in the n8n chat UI without using curl

### Requirement: Workflow active on import

The chat workflow JSON SHALL set `active: true` so the chat endpoint is available after container start without manual activation (participants may still use the n8n toggle).

#### Scenario: Chat available after docker compose up

- **WHEN** a participant runs `docker compose up n8n` with a valid `GOOGLE_API_KEY`
- **THEN** the chat workflow SHALL be imported, published, and active alongside the batch workflow
