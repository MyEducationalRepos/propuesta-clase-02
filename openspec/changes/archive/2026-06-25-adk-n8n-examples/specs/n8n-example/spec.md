## ADDED Requirements

### Requirement: n8n example lives in examples/n8n/
The n8n workflow SHALL be located at `examples/n8n/workflow_triaje.json` with a Dockerfile at `examples/n8n/Dockerfile` and a README at `examples/n8n/README.md`.

#### Scenario: File structure after restructuring
- **WHEN** a participant navigates to `examples/n8n/`
- **THEN** they SHALL find `workflow_triaje.json`, `Dockerfile`, and `README.md`

### Requirement: Runs exclusively via Docker
The n8n example SHALL run via `docker compose up n8n` using the official n8n image. No local n8n installation required.

#### Scenario: Participant starts n8n
- **WHEN** a participant runs `docker compose up n8n` from the project root
- **THEN** n8n SHALL be accessible at `http://localhost:5678` with the workflow JSON available for import

### Requirement: n8n README provides import instructions
The `examples/n8n/README.md` SHALL contain numbered steps to: (1) run `docker compose up n8n`, (2) open the web UI, (3) import the JSON workflow, (4) configure the Gemini API credential, (5) test the webhook endpoint.

#### Scenario: Participant imports workflow successfully
- **WHEN** a participant follows all numbered steps
- **THEN** they SHALL see the workflow loaded with all nodes visible in the n8n canvas

### Requirement: Node descriptions in README
The README SHALL include a table describing each node in the workflow: its name, type, and purpose in the triage flow.

#### Scenario: Participant understands workflow nodes
- **WHEN** a participant reads the node descriptions
- **THEN** they SHALL find every node from the JSON described with its role (trigger, agent, model, tools, conditional, notification, logging, response)

### Requirement: Configuration checklist
The README SHALL include a checklist of all credentials and IDs that need configuration before the workflow can run (Gemini API key, Gmail OAuth, Google Sheets ID).

#### Scenario: Participant reviews checklist
- **WHEN** a participant reads the configuration checklist
- **THEN** they SHALL find each configurable item with where to set it in the n8n UI and what value format is expected

### Requirement: Testing instructions with curl
The README SHALL include a curl command example to test the webhook endpoint.

#### Scenario: Participant tests webhook
- **WHEN** a participant runs the provided curl command against `http://localhost:5678`
- **THEN** the webhook SHALL receive the test claim and return the agent's triage response
