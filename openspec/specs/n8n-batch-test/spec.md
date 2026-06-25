## ADDED Requirements

### Requirement: Manual Trigger runs all test cases
The workflow SHALL include a Manual Trigger node that, when activated via the "Execute workflow" button in the n8n UI, runs all 6 built-in test cases through the agent sequentially.

#### Scenario: Student clicks Execute workflow
- **WHEN** a student clicks the "Execute workflow" button in the n8n canvas
- **THEN** the workflow SHALL process all 6 test cases through the agent, with each execution visible on the canvas

### Requirement: Test cases match ADK example
The 6 test cases SHALL match the AVISOS list in `examples/adk/agente_triaje.py`: (1) standard low severity, (2) expired policy, (3) high severity with reinsurer notice, (4) incomplete data, (5) earthquake special rule, (6) non-existent policy.

#### Scenario: Same cases in both examples
- **WHEN** a student compares the n8n test cases with the ADK test cases
- **THEN** they SHALL find the same 6 claim notices used in both examples

### Requirement: Test case items use webhook-compatible structure
Each test case item SHALL use the structure `{ body: { aviso: "..." } }` so the agent node's input expression works identically for both the webhook and the manual trigger paths.

#### Scenario: Agent receives test case input
- **WHEN** the Manual Trigger fires and the test cases Code node outputs items
- **THEN** each item SHALL have `body.aviso` containing the claim notice text, matching the webhook payload structure

### Requirement: All test case results are logged
Each of the 6 test cases SHALL produce an entry in `data/log_triaje.md`. Cases classified as Alta SHALL also produce an entry in `data/alertas_reaseguro.md`.

#### Scenario: Log files after full batch execution
- **WHEN** all 6 test cases have been processed
- **THEN** `data/log_triaje.md` SHALL contain 6 new rows (one skipped for expired/missing policy is acceptable) and `data/alertas_reaseguro.md` SHALL contain rows for each Alta severity case
