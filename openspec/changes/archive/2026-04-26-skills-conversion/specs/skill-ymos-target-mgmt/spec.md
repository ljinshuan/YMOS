## ADDED Requirements

### Requirement: Target management skill triggers
The ymos-target-mgmt skill SHALL trigger on `关注 [ticker]`, `建仓 [ticker]`, `移除关注 [ticker]`, and `清仓 [ticker]`.

#### Scenario: Watch a new ticker
- **WHEN** user says "关注 NVDA"
- **THEN** skill runs `ymos init stock --ticker NVDA --name NVIDIA --location watchlist`, updates watchlist state, offers to trigger ymos-research

#### Scenario: Move to holdings
- **WHEN** user says "建仓 NVDA"
- **THEN** skill checks P1+P4+P2 exist, moves directory from watchlist to holdings, initializes memo, updates both state machines

### Requirement: Target management triggers research
The skill SHALL offer to trigger ymos-research when adding a new ticker to watchlist.

#### Scenario: Offer research after watching
- **WHEN** a new ticker is added to watchlist
- **THEN** skill asks user "是否现在跑初始调研？" and if yes, executes ymos-research flow

### Requirement: Archive on removal
The skill SHALL move stock directories to data/stocks/watchlist/_archive/ when removing from watchlist.

#### Scenario: Remove watchlist ticker
- **WHEN** user says "移除关注 NVDA"
- **THEN** skill moves data/stocks/watchlist/NVIDIA_NVDA/ to data/stocks/watchlist/_archive/NVIDIA_NVDA/
