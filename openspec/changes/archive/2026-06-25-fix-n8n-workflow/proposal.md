## Why

The n8n workflow example is broken out of the box. Two critical issues prevent classroom use: (1) the Gemini API credential must be configured manually inside the n8n UI because the workflow JSON contains a placeholder `"id": "CONFIGURAR"`, and (2) the "Buscar Poliza" and "Buscar Liquidador" tool nodes reference sub-workflows that don't exist (`workflowId.value: ""`), causing immediate failures when the agent tries to use them. A non-technical audience cannot debug either problem.

## What Changes

- Replace the two `toolWorkflow` nodes (Buscar Poliza, Buscar Liquidador) with `toolCode` nodes containing inline JavaScript that returns the same mock data as the ADK Python example. This eliminates the dependency on nonexistent sub-workflows.
- Auto-provision the Google Gemini credential at container startup using `n8n import:credentials` (or the REST API) so the workflow JSON references a real credential instead of `"CONFIGURAR"`.
- Update `init-workflows.sh` to handle credential injection from the `GOOGLE_API_KEY` environment variable before importing the workflow.
- Update `workflow_triaje.json` to use the new self-contained tool nodes and a valid credential reference.
- Update `examples/n8n/README.md` to reflect that credential configuration is now automatic.

## Capabilities

### New Capabilities

- `n8n-self-contained-tools`: Inline JavaScript tool nodes (toolCode) for Buscar Poliza and Buscar Liquidador, containing the same mock data as the ADK example, removing the dependency on external sub-workflows.
- `n8n-auto-credential`: Automatic provisioning of the Google Gemini API credential at container startup from the GOOGLE_API_KEY env var, so users never touch credential configuration.

### Modified Capabilities

(none -- no existing specs)

## Impact

- `examples/n8n/workflow_triaje.json`: Two nodes replaced, credential ID updated.
- `examples/n8n/init-workflows.sh`: Credential injection logic added.
- `examples/n8n/Dockerfile`: May need changes if new files are copied.
- `examples/n8n/README.md`: Remove manual credential setup section.
- `README.md` (root): Simplify n8n instructions (no manual API key step).
