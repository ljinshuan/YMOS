## ADDED Requirements

### Requirement: Shared Futu OpenD connection check
The system SHALL provide `check_opend_connection(host, port)` in `cli/core/futu_utils.py` that tests TCP reachability of Futu OpenD with a 3-second timeout. Returns True if reachable, False otherwise.

#### Scenario: OpenD is running
- **WHEN** Futu OpenD is listening on the configured host:port
- **THEN** returns True

#### Scenario: OpenD is not running
- **WHEN** no process is listening on the configured host:port
- **THEN** returns False within 3 seconds

### Requirement: Shared ticker-to-Futu-symbol conversion
The system SHALL provide `ticker_to_futu_symbol(ticker)` in `cli/core/futu_utils.py` that converts YMOS ticker format to Futu standard symbol format (e.g., `0700.HK` → `HK.00700`, `AAPL` → `US.AAPL`, `688008.SS` → `SH.688008`).

#### Scenario: All ticker format conversions
- **WHEN** input tickers include `0700.HK`, `AAPL`, `688008.SS`, `000001.SZ`
- **THEN** returns `HK.00700`, `US.AAPL`, `SH.688008`, `SZ.000001` respectively

### Requirement: OpenD startup guide constant
The system SHALL provide `OPEND_STARTUP_GUIDE` as a module-level constant string in `cli/core/futu_utils.py`, containing the Chinese-language guide for starting Futu OpenD.

#### Scenario: Guide content available
- **WHEN** importing `OPEND_STARTUP_GUIDE` from `cli.core.futu_utils`
- **THEN** returns a non-empty string containing setup instructions in Chinese

### Requirement: DRY refactor of existing commands
The system SHALL replace inline `_check_opend_connection()` and `_ticker_to_futu_symbol()` functions in `cli/commands/capital_flow.py` and `cli/commands/screener.py` with imports from `cli/core/futu_utils.py`.

#### Scenario: No duplicate functions
- **WHEN** searching for function definitions of `check_opend_connection` and `ticker_to_futu_symbol` across `cli/`
- **THEN** only `cli/core/futu_utils.py` defines these functions; command files import them
