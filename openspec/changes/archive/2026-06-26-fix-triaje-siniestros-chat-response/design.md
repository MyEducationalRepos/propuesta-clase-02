## Context

`workflow_triaje_chat.json` uses a Chat Trigger (`@n8n/n8n-nodes-langchain.chatTrigger` v1.3) with `options.responseMode: "streaming"`. The AI Agent node does not set `enableStreaming: true`. n8n surfaces this mismatch as `[No response received. This could happen if streaming is enabled in the trigger but disabled in agent node(s)]`.

The workflow also runs severity branching and markdown logging **inline after** the agent. n8n's Chat Trigger builder hint states that with `streaming` mode the agent should stream directly to the widget and side-effects (logging) should be on a parallel branch, not inline after the agent.

Participants follow `examples/n8n/README.md` and paste the documented POL-2024-003 example; they expect a structured triage reply in the chat panel within ~30 seconds.

## Goals / Non-Goals

**Goals:**

- Return the agent's structured triage text in the n8n chat UI for valid claim submissions.
- Keep the same agent prompt, tools, severity branch, and markdown logging behavior.
- Fix survives `docker compose up n8n --build` re-import via `init-workflows.sh`.

**Non-Goals:**

- Token-by-token streaming UX (nice-to-have, not required for class).
- Changing the batch workflow or ADK example.
- External chat UI (Slack, embeddable widget).

## Decisions

### 1. Use `lastNode` response mode instead of `streaming`

**Choice:** Set Chat Trigger `options.responseMode` to `"lastNode"`.

**Rationale:** The workflow has downstream logging nodes after the agent. `lastNode` mode sends the final node's `output` field to the chat widget. The existing `Registro Log` and `Alerta Reaseguro` nodes already return `{ output }` copied from the agent, satisfying n8n's contract. This avoids streaming/WebSocket edge cases and does not require enabling streaming on the agent or Gemini sub-node.

**Alternative considered:** Keep `streaming` and set `enableStreaming: true` on the agent. Rejected because inline logging after the agent still conflicts with n8n's recommended chat topology; streaming adds complexity without classroom benefit.

### 2. Keep inline logging topology

**Choice:** Retain `Agent -> If -> Log / Alerta` chain; rely on terminal Code nodes returning `{ output }`.

**Rationale:** Minimal diff. `Registro Log` is the last node on both If branches and already echoes agent output. No connection rewiring needed.

**Alternative considered:** Parallel logging branch off the agent. Deferred; only needed if `lastNode` proves unreliable for Alta-severity dual-branch runs.

### 3. README troubleshooting entry

**Choice:** Add a short "No response received" subsection under Errores comunes explaining the streaming mismatch and that the fix is applied in the shipped workflow.

**Rationale:** Helps instructors who cached an older workflow JSON in a running container.

## Risks / Trade-offs

- **[Alta severity runs two terminal nodes in parallel]** → Both return `{ output }`; n8n picks one last-executed node. Acceptable; chat still shows triage text. Monitor in manual test.
- **[Participants on stale container without rebuild]** → README note to `docker compose up n8n --build`.
- **[n8n version drift changes responseMode values]** → Image pinned in Dockerfile (`n8nio/n8n:2.27.1`); re-test after upgrades.

## Migration Plan

1. Update `workflow_triaje_chat.json` response mode.
2. Update `examples/n8n/README.md` troubleshooting.
3. Rebuild: `docker compose down && docker compose up n8n --build`.
4. Manual test: paste POL-2024-003 example in chat; confirm structured reply.
5. Rollback: revert JSON and README; rebuild container.

## Open Questions

- None blocking.
