# cli-init-ops Specification

## Purpose
TBD - created by archiving change cli-infrastructure. Update Purpose after archive.
## Requirements
### Requirement: Initialize stock directory
The `ymos init stock` command SHALL create a stock directory with initialized documents at the specified location.

#### Scenario: Create watchlist stock
- **WHEN** user runs `ymos init stock --ticker ALAB --name "Astera Labs" --location watchlist`
- **THEN** system creates data/stocks/watchlist/Astera Labs_ALAB/ with knowledge-base.md from template

#### Scenario: Create holdings stock
- **WHEN** user runs `ymos init stock --ticker BABA --name "阿里巴巴" --location holdings`
- **THEN** system creates data/stocks/holdings/阿里巴巴_BABA/ with knowledge-base.md and memo.md from templates

### Requirement: Initialize directory structure
The `ymos init dirs` command SHALL create all required data directories.

#### Scenario: Fresh init
- **WHEN** user runs `ymos init dirs` on a fresh system
- **THEN** system creates data/state/, data/stocks/holdings/, data/stocks/watchlist/, data/reports/market-insight/raw/, data/reports/radar/raw/, data/reports/strategy/raw/, data/dashboard/

### Requirement: Initialize template file
The `ymos init template` command SHALL create a single document from template for a specific stock.

#### Scenario: Create knowledge base
- **WHEN** user runs `ymos init template --type knowledge-base --ticker BABA --name "阿里巴巴"`
- **THEN** system creates a minimal knowledge-base.md skeleton in the stock directory

#### Scenario: Create memo
- **WHEN** user runs `ymos init template --type memo --ticker BABA --name "阿里巴巴"`
- **THEN** system creates a minimal memo.md skeleton in the stock directory

