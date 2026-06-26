## MODIFIED Requirements

### Requirement: Chat Trigger as entry point

The chat workflow SHALL use n8n's Chat Trigger node (`@n8n/n8n-nodes-langchain.chatTrigger`) as its sole trigger. The user message SHALL flow to the AI Agent via `$json.chatInput`. The Chat Trigger `responseMode` SHALL be `lastNode` so the chat widget receives the agent triage text when logging nodes run after the agent.

#### Scenario: Participant sends a claim in chat

- **WHEN** a participant types a claim description in the n8n chat panel and sends it
- **THEN** the AI Agent node SHALL receive the message as input and produce a triage response visible in the chat

#### Scenario: Documented example returns structured reply

- **WHEN** a participant pastes the README example claim for POL-2024-003 (robo en farmacia, 300 UF)
- **THEN** the chat panel SHALL display a structured triage answer containing policy status, severity, and liquidador (not `[No response received]`)
