## Context

The project ships one n8n workflow (`workflow_triaje.json`) imported at container start via `init-workflows.sh`. It supports batch execution (Manual Trigger + 6 test cases) and a POST webhook (`/webhook/triaje-siniestro`). Participants who want to type a custom claim and see a conversational reply must use curl or edit test data. n8n 2.x provides a **Chat Trigger** node (`@n8n/n8n-nodes-langchain.chatTrigger`) that exposes an in-UI chat panel when the workflow is active.

## Goals / Non-Goals

**Goals:**

- Deliver a second workflow with the same triage agent, Gemini model, tools, severity branch, and markdown logging.
- Enable participants to open a chatbox in n8n, paste or type a new claim, and receive the agent's structured triage response.
- Import both workflows automatically on `docker compose up n8n` with zero extra configuration.

**Non-Goals:**

- Replacing or removing the existing batch/webhook workflow.
- Building a custom external chat UI (Slack, Teams, embeddable widget).
- Multi-session memory across unrelated chat conversations (n8n chat session memory is limited to the current chat session only).
- Changing ADK example or lesson plan content beyond a brief README mention.

## Decisions

### 1. Separate workflow file instead of extending the existing JSON

**Choice:** Create `workflow_triaje_chat.json` as a standalone workflow with its own `id` (`triaje-siniestros-chat`).

**Rationale:** Keeps the classroom batch demo untouched. Chat Trigger wiring differs from Manual Trigger + Webhook; a separate file is easier to maintain and import independently.

**Alternative considered:** Add Chat Trigger as a third entry point in `workflow_triaje.json`. Rejected because n8n chat workflows are typically self-contained and mixing three triggers on one canvas confuses participants.

### 2. Chat Trigger as sole entry point for the chat workflow

**Choice:** Single **When chat message received** node feeding the AI Agent. User message maps to `$json.chatInput` (n8n Chat Trigger default).

**Rationale:** Minimal surface area; participants see one clear path: chat in, triage out.

**Alternative considered:** Chat Trigger plus webhook in the same workflow. Rejected for scope; the original workflow already covers webhook testing.

### 3. Reuse agent configuration verbatim

**Choice:** Copy the same system prompt, Gemini 2.5 Flash settings (temperature 0.2), `Buscar_Poliza` and `Buscar_Liquidador` tool code, severity If node, and markdown logging nodes from `workflow_triaje.json`.

**Rationale:** Parity with the batch example; only the trigger differs.

### 4. Agent prompt input binding

**Choice:** Set AI Agent `text` to `={{ $json.chatInput }}` instead of `={{ $json.body.aviso }}`.

**Rationale:** Chat Trigger exposes the user message in `chatInput`. Logging nodes continue to read `$('Agente de Triaje').item.json.output`.

### 5. Dual import in init script

**Choice:** Extend `init-workflows.sh` to import both JSON files and publish both by id:

```sh
n8n import:workflow --input=/home/node/workflows/workflow_triaje.json
n8n publish:workflow --id=triaje-siniestros
n8n import:workflow --input=/home/node/workflows/workflow_triaje_chat.json
n8n publish:workflow --id=triaje-siniestros-chat
```

**Rationale:** Matches existing credential and publish pattern; no Dockerfile change beyond COPY of the new JSON.

### 6. Workflow naming and activation

**Choice:** Display name **"Triaje de Siniestros — Chat IA"**, `active: true`, Spanish meta description noting chat usage.

**Rationale:** Distinguishes clearly from **"Triaje de Siniestros — Agente IA"** in the Workflows list.

## Risks / Trade-offs

- **[Chat panel not visible until workflow is active]** → README must state: activate toggle, open workflow, use **Chat** tab/button in n8n UI.
- **[Duplicate logging from both workflows]** → Acceptable; both append to the same markdown files with timestamps. Document that chat and batch runs share `data/`.
- **[n8n Chat Trigger API shape changes across versions]** → Pin n8n image (`n8nio/n8n:2.27.1`) already in Dockerfile; test chat flow after import.
- **[Long agent runs in chat UX]** → Same 1-2 minute latency as batch; README sets expectation that the chat waits for tool calls.

## Migration Plan

1. Add `workflow_triaje_chat.json` and update `init-workflows.sh`.
2. Rebuild n8n container: `docker compose down && docker compose up n8n --build`.
3. Verify both workflows appear and chat responds to a sample claim.
4. Rollback: revert init script and remove chat JSON; rebuild container.

## Open Questions

- None blocking. Optional future work: link chat workflow from lesson plan slide (out of scope here).
