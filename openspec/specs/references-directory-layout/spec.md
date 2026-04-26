## Requirements

### Requirement: SOPs collected in references/sops/
All SOP documents SHALL be stored under references/sops/ with kebab-case English filenames.

#### Scenario: SOP file location
- **WHEN** a skill needs the market insight SOP
- **THEN** it reads references/sops/market-insight.md

### Requirement: P-series prompts in references/prompts/
All P-series analysis prompts SHALL be stored under references/prompts/.

#### Scenario: Prompt file location
- **WHEN** a skill needs the P13 market scanner prompt
- **THEN** it reads references/prompts/p13-market-scanner.md

### Requirement: Templates in references/templates/
All document templates SHALL be stored under references/templates/.

#### Scenario: Template file location
- **WHEN** a skill needs the knowledge base template
- **THEN** it reads references/templates/knowledge-base.md

### Requirement: Knowledge libraries in references/knowledge/
All reference knowledge libraries SHALL be stored under references/knowledge/ organized by domain.

#### Scenario: Diagnosis knowledge location
- **WHEN** the diagnosis skill needs its case library
- **THEN** it reads references/knowledge/diagnosis/diagnosis_case_library.md
