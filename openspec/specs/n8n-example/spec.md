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
The README SHALL include a table describing each node in both workflows: its name, type, and purpose in the triage flow. The batch workflow table SHALL include the Manual Trigger and test cases Code node in addition to the existing nodes. The chat workflow table SHALL include the Chat Trigger node in addition to the agent, model, tools, conditional, and logging nodes.

#### Scenario: Participant understands batch workflow nodes
- **WHEN** a participant reads the node descriptions for the batch workflow
- **THEN** they SHALL find every node from the JSON described with its role (manual trigger, test cases generator, webhook trigger, agent, model, tools, conditional, local alert writer, local log writer)

#### Scenario: Participant understands chat workflow nodes
- **WHEN** a participant reads the node descriptions for the chat workflow
- **THEN** they SHALL find the Chat Trigger, AI Agent, Gemini model, policy tool, liquidator tool, severity conditional, alert writer, and log writer described with their roles

### Requirement: Dual n8n workflow files exist
The n8n workflows SHALL be located at `examples/n8n/workflow_triaje.json` (batch and webhook) and `examples/n8n/workflow_triaje_chat.json` (chat), with a Dockerfile at `examples/n8n/Dockerfile` and a README at `examples/n8n/README.md`.

#### Scenario: Dual workflow file structure
- **WHEN** a participant navigates to `examples/n8n/`
- **THEN** they SHALL find `workflow_triaje.json`, `workflow_triaje_chat.json`, `Dockerfile`, and `README.md`

### Requirement: Chat workflow documented in n8n README
The `examples/n8n/README.md` SHALL document the chat workflow as an interactive alternative to batch execution and curl, with step-by-step instructions to open **"Triaje de Siniestros — Chat IA"** and use the in-UI chatbox.

#### Scenario: Participant discovers chat option
- **WHEN** a participant reads the testing section of the n8n README
- **THEN** they SHALL find the chat workflow described as a way to create and triage a new custom claim interactively

### Requirement: Configuration checklist
The README SHALL include a checklist of all credentials and IDs that need configuration before the workflow can run (Gemini API key only; Gmail OAuth and Google Sheets ID are no longer required since those nodes are replaced by local Code nodes).

#### Scenario: Participant reviews checklist
- **WHEN** a participant reads the configuration checklist
- **THEN** they SHALL find only the Gemini API key as a required credential, with a note that logging is handled automatically via local markdown files

### Requirement: Testing instructions prioritize UI execution
The README SHALL present clicking "Execute workflow" as the primary testing method. The curl-based webhook testing SHALL be documented as an alternative method.

#### Scenario: Participant tests via UI
- **WHEN** a participant reads the testing instructions
- **THEN** the first method described SHALL be clicking "Execute workflow" to run all built-in test cases, with curl documented as a secondary option

### Requirement: Testing instructions with curl
The README SHALL include a curl command example to test the webhook endpoint.

#### Scenario: Participant tests webhook
- **WHEN** a participant runs the provided curl command against `http://localhost:5678`
- **THEN** the webhook SHALL receive the test claim and return the agent's triage response
