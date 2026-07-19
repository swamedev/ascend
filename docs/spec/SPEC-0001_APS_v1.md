# SPEC-0001 — ASCEND Package Specification (APS) v1.0

**Status:** Stable  
**Version:** 1.0.0  
**Obsoletes:** Draft versions prior to 2026  
**License:** MIT  

---

## 1. Abstract

APS defines the standard format for representing competency development packages.
A package is a self-contained, versioned, and validated unit of learning content
that the ASCEND Runtime can load, validate, and execute.

---

## 2. Scope

This specification covers:

- Directory structure of an APS package
- YAML grammar for each file
- Semantic meaning of every field
- Versioning and compatibility rules
- Validation rules

It does NOT cover:

- Execution semantics (see SPEC-0002 AEP)
- Registry interactions (see SPEC-0003 ARP)
- Agent interactions (see SPEC-0004 AAP)

---

## 3. Directory Structure

```
<package-id>/
    package.yaml            # REQUIRED — package metadata and spec
    competencies/
        competencies.yaml   # OPTIONAL — competency definitions
    achievements/
        achievements.yaml   # OPTIONAL — achievement definitions
    assessments/
        rubrics.yaml        # OPTIONAL — rubric definitions
    journeys/
        <journey-id>/
            journey.yaml    # REQUIRED — journey metadata and spec
            missions/
                <mission-id>/
                    mission.yaml  # REQUIRED — mission metadata and spec
    README.md               # OPTIONAL — human-readable description
```

---

## 4. YAML Grammar

### 4.1 package.yaml

```yaml
metadata:
  id: string                    # REQUIRED — unique package identifier (kebab-case)
  version: semver               # REQUIRED — semantic version (MAJOR.MINOR.PATCH)
  title: string                 # RECOMMENDED — human-readable name
  description: string           # RECOMMENDED — one-line summary
  author: string                # RECOMMENDED — author or organization name
  license: string               # RECOMMENDED — SPDX license identifier

spec:
  runtime: string               # REQUIRED — minimum runtime version (e.g., ">=1.0")
  language: string              # RECOMMENDED — BCP 47 language tag (e.g., "en", "pt-BR")
  estimated_hours: integer      # RECOMMENDED — total estimated time in hours
  dependencies: [string]        # OPTIONAL — list of package IDs this package depends on

capabilities: [string]          # OPTIONAL — runtime capabilities required (e.g., "evidence", "ai")
```

#### Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `metadata.id` | string | yes | Unique identifier, kebab-case, 1-64 chars |
| `metadata.version` | semver | yes | MAJOR.MINOR.PATCH per SemVer 2.0 |
| `metadata.title` | string | no | Human-readable title |
| `metadata.description` | string | no | Short description |
| `metadata.author` | string | no | Author name or organization |
| `metadata.license` | string | no | SPDX identifier (e.g., "MIT", "Apache-2.0") |
| `spec.runtime` | string | yes | Runtime version constraint |
| `spec.language` | string | no | BCP 47 language tag |
| `spec.estimated_hours` | integer | no | Total hours, >= 0 |
| `spec.dependencies` | [string] | no | Package IDs |
| `capabilities` | [string] | no | Required capabilities |

### 4.2 competencies.yaml

```yaml
spec:
  competencies:
    - id: string                # REQUIRED — unique identifier within package
      name: string              # RECOMMENDED — human-readable name
      description: string       # RECOMMENDED — what this competency represents
      level: string             # OPTIONAL — "beginner", "intermediate", "advanced"
      evidence_required: boolean  # OPTIONAL — default true
      mastery_threshold: integer  # OPTIONAL — percentage (0-100), default 80
```

### 4.3 achievements.yaml

```yaml
spec:
  achievements:
    - id: string                # REQUIRED — unique identifier within package
      name: string              # RECOMMENDED — human-readable name
      description: string       # RECOMMENDED — description
      criteria: [string]        # OPTIONAL — list of criteria strings
      badge: string             # OPTIONAL — badge identifier
```

### 4.4 rubrics.yaml

