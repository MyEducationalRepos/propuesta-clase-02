## Why

Students click "Execute workflow" in n8n and nothing happens because the webhook trigger waits for an external HTTP request. The ADK example runs all 6 test cases on startup, but n8n has no equivalent. Both examples should run a complete set of test cases with a single action so students can compare agent behavior side by side.

## What Changes

- Add a Manual Trigger node to the n8n workflow so clicking "Execute workflow" runs all test cases without curl.
- Add a Code node with the same 6 test cases from the ADK example, outputting them as individual items that flow through the agent sequentially.
- Keep the existing webhook trigger for external API use (both triggers coexist).
- Verify the ADK example runs all cases correctly (it already has the 6-case batch in `AVISOS`).
- Update READMEs to document the one-click execution flow.

## Capabilities

### New Capabilities

- `n8n-batch-test`: Manual trigger with built-in test cases for one-click execution in the n8n UI. Generates 6 claim notices that the agent processes sequentially, with results logged to local markdown files.

### Modified Capabilities

- `n8n-example`: README updated to document the "Execute workflow" button as the primary testing method instead of curl.

## Impact

- `examples/n8n/workflow_triaje.json`: Add Manual Trigger node, add test cases Code node, wire to existing agent flow.
- `examples/n8n/README.md`: Rewrite testing instructions to prioritize the UI button.
- `examples/adk/README.md`: Verify and clarify that all 6 cases run on startup.
