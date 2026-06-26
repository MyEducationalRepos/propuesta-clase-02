## Why

The **Triaje de Siniestros — Chat IA** workflow returns `[No response received]` in the n8n chat panel instead of the agent's triage classification. Participants cannot complete the interactive classroom exercise because the chatbot appears broken. The Chat Trigger is configured for streaming while the AI Agent node does not enable streaming, and logging nodes run inline after the agent, which n8n does not support for chat reply delivery.

## What Changes

- Fix `workflow_triaje_chat.json` so a claim pasted in the chat panel produces a visible structured triage reply (policy, severity, liquidador).
- Align Chat Trigger `responseMode` with agent output delivery (`lastNode`) and ensure the terminal logging node returns `{ output }` for the chat widget.
- Enable streaming on the AI Agent only if we keep streaming mode; preferred fix is `lastNode` for reliability with downstream logging.
- Document the chat-no-response troubleshooting case in `examples/n8n/README.md`.

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `n8n-chat-triage`: Chat workflow must return agent triage text in the n8n chat UI for every valid claim submission, including the documented example (POL-2024-003, 300 UF).

## Impact

- `examples/n8n/workflow_triaje_chat.json` (response mode, optional agent streaming flag, connection layout)
- `examples/n8n/README.md` (troubleshooting for empty chat responses)
- No Docker, init script, or batch workflow changes required
