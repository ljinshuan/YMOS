## ADDED Requirements

### Requirement: YMOS-monitor skill SHALL provide盯盘 SOP
The system SHALL include `skills/ymos-monitor/` skill with SKILL.md defining capabilities, trigger phrases, and sop.md defining the standard monitoring operation flow.

#### Scenario: Agent discovers monitor skill
- **WHEN** agent reads skills directory
- **THEN** ymos-monitor skill is discoverable with trigger phrases: "开始盯盘", "停一下盯盘", "查看告警", "监控状态"

### Requirement: Monitor skill SHALL register routing entries
The system SHALL add routing entries to `skills/ymos-core/routing.md` for monitor-related trigger phrases, mapping to ymos-monitor skill.

#### Scenario: Trigger phrase routed to monitor skill
- **WHEN** user says "开始盯盘"
- **THEN** agent routes to ymos-monitor skill which provides cron setup guidance and configuration instructions

#### Scenario: View alerts routed to monitor skill
- **WHEN** user says "查看告警"
- **THEN** agent reads `data/monitor/alerts/YYYY-MM-DD.md` and presents recent alerts

### Requirement: Monitor skill SHALL reference CLI commands
The SKILL.md SHALL document the two CLI commands (`fetch-prices`, `check-signals`) with their parameters and usage examples, so agents can guide users on setup and execution.

#### Scenario: Agent provides cron setup guidance
- **WHEN** user asks to set up monitoring
- **THEN** agent reads SKILL.md and provides cron configuration examples using the correct CLI commands and parameters
