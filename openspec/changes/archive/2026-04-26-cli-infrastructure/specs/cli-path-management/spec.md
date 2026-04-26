## ADDED Requirements

### Requirement: Centralized path constants
The `cli/core/paths.py` module SHALL define all file system paths used by YMOS as a single source of truth.

#### Scenario: Path resolution from YMOS root
- **WHEN** any CLI command needs to locate a state machine file
- **THEN** it calls `Paths.state / "holdings.md"` instead of hardcoding the path

#### Scenario: Auto-detect YMOS root
- **WHEN** the Paths class is initialized without arguments
- **THEN** it walks up from CWD to find the directory containing CLAUDE.md and uses that as root

### Requirement: Report listing
The `ymos report list` command SHALL list available reports by type and date.

#### Scenario: List latest reports
- **WHEN** user runs `ymos report list --type radar --latest`
- **THEN** system finds the most recent radar report file and prints its path

#### Scenario: List by date
- **WHEN** user runs `ymos report list --type insight --date 2026-04-26`
- **THEN** system prints the path to the insight report for that date, or "not found"

### Requirement: Migration command
The `ymos migrate` command SHALL move existing runtime data from old paths to new data/ structure.

#### Scenario: Migrate existing data
- **WHEN** user runs `ymos migrate` on a system with old directory structure
- **THEN** system moves all reports, state machines, stock directories to data/ following the new layout
