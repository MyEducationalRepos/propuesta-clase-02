## Why

The n8n workflow currently has Gmail and Google Sheets nodes disabled because they require OAuth credentials students cannot configure in class. Students need to see tangible results of the agent's decisions (reinsurer alerts for high severity, log entries for all cases) without external service dependencies.

## What Changes

- Re-enable the "If Severidad Alta?" node to branch execution after the agent responds.
- Replace the disabled Gmail node with a Code node that appends a row to a local markdown file (`/data/alertas_reaseguro.md`) for high-severity cases.
- Replace the disabled Google Sheets node with a Code node that appends a row to a local markdown file (`/data/log_triaje.md`) for all processed cases.
- Mount a Docker volume so both markdown files persist on the host and students can open them directly.
- Both files use a markdown table format so they render nicely in any viewer.

## Capabilities

### New Capabilities
- `n8n-local-markdown-log`: Write agent triage results to local markdown files instead of external services (Gmail, Google Sheets). Two output files: alerts for reinsurers (high severity only) and a full triage log (all cases).

### Modified Capabilities
- `n8n-example`: Re-enable the If/notification/log branch that was disabled, now wired to local Code nodes instead of Gmail/Sheets.

## Impact

- `examples/n8n/workflow_triaje.json`: Re-enable disabled nodes, replace Gmail/Sheets with Code nodes, rewire connections.
- `docker-compose.yml`: Add volume mount for `./data:/data` on the n8n service.
- `examples/n8n/README.md`: Document the output files and where to find them.
