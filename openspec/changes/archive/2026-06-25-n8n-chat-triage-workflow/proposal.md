## Why

The existing n8n triage workflow is powerful for batch demos and webhook integration, but participants cannot interact with the agent conversationally inside n8n. A chat-enabled variant lets insurance professionals type a new claim in a chatbox, see the agent reason and respond in real time, and experience the multi-turn nature of agentic AI without curl or pre-built test cases.

## What Changes

- Add a second n8n workflow JSON (`workflow_triaje_chat.json`) with a Chat Trigger entry point alongside the same triage agent, tools, and logging nodes.
- Update `init-workflows.sh` to import and publish both workflows on container start.
- Extend `examples/n8n/README.md` with a dedicated section: how to open the chat workflow, start a conversation, submit a new claim, and read the agent reply.
- Update the top-level `README.md` to mention the chat workflow as an optional hands-on path.
- Reuse the same Gemini credential, mock policy/liquidator tools, and local markdown logging (`data/log_triaje.md`, `data/alertas_reaseguro.md`).

## Capabilities

### New Capabilities

- `n8n-chat-triage`: Chat-triggered n8n workflow for interactive claim triage with in-UI chatbox, same agent logic as the batch workflow, and documentation for classroom use.

### Modified Capabilities

- `n8n-example`: Extend requirements to cover a second workflow file, dual import on startup, and README instructions for the chat variant.
- `docker-infra`: Extend n8n container init to import and publish both workflow JSON files.

## Impact

- New file: `examples/n8n/workflow_triaje_chat.json`.
- Modified: `examples/n8n/init-workflows.sh`, `examples/n8n/README.md`, `README.md`.
- No new host dependencies; same Docker Compose service and `.env` configuration.
- Existing batch workflow (`workflow_triaje.json`) remains unchanged in behavior.
