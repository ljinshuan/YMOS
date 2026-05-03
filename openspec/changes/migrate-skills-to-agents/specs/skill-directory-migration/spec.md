## ADDED Requirements

### Requirement: Skills reside in .agents/skills/ directory
All YMOS skill directories SHALL be located under `.agents/skills/` instead of `skills/`. Each skill SHALL maintain its internal structure (SKILL.md, sop/, prompts/, knowledge/, templates/) unchanged.

#### Scenario: Skill directory exists at new location
- **WHEN** migration is complete
- **THEN** all 11 skill directories SHALL exist under `.agents/skills/` (ymos-core, ymos-onboarding, ymos-market-insight, ymos-radar, ymos-research, ymos-strategy, ymos-target-mgmt, ymos-reconcile, ymos-diagnosis, ymos-screener, ymos-sentiment)

#### Scenario: Old skills/ directory removed
- **WHEN** migration is complete
- **THEN** the `skills/` directory at project root SHALL NOT exist

### Requirement: Documentation references updated
All project documentation files SHALL reference `.agents/skills/` instead of `skills/` for skill paths.

#### Scenario: CLAUDE.md paths updated
- **WHEN** migration is complete
- **THEN** CLAUDE.md SHALL contain zero references to `skills/` as a project root path (all replaced with `.agents/skills/`)

#### Scenario: AGENT_GUIDE.md paths updated
- **WHEN** migration is complete
- **THEN** AGENT_GUIDE.md SHALL contain zero references to `skills/` as a project root path

#### Scenario: No stale references remain
- **WHEN** a grep for `skills/` is performed across the project (excluding `.git/`, `node_modules/`, `data/`)
- **THEN** all remaining matches SHALL be in contexts unrelated to YMOS skill paths (e.g., comments about generic skills, third-party docs)

### Requirement: Git history preserved
File moves SHALL use `git mv` so that git history remains traceable for each skill file.

#### Scenario: File history traceable
- **WHEN** `git log --follow .agents/skills/ymos-core/SKILL.md` is executed
- **THEN** the output SHALL show commit history from before the migration

### Requirement: No content changes
No file content within any skill directory SHALL be modified during migration. Only the directory location changes.

#### Scenario: File content integrity
- **WHEN** migration is complete
- **THEN** `git diff --stat` for the migration commit SHALL show only renames (no content modifications)
