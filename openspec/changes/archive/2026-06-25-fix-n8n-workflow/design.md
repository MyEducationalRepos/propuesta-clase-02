## Context

The n8n workflow (`workflow_triaje.json`) has three bugs that make it non-functional out of the box:

1. The credential key in the workflow JSON is `googleGeminiApi` but the node type `lmChatGoogleGemini` internally requests `googlePalmApi`. The credential reference never resolves.
2. The "Buscar Poliza" and "Buscar Liquidador" nodes are `toolWorkflow` type pointing to sub-workflows with empty `workflowId.value: ""`. No sub-workflows exist.
3. The credential `"id": "CONFIGURAR"` is a placeholder. Even with the correct type key, there is no matching credential in n8n's database.

The audience is non-technical insurance professionals. Zero manual configuration is the target.

## Goals / Non-Goals

**Goals:**
- The n8n example works end-to-end after `docker compose up n8n` with zero manual steps beyond login.
- The Gemini credential is provisioned automatically from `GOOGLE_API_KEY` in `.env`.
- The tool nodes return the same mock data as the ADK Python example.

**Non-Goals:**
- Real API integrations (Gmail, Google Sheets) remain non-functional placeholders.
- No new n8n features beyond fixing existing broken nodes.

## Decisions

### D1: Replace `toolWorkflow` with `toolCode` nodes

**Choice:** Use `@n8n/n8n-nodes-langchain.toolCode` (Custom Code Tool) with inline JavaScript.

**Why:** `toolWorkflow` requires separate sub-workflows to exist. Creating and importing multiple workflows adds complexity and fragility. `toolCode` is self-contained: the mock data lives inside the workflow JSON itself. The JavaScript mirrors the Python dicts from `agente_triaje.py`.

**Alternative rejected:** Create separate sub-workflow JSON files and import them. More files, more import ordering issues, more failure modes.

### D2: Auto-provision credential via REST API after n8n starts

**Choice:** In `init-workflows.sh`, start n8n in the background, wait for it to be ready, create the credential via `POST /api/v1/credentials`, import the workflow, then keep n8n running in the foreground.

**Why:** The CLI command `n8n import:credentials` requires the credential JSON to have an encryption-compatible format. Using the REST API with plain-text data is simpler and the API handles encryption internally. It also lets us set the credential ID, which we reference in the workflow JSON.

**Requires:** `N8N_PUBLIC_API_ENABLED=true` and an `N8N_API_KEY` environment variable in docker-compose.yml.

**Alternative rejected:** `n8n import:credentials --input=file.json` before starting n8n. Riskier: n8n docs say plain-text import works, but community reports suggest issues with encryption keys and format mismatches. The REST API is the documented, supported path for credential creation.

### D3: Fix credential key from `googleGeminiApi` to `googlePalmApi`

**Choice:** Update the workflow JSON credential key to `googlePalmApi`.

**Why:** The n8n source code for `lmChatGoogleGemini` calls `this.getCredentials('googlePalmApi')`. The current key `googleGeminiApi` silently fails to match. This is a legacy naming issue in n8n (PaLM was renamed to Gemini but the internal type was not updated).

### D4: Wait-for-ready loop in init script

**Choice:** Poll `http://localhost:5678/healthz` (or `/api/v1/workflows`) in a loop before creating the credential.

**Why:** n8n needs time to initialize its database. The credential API call will fail if n8n is not ready. A simple `until curl -sf ... ; do sleep 1; done` loop handles this.

## Risks / Trade-offs

- [n8n API breaking changes] The credential creation API format may change between n8n versions. Mitigation: pin the n8n Docker image to a specific version tag instead of `:latest`.
- [Startup delay] The wait-for-ready loop adds seconds to first boot. Mitigation: acceptable for a classroom demo; the loop exits as soon as n8n is ready.
- [API key in env var] The `N8N_API_KEY` for internal use is exposed in docker-compose.yml. Mitigation: it is a local-only classroom demo, not production. The key is only used for the single credential provisioning call.