```yaml
spec:
  rubrics:
    - id: string                # REQUIRED — unique identifier within package
      title: string             # RECOMMENDED — human-readable title
      criteria:
        <criterion-id>:         # REQUIRED — at least one criterion
          weight: integer       # REQUIRED — weight percentage (all criteria sum to 100)
          description: string   # RECOMMENDED — description of this criterion
```

### 4.5 journey.yaml

```yaml
metadata:
  id: string                    # REQUIRED — unique identifier within package
  title: string                 # RECOMMENDED — human-readable title
  description: string           # RECOMMENDED — description

spec:
  difficulty: string            # OPTIONAL — "beginner", "intermediate", "advanced"
  estimated_hours: integer      # RECOMMENDED — estimated time in hours
  unlocks: [string]             # OPTIONAL — journey IDs unlocked after completion
```

### 4.6 mission.yaml

```yaml
metadata:
  id: string                    # REQUIRED — unique identifier within journey
  title: string                 # RECOMMENDED — human-readable title
  description: string           # RECOMMENDED — description

spec:
  difficulty: string            # OPTIONAL — "beginner", "intermediate", "advanced"
  estimated_minutes: integer    # RECOMMENDED — estimated time in minutes
  xp: integer                   # RECOMMENDED — XP awarded on completion (>= 0)
  prerequisites: [string]       # OPTIONAL — mission IDs that must be completed first
  competencies: [string]        # OPTIONAL — competency IDs mapped to this mission

  challenge:
    type: string                # RECOMMENDED — "practical", "quiz", "project", "essay"
    description: string         # REQUIRED — challenge description (supports markdown)

  evidence:
    required: boolean           # OPTIONAL — default true
    types: [string]             # OPTIONAL — "code", "document", "project", "report", "video"

  assessment:
    rubric: string              # OPTIONAL — rubric ID for assessment
```

---

## 5. Semantics

### 5.1 Identity

Package IDs MUST be globally unique. The RECOMMENDED format is reverse domain notation
(e.g., `org.ascend.cyber-foundations`) or simple kebab-case for community packages.

### 5.2 Versioning

Packages MUST follow SemVer 2.0:

- MAJOR: incompatible API/structural changes
- MINOR: backward-compatible additions
- PATCH: backward-compatible fixes

### 5.3 Dependencies

The `dependencies` field lists package IDs that MUST be present for this package
to function. The Runtime MAY resolve dependencies automatically; if it cannot,
execution SHOULD fail with a clear error.

### 5.4 Capabilities

The `capabilities` field declares what runtime features the package requires:

| Capability | Description |
|---|---|
| `evidence` | Evidence submission and assessment |
| `ai` | AI-assisted evaluation |
| `plugin` | External plugin execution |
| `async` | Asynchronous execution support |

---

## 6. Validation Rules

A valid package MUST satisfy:

1. `package.yaml` exists and is valid YAML
2. `metadata.id` is non-empty, kebab-case, 1-64 characters
3. `metadata.version` is a valid SemVer 2.0 string
4. `spec.runtime` is a valid version constraint
5. All referenced competency IDs exist in `competencies.yaml`
6. All referenced rubric IDs exist in `rubrics.yaml`
7. All mission prerequisites exist within the same journey
8. All journey unlocks reference existing journey IDs
9. Mission XP is non-negative
10. Rubric criteria weights sum to 100

---

## 7. Version Compatibility

| Runtime Version | APS Versions Supported |
|---|---|
| >= 1.0, < 2.0 | 1.x |
| >= 2.0 | 1.x, 2.x |

APS v1.x packages MUST work on any Runtime v1.x without modification.
Breaking changes to APS require a MAJOR version bump.

---

## 8. Grammar Summary (ABNF)

```abnf
package-id    = 1*64(ALPHA / DIGIT / "-")
semver        = major "." minor "." patch
major         = 1*DIGIT
minor         = 1*DIGIT
patch         = 1*DIGIT
```

---

## 9. Examples

See `packages/cyber-foundations/` for a complete reference implementation.
