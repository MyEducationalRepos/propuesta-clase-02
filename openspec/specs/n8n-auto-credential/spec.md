## ADDED Requirements

### Requirement: Gemini credential provisioned automatically at startup

The init script SHALL create a Google Gemini (PaLM) API credential in n8n's database using the `GOOGLE_API_KEY` environment variable. The credential SHALL be created via the n8n REST API (`POST /api/v1/credentials`) after n8n is ready. The workflow JSON SHALL reference this credential by its known ID.

#### Scenario: First startup with valid API key
- **WHEN** the container starts with `GOOGLE_API_KEY=AIzaSy...` in the environment
- **THEN** the init script creates a credential of type `googlePalmApi` with the API key value and the workflow's Gemini node uses it without manual configuration

#### Scenario: Startup without API key
- **WHEN** the container starts without `GOOGLE_API_KEY` set
- **THEN** the init script logs a warning and skips credential creation; the workflow loads but the Gemini node will fail at runtime with a missing credential error

### Requirement: Workflow uses correct credential type key

The workflow JSON SHALL reference the Gemini credential with the key `googlePalmApi` (not `googleGeminiApi`). This matches the internal type name used by n8n's `lmChatGoogleGemini` node.

#### Scenario: Credential resolution
- **WHEN** n8n loads the workflow and resolves the Gemini node's credentials
- **THEN** it finds the credential by type `googlePalmApi` and connects successfully

### Requirement: n8n API enabled for credential provisioning

The docker-compose.yml SHALL set `N8N_PUBLIC_API_ENABLED=true` and provide a static `N8N_API_KEY` so the init script can authenticate to the REST API.

#### Scenario: API accessible from init script
- **WHEN** the init script sends a POST request to `http://localhost:5678/api/v1/credentials` with the API key header
- **THEN** n8n accepts the request and creates the credential

### Requirement: Init script waits for n8n readiness

The init script SHALL poll n8n's health endpoint in a loop before attempting credential creation. It SHALL time out after a reasonable period (30 seconds) and proceed without the credential if n8n fails to start.

#### Scenario: Normal startup
- **WHEN** n8n starts and becomes ready within 30 seconds
- **THEN** the init script detects readiness, creates the credential, and imports the workflow

#### Scenario: Slow startup
- **WHEN** n8n takes more than 30 seconds to become ready
- **THEN** the init script logs a timeout warning and starts n8n anyway (workflow loads but credential may be missing)
