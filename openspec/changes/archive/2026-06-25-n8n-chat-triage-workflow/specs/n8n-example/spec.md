## MODIFIED Requirements

### Requirement: Node descriptions in README

The README SHALL include a table describing each node in both workflows: its name, type, and purpose in the triage flow. The batch workflow table SHALL include the Manual Trigger and test cases Code node in addition to the existing nodes. The chat workflow table SHALL include the Chat Trigger node in addition to the agent, model, tools, conditional, and logging nodes.

#### Scenario: Participant understands batch workflow nodes

- **WHEN** a participant reads the node descriptions for the batch workflow
- **THEN** they SHALL find every node from the JSON described with its role (manual trigger, test cases generator, webhook trigger, agent, model, tools, conditional, local alert writer, local log writer)

#### Scenario: Participant understands chat workflow nodes

- **WHEN** a participant reads the node descriptions for the chat workflow
- **THEN** they SHALL find the Chat Trigger, AI Agent, Gemini model, policy tool, liquidator tool, severity conditional, alert writer, and log writer described with their roles

## ADDED Requirements

### Requirement: Dual n8n workflow files exist

The n8n workflows SHALL be located at `examples/n8n/workflow_triaje.json` (batch and webhook) and `examples/n8n/workflow_triaje_chat.json` (chat), with a Dockerfile at `examples/n8n/Dockerfile` and a README at `examples/n8n/README.md`.

#### Scenario: File structure after restructuring

- **WHEN** a participant navigates to `examples/n8n/`
- **THEN** they SHALL find `workflow_triaje.json`, `workflow_triaje_chat.json`, `Dockerfile`, and `README.md`

### Requirement: Chat workflow documented in n8n README

The `examples/n8n/README.md` SHALL document the chat workflow as an interactive alternative to batch execution and curl, with step-by-step instructions to open **"Triaje de Siniestros — Chat IA"** and use the in-UI chatbox.

#### Scenario: Participant discovers chat option

- **WHEN** a participant reads the testing section of the n8n README
- **THEN** they SHALL find the chat workflow described as a way to create and triage a new custom claim interactively
