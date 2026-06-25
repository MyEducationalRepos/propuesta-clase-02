## ADDED Requirements

### Requirement: Top-level README exists
The project root SHALL contain a `README.md` that introduces the repository, links to the lesson plan, and directs participants to the two example paths.

#### Scenario: Participant opens repository
- **WHEN** a participant opens the repository root (GitHub or local)
- **THEN** they SHALL see a README with: project title, one-paragraph description, prerequisite list, and links to `examples/adk/` and `examples/n8n/`

### Requirement: Prerequisites section
The README SHALL list Docker as the only required prerequisite, with a link to Docker Desktop installation. Google API key listed as the only credential needed.

#### Scenario: Participant checks prerequisites
- **WHEN** a participant reads the prerequisites section
- **THEN** they SHALL find Docker and a Google API key as the only requirements, with install/setup links

### Requirement: Quick start section
The README SHALL include a quick start with 3 steps: (1) clone, (2) `cp .env.copy .env` and set key, (3) `docker compose up adk` or `docker compose up n8n`.

#### Scenario: Participant follows quick start
- **WHEN** a participant follows the 3 quick start steps
- **THEN** they SHALL see the ADK agent process test claims within 2 minutes of cloning (after image build)

### Requirement: Project structure overview
The README SHALL include a tree or list showing the directory layout with one-line descriptions per entry.

#### Scenario: Participant reads structure overview
- **WHEN** a participant reads the project structure section
- **THEN** they SHALL understand where to find the lesson plan, ADK example, n8n example, and Docker configuration
