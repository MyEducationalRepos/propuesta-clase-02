## MODIFIED Requirements

### Requirement: Node descriptions in README
The README SHALL include a table describing each node in the workflow: its name, type, and purpose in the triage flow. The table SHALL include the Manual Trigger and test cases Code node in addition to the existing nodes.

#### Scenario: Participant understands workflow nodes
- **WHEN** a participant reads the node descriptions
- **THEN** they SHALL find every node from the JSON described with its role (manual trigger, test cases generator, webhook trigger, agent, model, tools, conditional, local alert writer, local log writer)

### Requirement: Testing instructions prioritize UI execution
The README SHALL present clicking "Execute workflow" as the primary testing method. The curl-based webhook testing SHALL be documented as an alternative method.

#### Scenario: Participant tests via UI
- **WHEN** a participant reads the testing instructions
- **THEN** the first method described SHALL be clicking "Execute workflow" to run all built-in test cases, with curl documented as a secondary option
