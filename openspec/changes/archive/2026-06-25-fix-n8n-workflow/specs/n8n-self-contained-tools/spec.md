## ADDED Requirements

### Requirement: Buscar Poliza tool returns mock data inline

The workflow SHALL include a `toolCode` node named "Buscar Poliza" that receives a policy number as `query` and returns a JSON string with the policy data. The mock data SHALL match the `consultar_poliza` function in `agente_triaje.py`: policies POL-2024-001 through POL-2024-004 with their estado, ramo, suma_asegurada, deducible, and asegurado fields. If the policy is not found, it SHALL return `{"estado": "No encontrada", "mensaje": "Poliza no existe en el sistema"}`.

#### Scenario: Known policy lookup
- **WHEN** the agent calls Buscar Poliza with query "POL-2024-001"
- **THEN** the tool returns a JSON string containing `"estado": "Vigente"`, `"ramo": "Incendio"`, and the corresponding asegurado, suma_asegurada, deducible fields

#### Scenario: Unknown policy lookup
- **WHEN** the agent calls Buscar Poliza with query "POL-2024-999"
- **THEN** the tool returns `{"estado": "No encontrada", "mensaje": "Poliza no existe en el sistema"}`

#### Scenario: Policy extracted from natural text
- **WHEN** the agent passes a query string that contains "POL-2024-003" (possibly with surrounding text)
- **THEN** the JavaScript code SHALL extract the policy number using a regex and look it up in the mock data

### Requirement: Buscar Liquidador tool returns mock data inline

The workflow SHALL include a `toolCode` node named "Buscar Liquidador" that receives a JSON string with `ramo` and `severidad` fields as `query` and returns a JSON string with the assigned liquidador data. The mock data SHALL match the `asignar_liquidador` function in `agente_triaje.py`. If no match is found, it SHALL return the Pool General fallback.

#### Scenario: Known ramo and severidad combination
- **WHEN** the agent calls Buscar Liquidador with query containing ramo "Incendio" and severidad "Alta"
- **THEN** the tool returns a JSON string with liquidador "Maria Gonzalez" and cargo "Liquidador Senior"

#### Scenario: Unknown combination fallback
- **WHEN** the agent calls Buscar Liquidador with a ramo/severidad combination not in the mock data
- **THEN** the tool returns the Pool General fallback with "Asignacion manual requerida"

### Requirement: Tool nodes are connected to AI Agent

Both toolCode nodes SHALL be connected to the "Agente de Triaje" AI Agent node via the `ai_tool` connection type, replacing the previous `toolWorkflow` connections.

#### Scenario: Agent can invoke both tools
- **WHEN** a siniestro aviso is sent to the webhook containing a policy number and damage amount
- **THEN** the agent invokes Buscar Poliza, classifies severity, invokes Buscar Liquidador, and returns a structured response
