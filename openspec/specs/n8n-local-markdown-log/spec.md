## ADDED Requirements

### Requirement: High severity cases are logged to a reinsurer alerts file
The workflow SHALL append a row to `/data/alertas_reaseguro.md` when the agent classifies a claim as Alta severity. The row SHALL include timestamp, policy number, insured party, severity, and the full agent output.

#### Scenario: Alta severity claim triggers reinsurer alert
- **WHEN** a claim is submitted with severity classified as Alta
- **THEN** a new row SHALL be appended to `/data/alertas_reaseguro.md` with the triage details

#### Scenario: Non-alta severity claim does not trigger reinsurer alert
- **WHEN** a claim is submitted with severity Baja or Media
- **THEN** no row SHALL be appended to `/data/alertas_reaseguro.md`

### Requirement: All processed cases are logged to a triage log file
The workflow SHALL append a row to `/data/log_triaje.md` for every claim processed, regardless of severity. The row SHALL include timestamp, policy number, severity, and a summary of the agent output.

#### Scenario: Any processed claim is logged
- **WHEN** a claim is submitted and the agent produces a triage response
- **THEN** a new row SHALL be appended to `/data/log_triaje.md`

### Requirement: Log files use markdown table format
Both output files SHALL use markdown table format with a header row. If the file does not exist, the Code node SHALL create it with the header row before appending data.

#### Scenario: First write creates the file with header
- **WHEN** a claim is processed and the target markdown file does not yet exist
- **THEN** the Code node SHALL create the file with a header row and then append the data row

#### Scenario: Subsequent writes append to existing file
- **WHEN** a claim is processed and the target markdown file already exists
- **THEN** the Code node SHALL append a data row without duplicating the header

### Requirement: Log files persist on the host via Docker volume
The `docker-compose.yml` SHALL mount `./data:/data` on the n8n service so that output files are accessible from the host filesystem.

#### Scenario: Student opens log files from the project folder
- **WHEN** a student navigates to `./data/` on their host machine after running the workflow
- **THEN** they SHALL find `alertas_reaseguro.md` and `log_triaje.md` with the logged results
