## 1. n8n workflow changes

- [x] 1.1 Add a Manual Trigger node to `workflow_triaje.json`
- [x] 1.2 Add a "Casos de Prueba" Code node that outputs 6 items (matching ADK's AVISOS), each with `{ body: { aviso: "..." } }` structure
- [x] 1.3 Wire: Manual Trigger -> Casos de Prueba -> Agente de Triaje (existing agent node)
- [x] 1.4 Keep the existing Webhook -> Agente de Triaje path unchanged

## 2. Documentation

- [x] 2.1 Update `examples/n8n/README.md`: make "Execute workflow" the primary test method, curl as secondary
- [x] 2.2 Update node descriptions table to include Manual Trigger and Casos de Prueba nodes

## 3. Verify

- [x] 3.1 Rebuild n8n, click "Execute workflow" in UI, confirm all 6 cases are processed and log files are populated
- [x] 3.2 Confirm webhook path still works via curl
