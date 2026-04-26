# skill-ymos-onboarding Specification

## Purpose
TBD - created by archiving change skills-conversion. Update Purpose after archive.
## Requirements
### Requirement: Onboarding skill triggers
The ymos-onboarding skill SHALL trigger on `开始使用`, `初始化系统`, and `补全信息`.

#### Scenario: First-time user
- **WHEN** user says "开始使用" and all state files are empty
- **THEN** skill executes full onboarding: preference interview → holdings → watchlist

#### Scenario: Partial data exists
- **WHEN** user says "补全信息" and preferences exist but holdings are empty
- **THEN** skill only executes the missing holdings step

### Requirement: Onboarding references SOP
The skill SHALL reference `references/sops/onboarding.md` for detailed execution steps.

#### Scenario: Agent reads SOP
- **WHEN** skill is triggered
- **THEN** agent reads references/sops/onboarding.md and follows its steps

### Requirement: Onboarding uses CLI for data operations
The skill SHALL use `ymos init` and `ymos state` commands for directory creation and state writes.

#### Scenario: Create stock during onboarding
- **WHEN** user provides a holding ticker during onboarding
- **THEN** skill calls `ymos init stock --ticker TICKER --name NAME --location holdings`

