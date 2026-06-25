## MODIFIED Requirements

### Requirement: Configuration checklist
The README SHALL include a checklist of all credentials and IDs that need configuration before the workflow can run (Gemini API key only; Gmail OAuth and Google Sheets ID are no longer required since those nodes are replaced by local Code nodes).

#### Scenario: Participant reviews checklist
- **WHEN** a participant reads the configuration checklist
- **THEN** they SHALL find only the Gemini API key as a required credential, with a note that logging is handled automatically via local markdown files

### Requirement: Node descriptions in README
The README SHALL include a table describing each node in the workflow: its name, type, and purpose in the triage flow. The table SHALL reflect the Code nodes for local logging instead of Gmail/Google Sheets.

#### Scenario: Participant understands workflow nodes
- **WHEN** a participant reads the node descriptions
- **THEN** they SHALL find every node from the JSON described with its role (trigger, agent, model, tools, conditional, local alert writer, local log writer)
