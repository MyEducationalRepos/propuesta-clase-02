## 1. Workflow fix

- [x] 1.1 Change Chat Trigger `options.responseMode` from `streaming` to `lastNode` in `workflow_triaje_chat.json`
- [x] 1.2 Confirm terminal logging nodes (`Registro Log`, `Alerta Reaseguro`) return `{ output }` from the agent

## 2. Documentation

- [x] 2.1 Add "No response received" troubleshooting entry to `examples/n8n/README.md`

## 3. Verification

- [x] 3.1 Rebuild n8n container and paste POL-2024-003 example in chat; confirm structured triage reply appears
