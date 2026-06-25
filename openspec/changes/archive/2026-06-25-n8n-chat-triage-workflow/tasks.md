## 1. Chat workflow JSON

- [x] 1.1 Create `examples/n8n/workflow_triaje_chat.json` with id `triaje-siniestros-chat`, name **"Triaje de Siniestros — Chat IA"**, and `active: true`
- [x] 1.2 Add Chat Trigger node (`@n8n/n8n-nodes-langchain.chatTrigger`) connected to the AI Agent with `text` bound to `={{ $json.chatInput }}`
- [x] 1.3 Copy AI Agent system prompt, Gemini 2.5 Flash node, `Buscar_Poliza` and `Buscar_Liquidador` tools from `workflow_triaje.json`
- [x] 1.4 Copy severity If branch, `Alerta Reaseguro`, and `Registro Log` nodes with the same markdown logging logic
- [x] 1.5 Wire all node connections (Chat Trigger → Agent → If → logging) and set Spanish meta description

## 2. Container import

- [x] 2.1 Update `examples/n8n/Dockerfile` to COPY `workflow_triaje_chat.json` into `/home/node/workflows/`
- [x] 2.2 Extend `examples/n8n/init-workflows.sh` to import and publish `triaje-siniestros-chat` after the batch workflow
- [x] 2.3 Rebuild and verify both workflows appear in n8n after `docker compose up n8n --build`

## 3. Documentation

- [x] 3.1 Add chat workflow section to `examples/n8n/README.md`: open workflow, activate, use chat panel, example claim text
- [x] 3.2 Add node description table for the chat workflow (Chat Trigger, Agent, model, tools, If, log writers)
- [x] 3.3 Update top-level `README.md` with a brief mention of the chat workflow as an interactive alternative

## 4. Verification

- [x] 4.1 Send a sample claim via n8n chat UI and confirm structured triage response in chat
- [x] 4.2 Confirm `data/log_triaje.md` receives a new row after a chat triage run
- [x] 4.3 Submit a high-severity chat claim and confirm `data/alertas_reaseguro.md` is updated
- [x] 4.4 Confirm existing batch workflow (`workflow_triaje.json`) still runs all 6 test cases unchanged
