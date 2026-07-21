# SPEC-0008 — ASCEND Registry Protocol

| Campo | Valor |
|-------|-------|
| **ID** | SPEC-0008 |
| **Nome** | Registry Protocol |
| **Versão** | 1.0 |
| **Status** | Draft |
| **Categoria** | Specification |
| **Owner** | Chief Architect |

## 1. Purpose

Define o protocolo de comunicação entre o ASCEND Runtime e um
Package Registry, permitindo busca, instalação e publicação de pacotes.

## 2. Registry Operations

### 2.1 Search

```
GET /v1/packages?q=<query>
```

Response:

```json
{
  "results": [
    {
      "id": "cyber-foundations",
      "version": "1.0.0",
      "title": "Cyber Foundations",
      "description": "...",
      "author": "ASCEND Institute",
      "downloads": 1500
    }
  ]
}
```

### 2.2 Package Info

```
GET /v1/packages/<id>
```

Response:

```json
{
  "id": "cyber-foundations",
  "versions": ["1.0.0", "0.9.0"],
  "latest": "1.0.0",
  "author": "ASCEND Institute",
  "license": "MIT"
}
```

### 2.3 Download

```
GET /v1/packages/<id>/<version>/download
```

Response: `.tar.gz` ou `.zip` contendo o pacote.

### 2.4 Publish

```
POST /v1/packages
Authorization: Bearer <token>
Body: multipart/form-data (package.tar.gz)
```

Response:

```json
{
  "status": "published",
  "id": "cyber-foundations",
  "version": "1.0.0"
}
```

## 3. Local Package Cache

```
~/.ascend/packages/
└── <id>/
    └── <version>/
        ├── package.yaml
        └── ...
```

## 4. CLI Commands (Future)

```bash
ascend search linux
ascend info cyber-foundations
ascend install cyber-foundations
ascend install cyber-foundations@1.0.0
ascend uninstall cyber-foundations
ascend list                # installed packages
ascend outdated            # check for updates
ascend update              # update all packages
```

## 5. Dependency Resolution

Pacotes podem depender de outros pacotes:

```yaml
# package.yaml
spec:
  dependencies:
    - python-basics >= 1.0
    - git-foundations
```

O Registry resolve a árvore de dependências antes de instalar.

## Status

**SPEC-0008 — Registry Protocol**

- Estado: 🟡 Draft
- Próximo: Implementação após Package Engine e CLI
