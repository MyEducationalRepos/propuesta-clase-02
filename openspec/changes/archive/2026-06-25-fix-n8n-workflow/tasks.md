## 1. Fix workflow JSON

- [x] 1.1 Replace the "Buscar Poliza" `toolWorkflow` node with a `toolCode` node containing inline JavaScript that mirrors `consultar_poliza()` from `agente_triaje.py`
- [x] 1.2 Replace the "Buscar Liquidador" `toolWorkflow` node with a `toolCode` node containing inline JavaScript that mirrors `asignar_liquidador()` from `agente_triaje.py`
- [x] 1.3 Fix the credential key from `googleGeminiApi` to `googlePalmApi` in the Gemini node
- [x] 1.4 Set the credential ID in the workflow to a known value (e.g., `"id": "1"`) that matches what the init script will create

## 2. Auto-provision credential

- [x] 2.1 Add `N8N_PUBLIC_API_ENABLED=true` and a static `N8N_API_KEY` to docker-compose.yml
- [x] 2.2 Rewrite `init-workflows.sh` to: start n8n in background, wait for readiness, create credential via REST API using `GOOGLE_API_KEY`, import workflow, then `wait` on n8n process
- [x] 2.3 Pin n8n Docker image to a specific version tag instead of `:latest` in the Dockerfile

## 3. Update documentation

- [x] 3.1 Update `examples/n8n/README.md`: remove manual credential setup section, note that credential is auto-provisioned, update node descriptions table (toolCode instead of toolWorkflow)
- [x] 3.2 Update root `README.md`: simplify n8n instructions (no manual API key step inside n8n)

## 4. Verify

- [x] 4.1 Run `docker compose build n8n` and `docker compose up n8n`, confirm workflow loads with credential, send a test curl request and get a valid agent response
