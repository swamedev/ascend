# SPEC-0003 — ASCEND Registry Protocol (ARP) v1.0

**Status:** Draft  
**Version:** 0.1.0  
**License:** MIT  

---

## 1. Abstract

ARP defines how ASCEND packages are published, discovered, installed, and verified
through a Registry. The Registry is an optional component; packages can be used
directly from disk without any Registry interaction.

---

## 2. Scope

This specification covers:

- Registry API endpoints
- Publish flow
- Install/resolve flow
- Package signature verification
- Dependency resolution
- Search protocol

It does NOT cover:

- Package format (see SPEC-0001 APS)
- Execution semantics (see SPEC-0002 AEP)
- Agent interactions (see SPEC-0004 AAP)

---

## 3. Registry API

### 3.1 Base URL

All Registry endpoints are relative to a configurable base URL:
```
https://registry.ascend.dev/api/v1
```

### 3.2 Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/packages` | List/search packages |
| GET | `/packages/{id}` | Get package metadata |
| GET | `/packages/{id}/versions` | List versions |
| GET | `/packages/{id}/versions/{version}` | Get specific version |
| GET | `/packages/{id}/versions/{version}/download` | Download package archive |
| PUT | `/packages/{id}/versions/{version}` | Publish a version |
| GET | `/search?q={query}` | Search packages |

### 3.3 Package Metadata Response

```json
{
  "id": "cyber-foundations",
  "title": "Cyber Foundations",
  "description": "Competências fundamentais para desenvolvimento web",
  "author": "ASCEND Institute",
  "license": "MIT",
  "versions": {
    "1.0.0": {
      "published": "2026-07-19T00:00:00Z",
      "runtime": ">=1.0",
      "checksum": "sha256-abc123...",
      "signature": "pgp-signature-base64..."
    }
  },
  "downloads": 0,
  "verified": true
}
```

---

## 4. Publish Flow

```
Package Author
    │
    1. Create package (per SPEC-0001)
    │
    2. Sign package with PGP key
    │
    3. Upload to Registry:
       PUT /packages/{id}/versions/{version}
       Content-Type: application/gzip
       Body: signed package archive
    │
    4. Registry validates:
       - Package structure
       - Signature
       - Version not duplicate
    │
    5. Registry returns 201 Created
```

### 4.1 Authentication

Publishing REQUIRES authentication. The Registry MAY use:

- API tokens
- OAuth 2.0
- PGP key authentication

---

## 5. Install Flow

```
Client
    │
    1. Request: ascend registry install cyber-foundations
    │
    2. Resolve: GET /packages/cyber-foundations/versions/latest
    │
    3. Download: GET /packages/cyber-foundations/versions/1.0.0/download
    │
    4. Verify:
       - Check checksum
       - Verify PGP signature
    │
    5. Extract to packages/cyber-foundations/
    │
    6. Resolve dependencies recursively
```

---

## 6. Dependency Resolution

Packages MAY declare dependencies in `package.yaml`:

```yaml
spec:
  dependencies:
    - linux-foundations
    - git-foundations
```

The resolver MUST:

1. Fetch all dependencies from the Registry (or cache)
2. Check for version conflicts
3. Install in topological order
4. Reject circular dependencies

---

## 7. Signature Verification

All published packages SHOULD be signed.

### 7.1 Signing

```bash
gpg --detach-sign --armor cyber-foundations.tar.gz
```

### 7.2 Verification

```bash
gpg --verify cyber-foundations.tar.gz.asc cyber-foundations.tar.gz
```

The Registry MUST reject unsigned packages unless explicitly configured otherwise.

---

## 8. Search Protocol

```bash
GET /search?q=linux&language=en&level=beginner
```

Response:

```json
{
  "results": [
    {
      "id": "linux-foundations",
      "title": "Linux Foundations",
      "description": "...",
      "author": "ASCEND Institute",
      "version": "1.0.0",
      "downloads": 1200,
      "verified": true
    }
  ],
  "total": 1
}
```

---

## 9. Local Cache

Clients SHOULD cache downloaded packages at:

- Linux/macOS: `~/.ascend/cache/packages/`
- Windows: `%APPDATA%\ascend\cache\packages\`

Cache entries expire after 24 hours or on explicit `ascend registry update`.
