# SPEC-0007 — Package Validation Rules

| Campo | Valor |
|-------|-------|
| **ID** | SPEC-0007 |
| **Nome** | Package Validation Rules |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Specification |
| **Owner** | Chief Architect |

## 1. Purpose

Define as regras de validação que todo pacote APS deve satisfazer
antes de ser aceito pelo Runtime.

## 2. Validation Levels

| Level | Descrição |
|-------|-----------|
| `error` | Bloqueante. Pacote não pode ser carregado. |
| `warning` | Não bloqueante. Exibe aviso ao usuário. |
| `info` | Informativo. Sugestão de melhoria. |

## 3. Structural Validation

### 3.1 File Existence

| Rule | Level | Description |
|------|-------|-------------|
| `package.yaml` exists | error | Arquivo raiz obrigatório |
| `journeys/` exists | error | Diretório de jornadas obrigatório |
| `competencies/competencies.yaml` exists | error | Definição de competências obrigatória |
| Referenced mission exists | error | Toda missão em `spec.missions` deve ter diretório |

### 3.2 YAML Schema

| Rule | Level | Description |
|------|-------|-------------|
| Valid YAML syntax | error | Arquivo deve ser YAML válido |
| `apiVersion` present | error | Todo arquivo deve declarar `apiVersion` |
| `kind` present | error | Todo arquivo deve declarar `kind` |
| `metadata.id` present | error | Todo arquivo deve ter ID |
| `metadata.id` format | error | IDs: lowercase, hífens, sem espaços |

## 4. Reference Validation

| Rule | Level | Description |
|------|-------|-------------|
| Journey ID exists | error | Jornada referenciada em `spec.journeys` deve existir |
| Mission ID exists | error | Missão referenciada deve existir |
| Competency ID exists | error | Competência referenciada deve existir |
| Rubric ID exists | warning | Rubrica referenciada deve existir |
| Achievement ID exists | warning | Achievement referenciado deve existir |
| No circular dependencies | error | Jornadas não podem depender circularmente |

## 5. Business Validation

| Rule | Level | Description |
|------|-------|-------------|
| Duplicate IDs | error | Nenhum ID pode se repetir no pacote |
| Prerequisites exist | error | Pré-requisitos devem referenciar missões existentes |
| XP non-negative | error | XP deve ser >= 0 |
| Mastery threshold valid | warning | `mastery_threshold` entre 0 e 100 |
| Rubric weights sum 100 | warning | Pesos da rubrica devem somar 100 |

## 6. Version Validation

| Rule | Level | Description |
|------|-------|-------------|
| Valid SemVer | error | `metadata.version` deve seguir `X.Y.Z` |
| Runtime constraint | error | `spec.runtime` deve ser compatível com o runtime atual |

## 7. Integrity Checks

- Nenhum arquivo órfão (não referenciado)
- Assets referenciados devem existir em `assets/`
- Badges de achievements devem existir em `assets/`

## 8. Validation Output

O validador deve retornar:

```json
{
  "valid": false,
  "errors": [
    {"rule": "mission-not-found", "path": "linux-999", "message": "Mission not found"}
  ],
  "warnings": [],
  "package": "cyber-foundations"
}
```

## Status

**SPEC-0007 — Package Validation Rules**

- Estado: ✅ Approved
- Próximo: Implementação do validador no Package Engine
