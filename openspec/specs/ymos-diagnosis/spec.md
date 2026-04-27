# ymos-diagnosis Specification

## Purpose
TBD - created by archiving change skills-conversion. Update Purpose after archive.
## Requirements
### Requirement: Diagnosis skill location
The ymos-diagnosis skill SHALL reside at skills/ymos-diagnosis/SKILL.md instead of Brain/ymos-diagnosis/SKILL.md.

#### Scenario: Skill discovery
- **WHEN** agent looks for the diagnosis skill
- **THEN** it reads skills/ymos-diagnosis/SKILL.md (not the old path)

### Requirement: Diagnosis knowledge references
The ymos-diagnosis skill SHALL reference knowledge files at references/knowledge/diagnosis/ instead of Brain/ymos-diagnosis/knowledge/.

#### Scenario: Read case library
- **WHEN** diagnosis skill reads its case library
- **THEN** it reads references/knowledge/diagnosis/diagnosis_case_library.md

### Requirement: Diagnosis skill uses CLI for state reads
The diagnosis skill SHALL use `ymos state read` to load user portfolio context when available.

#### Scenario: Contextual diagnosis
- **WHEN** diagnosis skill starts and data/state/preferences.md exists
- **THEN** skill reads user preferences via `ymos state read preferences` for richer context

