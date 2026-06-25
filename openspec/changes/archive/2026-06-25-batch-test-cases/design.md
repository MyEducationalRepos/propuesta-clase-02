## Context

The n8n workflow uses a Webhook trigger (`POST /webhook/triaje-siniestro`), which only fires on external HTTP requests. Students must use curl to test it, and each curl processes one claim. The ADK example already embeds 6 test cases and runs them all on `docker compose up adk`. The n8n example needs the same one-click experience via the "Execute workflow" button.

## Goals / Non-Goals

**Goals:**
- Clicking "Execute workflow" in n8n runs all 6 test cases through the agent, with visible execution on the canvas.
- Each case produces entries in `data/log_triaje.md` and (for Alta) `data/alertas_reaseguro.md`.
- The same 6 test cases from the ADK example are used in n8n for classroom comparison.
- The existing webhook trigger remains functional for external API use.

**Non-Goals:**
- Making the ADK output match n8n output format (they use different output mechanisms).
- Adding new test cases beyond the existing 6.
- Removing the webhook trigger.

## Decisions

### 1. Add a Manual Trigger node as a second entry point

**Rationale:** n8n supports multiple trigger nodes in one workflow. A Manual Trigger fires when the user clicks "Execute workflow". It coexists with the webhook trigger -- each fires independently.

**Alternative considered:** Replacing the webhook with the Manual Trigger. Rejected because the webhook is useful for external integration demos and curl examples in the README.

### 2. Code node generates 6 items (one per test case)

**Rationale:** A Code node after the Manual Trigger outputs an array of 6 items, each with an `aviso` field matching the ADK test cases. n8n processes downstream nodes once per item, so the agent evaluates each case sequentially. The canvas shows all 6 executions flowing through the nodes.

### 3. Merge both trigger paths before the agent via a common structure

**Rationale:** Both the webhook (single `$json.body.aviso`) and the Manual Trigger + Code node (multiple items with `$json.aviso`) need to feed the same agent node. The agent's input expression `={{ $json.body.aviso }}` must handle both cases. Solution: the test cases Code node outputs items with `{ body: { aviso: "..." } }` to match the webhook's structure. No change to the agent node needed.

### 4. No changes to ADK

**Rationale:** The ADK example already runs all 6 cases via `ejecutar_todos()` on startup. It works correctly. No modifications needed.

## Risks / Trade-offs

- [Risk] n8n processes 6 agent calls sequentially, which takes ~60-90 seconds total. -> Acceptable for classroom demo; students see each case completing one by one on the canvas.
- [Risk] Manual Trigger path bypasses webhook, so `responseMode: "lastNode"` applies to the last item's last node output only. -> Not a problem since there's no HTTP caller waiting for a response on the manual path.
- [Trade-off] Two trigger nodes make the canvas slightly more complex visually. -> Acceptable; it demonstrates that workflows can have multiple entry points.
