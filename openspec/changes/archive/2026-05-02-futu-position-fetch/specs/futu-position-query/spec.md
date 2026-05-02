## ADDED Requirements

### Requirement: Futu OpenD position query
The system SHALL provide `cli/core/sources/futu_position.py` with a `fetch_positions(host, port)` function that queries Futu OpenD `get_holdings` and returns a list of standardized position dicts.

#### Scenario: Successfully fetch positions
- **WHEN** calling `fetch_positions()` with Futu OpenD running and logged in, account has 3 holdings
- **THEN** returns a list of 3 position dicts with keys: ticker, name, quantity, cost_price, current_price, market_value, profit_loss, profit_loss_pct, currency

#### Scenario: OpenD not running
- **WHEN** calling `fetch_positions()` with Futu OpenD not reachable
- **THEN** returns None and prints connection error

#### Scenario: OpenD not logged in
- **WHEN** calling `fetch_positions()` with Futu OpenD running but not logged in
- **THEN** returns None and prints login-required error

#### Scenario: Empty positions
- **WHEN** calling `fetch_positions()` with a logged-in account that has no holdings
- **THEN** returns an empty list

### Requirement: Futu symbol to YMOS ticker conversion
The system SHALL provide `futu_symbol_to_ticker(symbol)` in `cli/core/futu_utils.py` that converts Futu format back to YMOS format: `HK.00700` → `0700.HK`, `US.AAPL` → `AAPL`, `SH.688008` → `688008.SS`, `SZ.000001` → `000001.SZ`.

#### Scenario: HK symbol conversion
- **WHEN** input is `HK.00700`
- **THEN** returns `0700.HK`

#### Scenario: US symbol conversion
- **WHEN** input is `US.AAPL`
- **THEN** returns `AAPL`

#### Scenario: SH symbol conversion
- **WHEN** input is `SH.688008`
- **THEN** returns `688008.SS`

#### Scenario: SZ symbol conversion
- **WHEN** input is `SZ.000001`
- **THEN** returns `000001.SZ`

### Requirement: CLI command ymos position fetch
The system SHALL register a `position` subcommand with a `fetch` action that queries the user's Futu account positions and saves results to files.

#### Scenario: Successful fetch with both formats
- **WHEN** running `ymos position fetch` with OpenD connected and holdings present
- **THEN** saves a JSON file and a Markdown file to `data/position/`, prints summary to stdout

#### Scenario: Successful fetch with JSON only
- **WHEN** running `ymos position fetch --format json`
- **THEN** saves only a JSON file to `data/position/`

#### Scenario: Successful fetch with custom output dir
- **WHEN** running `ymos position fetch --output-dir /tmp/ymos-test`
- **THEN** saves output files to the specified directory

#### Scenario: OpenD not available
- **WHEN** running `ymos position fetch` with OpenD not reachable
- **THEN** prints connection error guide and exits with code 1

### Requirement: Position JSON output format
The JSON output file SHALL contain a top-level object with: `meta` (source, fetched_at, position_count) and `positions` (array of position dicts).

#### Scenario: JSON structure
- **WHEN** positions are fetched successfully
- **THEN** JSON file contains `{"meta": {"source": "futu_opend", "fetched_at": "...", "position_count": N}, "positions": [...]}`

### Requirement: Position Markdown output format
The Markdown output SHALL display positions in a table with columns: 代码, 名称, 数量, 成本价, 当前价, 市值, 盈亏, 盈亏%, with a summary row showing total market value and total P&L.

#### Scenario: Markdown table rendering
- **WHEN** positions are fetched successfully with 2 holdings
- **THEN** Markdown file contains a table header row, 2 data rows, and a summary row with totals
