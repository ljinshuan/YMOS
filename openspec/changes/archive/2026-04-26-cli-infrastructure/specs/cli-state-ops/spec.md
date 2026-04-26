## ADDED Requirements

### Requirement: Read state machine
The `ymos state read` command SHALL read and output state machine content as structured JSON.

#### Scenario: Read holdings
- **WHEN** user runs `ymos state read holdings`
- **THEN** system reads data/state/holdings.md, parses the Markdown table, outputs JSON with all holdings rows

#### Scenario: Read watchlist
- **WHEN** user runs `ymos state read watchlist`
- **THEN** system reads data/state/watchlist.md, parses the Markdown table, outputs JSON with all watchlist rows

#### Scenario: Read preferences
- **WHEN** user runs `ymos state read preferences`
- **THEN** system reads data/state/preferences.md, outputs the full content

### Requirement: Update state machine
The `ymos state update` command SHALL update a specific field for a specific ticker in the state machine Markdown table.

#### Scenario: Update a single field
- **WHEN** user runs `ymos state update holdings --ticker BABA --field 当前价格 --value 120.5`
- **THEN** system finds the BABA row in holdings.md, updates the field, rewrites the file preserving table format, updates timestamp and changelog

#### Scenario: Ticker not found
- **WHEN** user runs `ymos state update holdings --ticker NONEXIST --field price --value 0`
- **THEN** system prints error "Ticker NONEXIST not found in holdings" and exits with code 1

### Requirement: State validation
The `ymos state validate` command SHALL check consistency between state machines and stock directories.

#### Scenario: Consistent state
- **WHEN** user runs `ymos state validate` and all state machine tickers have corresponding stock directories
- **THEN** system prints "Validation passed" and exits with code 0

#### Scenario: Missing stock directory
- **WHEN** a ticker exists in state machine but has no directory under data/stocks/
- **THEN** system prints warning listing missing directories and exits with code 1
