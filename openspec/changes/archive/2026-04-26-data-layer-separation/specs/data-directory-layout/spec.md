## ADDED Requirements

### Requirement: Data directory structure
All runtime data SHALL reside under `data/` with a fixed subdirectory layout.

#### Scenario: Standard layout exists
- **WHEN** system is initialized
- **THEN** data/ contains subdirectories: state/, stocks/holdings/, stocks/watchlist/, reports/market-insight/, reports/radar/, reports/strategy/, dashboard/

### Requirement: State files location
State machine files SHALL use English filenames under data/state/.

#### Scenario: State file naming
- **WHEN** system reads or writes state
- **THEN** holdings state is at data/state/holdings.md, watchlist at data/state/watchlist.md, preferences at data/state/preferences.md

### Requirement: Stock directories organized by status
Individual stock folders SHALL be under data/stocks/holdings/ or data/stocks/watchlist/ based on their current status.

#### Scenario: Holdings stock location
- **WHEN** a stock is in holdings
- **THEN** its directory is at data/stocks/holdings/NAME_TICKER/

#### Scenario: Watchlist stock location
- **WHEN** a stock is in watchlist
- **THEN** its directory is at data/stocks/watchlist/NAME_TICKER/

### Requirement: Reports organized by type and date
Report output SHALL be under data/reports/{type}/YYYY-MM/ with raw data in data/reports/{type}/raw/YYYY-MM/.

#### Scenario: Market insight report path
- **WHEN** a market insight report is generated for 2026-04-26
- **THEN** it is saved to data/reports/market-insight/2026-04/2026-04-26_市场洞察.md

#### Scenario: Raw data path
- **WHEN** price scan data is generated for 2026-04-26
- **THEN** raw JSON is saved to data/reports/radar/raw/2026-04/price_scan_20260426.json
