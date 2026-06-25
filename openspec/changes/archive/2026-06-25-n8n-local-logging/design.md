## Context

The n8n workflow has disabled Gmail/Sheets nodes because they need OAuth credentials students cannot set up in a classroom. The agent produces correct triage output but students see no persistent record of its decisions. We need a zero-config alternative that writes results locally.

## Goals / Non-Goals

**Goals:**
- Students see two output files after running the workflow: one with reinsurer alerts (alta only), one with a full triage log (all cases).
- Files are markdown tables, readable in any editor or GitHub.
- Files persist across container restarts via Docker volume.
- No external credentials or services required.

**Non-Goals:**
- Real email or spreadsheet integration.
- Concurrent-write safety (single user, classroom context).
- Log rotation or cleanup.

## Decisions

### 1. Use n8n Code nodes (JavaScript) instead of external services
**Rationale:** Code nodes run inline in n8n's JS Task Runner with no credentials. They can write to the filesystem using Node.js `fs` module. This replaces Gmail (Code node appending to `alertas_reaseguro.md`) and Google Sheets (Code node appending to `log_triaje.md`).

**Alternative considered:** Python Code nodes. Rejected because n8n 2.27.1's Python task runner is not available in the Docker image (logged warning on startup).

### 2. Markdown table format
**Rationale:** Renders natively in VS Code, GitHub, Obsidian, and any markdown viewer. Students can open the file and see formatted results without tools. Each Code node checks if the file exists; if not, writes the header row first, then appends a data row.

### 3. Docker volume mount `./data:/data`
**Rationale:** Files at `/data/` inside the container map to `./data/` on the host. Students open the files directly from the project folder. The directory is created automatically by Docker.

### 4. Agent node fans out to both Respond and If branches
**Rationale:** The response is sent immediately to the caller from the Agent (via `responseMode: lastNode`). In parallel, the If node evaluates severity and routes to the appropriate Code node. The If/Code branch can fail without affecting the webhook response.

## Risks / Trade-offs

- [Risk] Code node `fs.appendFileSync` fails if `/data` is not writable. -> Mitigated by Docker volume mount creating the directory with correct permissions.
- [Risk] Markdown table rows may break if agent output contains pipe characters (`|`). -> Low risk with structured prompts; acceptable for classroom use.
- [Trade-off] No real Gmail/Sheets integration. -> Acceptable; these are placeholders. The disabled nodes remain in the workflow as visual documentation of what a production version would include.
