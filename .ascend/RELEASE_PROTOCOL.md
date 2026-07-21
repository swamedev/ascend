# RELEASE PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-006 |
| **Name** | Release Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-000, AEGS-002 |
| **Referenced by** | All AEGS documents |

---

## 1. Purpose

Define the release lifecycle, versioning strategy, and release process for the ASCEND project.

---

## 2. Release Lifecycle

```
Alpha → Beta → RC → Stable → LTS
```

Each stage has specific quality gates.

---

## 3. Release Stages

### 3.1 Alpha

| Attribute | Value |
|-----------|-------|
| **Purpose** | Internal testing and validation |
| **Audience** | Core team only |
| **Stability** | Unstable, APIs may change |
| **Version** | `v<major>.<minor>.<patch>-alpha.<N>` |
| **Duration** | As needed |

### 3.2 Beta

| Attribute | Value |
|-----------|-------|
| **Purpose** | External validation with early adopters |
| **Audience** | Early adopters, testers |
| **Stability** | Feature-complete, APIs stabilizing |
| **Version** | `v<major>.<minor>.<patch>-beta.<N>` |
| **Duration** | Minimum 2 weeks |

### 3.3 Release Candidate (RC)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Final validation before stable release |
| **Audience** | All users |
| **Stability** | Stable, only critical bug fixes |
| **Version** | `v<major>.<minor>.<patch>-rc.<N>` |
| **Duration** | Minimum 1 week |

### 3.4 Stable

| Attribute | Value |
|-----------|-------|
| **Purpose** | Production use |
| **Audience** | All users |
| **Stability** | Stable, backward compatible |
| **Version** | `v<major>.<minor>.<patch>` |
| **Duration** | Until next release |

### 3.5 Long-Term Support (LTS)

| Attribute | Value |
|-----------|-------|
| **Purpose** | Extended support for production users |
| **Audience** | Enterprise, production users |
| **Stability** | Maximum stability |
| **Version** | `v<major>.<minor>.x-lts` |
| **Support** | Minimum 12 months |

---

## 4. Version Bump Rules

| Change Type | Bump | Example |
|-------------|------|---------|
| Breaking API change | MAJOR | `v1.2.3` → `v2.0.0` |
| New feature (backward compatible) | MINOR | `v1.2.3` → `v1.3.0` |
| Bug fix (backward compatible) | PATCH | `v1.2.3` → `v1.2.4` |
| Critical hotfix | PATCH + hotfix tag | `v1.2.4-hotfix.1` |

---

## 5. Release Process

### 5.1 Preparing a Release

```
1. Create release branch: release/v<version>
2. Update version in pyproject.toml
3. Update CHANGELOG.md
4. Run full test suite
5. Run ascend doctor
6. Create Release Notes
7. Create Migration Guide (if breaking)
8. Tag the release: git tag v<version>
9. Push tag
10. Create GitHub Release
```

### 5.2 Hotfix Process

```
1. Branch from latest LTS or stable tag
2. Apply the fix
3. Run minimal test suite
4. Tag: v<version>-hotfix.<N>
5. Create GitHub Release
6. Merge fix back to main branch
```

---

## 6. Release Artifacts

Every release must include:

| Artifact | Description |
|----------|-------------|
| **Tag** | Git tag with SemVer |
| **GitHub Release** | Release on GitHub with notes |
| **Release Notes** | Summary of changes, new features, fixes |
| **Migration Guide** | Instructions for upgrading (if breaking) |
| **CHANGELOG update** | Full change log updated |

---

## 7. Release Notes Template

```markdown
# ASCEND v<version>

**Release Date:** YYYY-MM-DD

## Summary

Brief overview of the release.

## New Features

- Feature 1 (#issue)
- Feature 2 (#issue)

## Bug Fixes

- Fix 1 (#issue)
- Fix 2 (#issue)

## Breaking Changes

- Change 1 — Migration: ...
- Change 2 — Migration: ...

## Documentation

- Doc 1
- Doc 2

## Acknowledgments

Thanks to contributors.
```

---

## 8. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
