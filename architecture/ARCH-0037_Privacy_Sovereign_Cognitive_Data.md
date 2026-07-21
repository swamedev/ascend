# ARCH-0037 — Privacy Sovereign Cognitive Data

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0037 |
| **Nome** | Privacy Sovereign Cognitive Data |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0001 System Architecture Overview, ARCH-0003 Core Engine Specification, ARCH-0030 Cognitive Architecture, ARCH-0031 Observation Model, DOC-0006 Lexicon |
| **Invariants** | I14 — Cognitive Independence, I08 — No Competency Without Evidence, I12 — Local First |

---

## 1. Purpose

The Cognitive Layer observes everything. Every click, every pause, every pattern. This data is intimate. It reveals how a person learns, struggles, and grows. This document defines who owns this data, who can access it, and under what conditions.

The Observation Model (ARCH-0031) defines *what* is captured. The Cognitive Architecture (ARCH-0030) defines *how* it is processed. This document defines *who controls it* at every point in the pipeline — from raw event emission through insight generation to export and deletion.

This is not a compliance document. It is an architectural contract. Every component in the ASCEND system — the Runtime, the Cognitive Layer, the Experience Layer, every SDK, every CLI command, every database schema — is bound by the rules herein. Any component that violates these rules is not part of ASCEND.

The Cognitive Layer is the most intimate system in the ASCEND architecture. It watches the Builder learn. It detects when they struggle, when they stagnate, when they accelerate. It builds a digital model of human cognition in the context of competency development. That model belongs to exactly one entity: the Builder. Not to the project. Not to a corporation. Not to an AI vendor. Not to the Developer. The Builder and only the Builder.

---

## 2. First Principle

> **The Builder is the absolute owner of all cognitive data.**

This is not a legal compliance statement. It is an architectural invariant. The system is designed so that the Builder's ownership is not a configuration option — it is physically enforced by the architecture.

What this means in concrete terms:

- **No data leaves the device without the Builder's explicit, granular, revocable consent.** "By using this software you agree" is not consent. Consent is an active choice made for each specific data category, each specific recipient, each specific duration.

- **No external service has access to raw cognitive data unless the Builder explicitly grants it.** The Runtime does not phone home. The Cognitive Layer does not sync to a cloud. The CLI does not send telemetry. The system is fully operational in a permanently air-gapped state.

- **No AI model can be trained on Builder data without the Builder's explicit opt-in.** And even then, the data must be anonymized before it reaches the model. The Builder's identity is never exposed to any training pipeline.

- **The Builder can delete any or all data at any time, and deletion is final.** There is no "we keep anonymized aggregates." There is no "we need this for research." Deletion means irrecoverable destruction. The architecture must make this possible without compromising system integrity.

- **The Builder can export all data in open, documented formats at any time.** There is no vendor lock-in at the data layer. The data format is not proprietary. The schema is public. The export tool is a first-class CLI command.

This principle flows directly from the First Principles (DOC-0003) and the Engineering Philosophy (DOC-0007). A competency development framework that does not give the learner absolute control over their own learning data is not a tool for empowerment — it is a surveillance system. ASCEND is designed to empower, not surveil.

---

## 3. Data Classification

Cognitive data is not monolithic. Different categories carry different sensitivity levels and require different handling rules. The classification below defines the sensitivity tiers used throughout this document.

| Category | Examples | Sensitivity | Rationale |
|----------|----------|-------------|-----------|
| **Runtime Data** | XP, level, competencies, achievements | Low — game-like progression | These are public-facing progression metrics. They reveal what the Builder has accomplished, not how. |
| **Behavioral Data** | Focus time, session duration, navigation paths | Medium — reveals habits | These reveal work patterns. Alone, they are low risk. Aggregated, they reveal when and how a person works. |
| **Learning Patterns** | Struggles, knowledge gaps, learning velocity | High — reveals cognitive profile | These reveal *how* a person thinks. They expose strengths and weaknesses. In the wrong hands, they could be used to manipulate or discriminate. |
| **Reflection Data** | Self-assessments, goals, reflection notes | Very High — personal thoughts | These are the Builder's private thoughts about their own growth. They may contain hopes, fears, insecurities. They deserve the highest protection. |
| **Evidence Content** | Mission evidence text | Very High — user-generated content | These are the Builder's own work products. Code snippets, essays, project artifacts. They constitute intellectual property and personal expression. |
| **Inferred Data** | Insights, recommendations, predictions | High — AI-generated profile | These are the system's interpretations of the Builder's data. They may be wrong. They may be biased. They are still personal data and belong to the Builder. |

The sensitivity tier determines default handling:

- **Low:** Can be stored locally with standard encryption. Can be included in anonymized exports by default.
- **Medium:** Stored locally. Requires explicit opt-in for any export that includes behavioral data.
- **High:** Stored locally with maximum encryption. Excluded from anonymized exports by default. Requires granular opt-in for any sharing.
- **Very High:** Stored locally with cryptographic safeguards. Never included in anonymized exports. Requires explicit per-category consent for any access beyond the Builder.

---

## 4. Data Ownership Rules

The following rules are architectural invariants. They are not guidelines, not recommendations, not best practices. They are hard constraints. Any component that cannot satisfy these rules cannot exist in the ASCEND system.

### R1 — Absolute Ownership

The Builder owns 100% of all cognitive data. No entity — not the ASCEND project, not a cloud provider, not an AI model, not a third-party service, not a Contributor, not the Chief Architect — holds any ownership stake. Ownership is not shared, not joint, not licensed, not transferred. It is absolute.

This means:
- The Builder has the right to access their data at any time without restriction.
- The Builder has the right to modify their data (annotations, corrections, deletions).
- The Builder has the right to export their data in open formats.
- The Builder has the right to delete their data permanently.
- The Builder has the right to deny access to any party, including the system itself.
- The Builder has the right to know exactly what data has been collected and how it is used.

No DRM. No hidden telemetry. No backdoors. No "we need this to improve the service."

### R2 — Local Default

All data is stored locally by default. Zero data leaves the device without explicit Builder action.

- The Runtime writes observations to a local SQLite database.
- The Cognitive Layer reads from the local database and writes insights back to it.
- The CLI operates exclusively on the local database.
- The Experience Layer communicates with the Runtime and Cognitive Layer through local IPC channels.
- There is no cloud sync. There is no remote database. There is no "optional cloud backup" that is enabled by default.
- Synchronization, if any, is a separate feature that requires explicit opt-in and is governed by the Sharing Protocol (Section 9).

The default configuration is fully offline. The Builder must take an affirmative action to enable any network access. This is not a checkbox in a settings menu — it is the absence of any network code in the default build.

### R3 — Explicit Consent

Any data sharing requires explicit, granular, revocable consent.

- **Explicit:** Consent must be given through an affirmative action. Pre-checked boxes, implied consent, "by using this service" agreements, and blanket terms-of-service are not consent.
- **Granular:** The Builder consents to specific data categories, specific recipients, specific purposes, and specific durations. "Share everything with everyone forever" is not a valid consent option.
- **Revocable:** The Builder can withdraw consent at any time. Withdrawal takes effect immediately. Data shared before withdrawal may remain with the recipient, but the Builder must be informed of this limitation.
- **Logged:** Every consent action is recorded in the audit log. The Builder can review their consent history at any time.

### R4 — Portability

The Builder can export all data in open formats at any time.

- **JSON Lines:** One event per line, suitable for programmatic processing.
- **CSV:** Flat files suitable for spreadsheet analysis.
- **SQLite dump:** Full database export for complete archival.
- **Markdown report:** Human-readable summary of all data.
- All export formats are documented in Section 6.
- Export is available via the CLI (`ascend export`) and programmatically via the SDK.
- Export includes all data categories. The Builder chooses which categories to include.
- Export does not require network access. It is a purely local operation.

### R5 — Cryptographic Deletion

The Builder can delete all data at any time. Deletion is cryptographic — data is irrecoverable after confirmation.

- Soft delete marks data as deleted and retains it for 30 days (recovery window).
- Hard delete overwrites data with zeros, removes indexes, and runs VACUUM.
- Cryptographic delete overwrites data with random data three times before deletion.
- After deletion, the system verifies that data is irrecoverable and reports the result.
- Deletion is available per-category, per-time-range, or globally.

### R6 — No Lock-In

Data format is open and documented. No proprietary encoding.

- The observation schema is defined in ARCH-0031 and published as part of the project documentation.
- The insight schema is defined in ARCH-0030 and published.
- The database schema is defined in ARCH-0005 and published.
- All schemas are versioned. Backward compatibility is maintained across minor versions.
- Migration paths are documented for major version changes.
- No data is stored in proprietary binary formats. No encryption is used for storage by default (encryption is opt-in).

---

## 5. Access Control Matrix

The following matrix defines who can do what with cognitive data. This matrix is enforced at the architecture level — not just at the UI level. The Runtime, Cognitive Layer, and Experience Layer all enforce these rules independently.

| Actor | Can Read | Can Write | Can Delete |
|-------|----------|-----------|------------|
| **Builder** | ✅ All data | ✅ Own observations, annotations | ✅ All data |
| **Runtime** | ❌ None | ✅ Writes domain events (via event bus) | ❌ None |
| **Cognitive Layer** | ✅ Observations, metrics, insights | ✅ Insights, recommendations (own output) | ❌ None |
| **Experience Layer** | ✅ Insights, recommendations | ✅ Observation events (via SDK) | ❌ None |
| **AI Model (if installed)** | ✅ Anonymized observations (opt-in) | ❌ None | ❌ None |
| **Third Party** | ❌ None | ❌ None | ❌ None |
| **Developer** | ❌ None | ❌ None | ❌ None |

### Detailed Rules

**Runtime:** The Runtime writes domain events and state snapshots to the observation store. It can observe what it has written (for error recovery), but it cannot read observations from the Cognitive Layer. The Runtime does not have access to insights, recommendations, or inferred data.

**Cognitive Layer:** The Cognitive Layer reads observations and metrics from the observation store. It writes insights and recommendations back to the store. It cannot delete anything. It cannot modify observations. It cannot read Builder annotations.

**Experience Layer:** The Experience Layer reads insights and recommendations for display to the Builder. It reads observations only for real-time display (session progress). It writes observation events through the SDK. It cannot delete anything.

**AI Model:** If the Builder has installed a local AI model and opted into AI processing, the model receives anonymized observations. Anonymization happens before the model receives the data. The model does not have access to raw observations, reflection data, or evidence content. The model does not write to the store. The model does not have access to the Builder's identity.

**Third Party:** Third parties have no access to cognitive data by default. If the Builder explicitly shares data via the Sharing Protocol (Section 9), the third party receives only the specific data the Builder chose to share, for the specific duration the Builder chose, with no right to sublicense or redistribute.

**Developer:** The Developer (any person writing code for ASCEND, including Contributors, maintainers, and the Chief Architect) has no access to any Builder's cognitive data. There is no backdoor. There is no admin panel. There is no debugging mode that allows reading another Builder's database. The Developer's own Builder data — if they use ASCEND for their own development — is subject to the same rules as any other Builder's.

---

## 6. Export Format

The canonical export format ensures that the Builder can always take their data elsewhere. The format is simple, open, and documented.

### 6.1 Directory Structure

```
export/
├── metadata.json           # Export manifest
├── builder-profile.json    # Builder identity (non-identifying)
├── observations.jsonl      # All observation events
├── metrics.jsonl           # Metric snapshots
├── insights.jsonl          # Insights and recommendations
├── sessions.jsonl          # Session summaries
└── evidence/               # Evidence content (optional)
    ├── mission-001.json
    ├── mission-002.json
    └── ...
```

### 6.2 metadata.json

```json
{
  "exportVersion": "1.0",
  "exportedAt": "2026-07-21T14:30:00Z",
  "builderId": "nonce-abc123def456",
  "dataCategories": ["observations", "metrics", "insights", "sessions"],
  "dateRange": {
    "from": "2026-01-01T00:00:00Z",
    "to": "2026-07-21T14:30:00Z"
  },
  "recordCounts": {
    "observations": 15420,
    "metrics": 3741,
    "insights": 892,
    "sessions": 187
  },
  "schemaVersions": {
    "observations": "1.0",
    "metrics": "1.0",
    "insights": "1.0",
    "sessions": "1.0"
  }
}
```

### 6.3 observations.jsonl

Each line is a JSON object representing one observation event. The schema follows ARCH-0031.

```json
{"type":"observation","id":"obs-001","timestamp":"2026-07-21T10:15:00Z","category":"mission","action":"complete","payload":{"missionId":"variables-101","score":85,"duration":240}}
{"type":"observation","id":"obs-002","timestamp":"2026-07-21T10:20:00Z","category":"session","action":"pause","payload":{"reason":"interrupted","duration":0}}
```

### 6.4 metrics.jsonl

Each line is a metric snapshot — an aggregate value at a point in time.

```json
{"type":"metric","id":"met-001","timestamp":"2026-07-21T10:15:00Z","name":"focus_time","value":240,"unit":"seconds","source":"observation"}
{"type":"metric","id":"met-002","timestamp":"2026-07-21T10:15:00Z","name":"session_streak","value":5,"unit":"days","source":"derived"}
```

### 6.5 insights.jsonl

Each line is an insight or recommendation generated by the Cognitive Layer.

```json
{"type":"insight","id":"ins-001","timestamp":"2026-07-21T10:15:00Z","confidence":0.85,"category":"struggle_detection","summary":"Builder spent 4x average time on variable scope missions","detail":"Pattern detected across 3 sessions","source":"pattern_detector","observations":["obs-001","obs-003","obs-007"]}
```

### 6.6 sessions.jsonl

Each line is a session summary.

```json
{"type":"session","id":"ses-001","start":"2026-07-21T09:00:00Z","end":"2026-07-21T10:15:00Z","duration":4500,"missions":["variables-101","functions-201"],"observations":42,"xpEarned":150}
```

### 6.7 Size Estimates

Based on average usage patterns:

| Period | Observations | Metrics | Insights | Total Size |
|--------|-------------|---------|----------|------------|
| 1 day | ~170 | ~42 | ~10 | ~100 KB |
| 30 days | ~5,100 | ~1,260 | ~300 | ~3 MB |
| 90 days | ~15,300 | ~3,780 | ~900 | ~9 MB |
| 1 year | ~62,000 | ~15,330 | ~3,650 | ~36 MB |

These are estimates. Actual size depends on usage intensity and evidence content.

### 6.8 Encryption

Export can be encrypted with optional PGP or password-based encryption (AES-256-GCM). Encrypted exports include a detached header with the schema version and encryption algorithm. The key is never stored alongside the export.

---

## 7. Deletion

Deletion is not a feature — it is a right. The architecture must make deletion complete, verifiable, and irreversible.

### 7.1 Three-Tier Deletion

The system supports three tiers of deletion, each progressively more thorough.

**Tier 1 — Soft Delete**

Marks records as deleted in the database. Records are hidden from all queries and exports. A background job permanently deletes soft-deleted records after 30 days.

- Duration: Instant (mark), 30 days (actual removal)
- Recoverable: Yes, within the 30-day window
- Database impact: Minimal — flag update
- Use case: Accidental deletion, second thoughts

**Tier 2 — Hard Delete**

Immediately overwrites the data in the database. Removes all indexes pointing to the data. Runs VACUUM to reclaim space. The database file is rewritten so that deleted data is not recoverable by file inspection.

- Duration: Variable — depends on data volume
- Recoverable: No
- Database impact: Medium — VACUUM requires exclusive lock
- Use case: Intentional permanent deletion

**Tier 3 — Cryptographic Delete**

For critical data (reflection data, evidence content), the system overwrites the data with random bytes three times before deletion. Each pass uses a different random seed. After the third pass, the data is hard-deleted.

- Pass 1: Overwrite with random bytes (passphrase: `0xDEADBEEF`)
- Pass 2: Overwrite with random bytes (passphrase: random)
- Pass 3: Overwrite with zeros
- Hard delete and VACUUM follow
- Duration: Longer — I/O bound
- Recoverable: Theoretically impossible with current technology
- Use case: Paranoia-level deletion of sensitive data

### 7.2 Deletion Verification

After each deletion operation, the system performs verification:

1. **Read verification:** Attempt to read the deleted records. Must return zero results.
2. **Integrity check:** Run `PRAGMA integrity_check` on the database.
3. **Size verification:** Confirm that the database file size decreased by approximately the expected amount.
4. **Report:** Generate a deletion report summarizing what was deleted, which tier was used, and the verification results.

If verification fails (e.g., data is still readable), the system logs the failure and alerts the Builder. The system does not consider the deletion complete until verification passes.

### 7.3 Partial Deletion

The Builder can delete specific categories, date ranges, or individual records:

- `ascend delete --category reflection --hard` — Deletes all reflection data
- `ascend delete --before 2026-06-01 --soft` — Soft-deletes data before June 1
- `ascend delete --all --crypto` — Cryptographic deletion of all data
- `ascend delete --id obs-001` — Deletes a specific observation

---

## 8. Anonymization

For Builders who opt into aggregate analysis or AI model training, data must be anonymized before it leaves the device. Anonymization is a one-way transformation — the output cannot be reversed to recover the original data.

### 8.1 Anonymization Pipeline

Raw data enters the anonymization pipeline. The pipeline applies transformations in order:

1. **Identity stripping:** The `builder_id` field is replaced with a random nonce. The mapping from real ID to nonce is stored locally and never exported.
2. **Session stripping:** The `session_id` field is replaced with a random nonce.
3. **Timestamp generalization:** Timestamps are rounded to day granularity. `2026-07-21T14:30:00Z` becomes `2026-07-21`.
4. **Free-text removal:** All free-text fields are removed — evidence content, reflection notes, self-assessment text, goal descriptions. These fields cannot be anonymized; they must be dropped.
5. **Metric bucketing:** Exact metric values are replaced with buckets:
   - Focus time: `<15min`, `15-30min`, `30-60min`, `>60min`
   - Score: `<50`, `50-69`, `70-84`, `85-100`
   - Session duration: same as focus time
   - Struggle level: `none`, `low`, `medium`, `high`
6. **ID re-keying:** All internal IDs (observation IDs, mission IDs, session IDs) are replaced with new random IDs. The mapping is discarded after anonymization.

### 8.2 Verification

After anonymization, the system verifies:

- No `builder_id` appears in the output.
- No session can be linked to a specific Builder.
- No timestamps are more precise than one day.
- No free-text fields are present.
- Metric values are bucketed.
- The output is internally consistent (IDs still reference each other).

### 8.3 What Remains

After anonymization, the output contains:

- Anonymized observation sequences: "A Builder completed mission `variables-101` with a score in the `70-84` range on `2026-07-21`."
- Behavioral patterns: "The Builder showed high struggle on function-related missions."
- Progression data: "The Builder leveled from 3 to 7 over 45 days."
- Session statistics: "The Builder had 12 sessions in July, average duration 30-60 minutes."

This data is statistically useful for aggregate analysis (e.g., "users commonly struggle on variable scope") without identifying any individual Builder.

---

## 9. Sharing Protocol

If the Builder chooses to share data, the system provides a structured, auditable sharing protocol.

### 9.1 Sharing Flow

```
Builder → Select data → Choose recipient → Choose duration → Grant access → Revocable at any time
```

1. **Select data:** The Builder chooses specific categories, date ranges, or individual records to share.
2. **Choose recipient:** The Builder specifies the recipient — a person, an organization, or a system (e.g., AI training pipeline).
3. **Choose duration:** The Builder sets an expiration date for access. Default is 30 days. Maximum is 1 year.
4. **Grant access:** The Builder confirms the sharing request. The system generates an access token and an audit log entry.
5. **Revocable at any time:** The Builder can revoke access before expiration. Revocation invalidates the access token immediately.

### 9.2 Sharing Requirements

Every sharing operation must satisfy:

- **Explicit selection:** The Builder hand-picks what to share. There is no "share everything" option.
- **Time-bound access:** Sharing always has an expiration. Permanent sharing is not allowed.
- **Revocable:** The Builder can revoke at any time without justification.
- **Audit log:** Every access by the recipient is logged — who accessed what, when, and how many records.
- **No redistribution:** The recipient cannot sublicense, resell, or redistribute the data.
- **Purpose limitation:** The Builder specifies the purpose of sharing. The recipient may only use the data for that purpose.

### 9.3 Access Token

```json
{
  "tokenId": "tok-abc123",
  "builderId": "nonce-abc123def456",
  "recipient": "researcher@example.com",
  "dataCategories": ["observations", "metrics"],
  "dateRange": {"from": "2026-01-01", "to": "2026-07-01"},
  "expiresAt": "2026-08-21T00:00:00Z",
  "purposes": ["academic_research"],
  "createdAt": "2026-07-21T14:30:00Z",
  "revokedAt": null
}
```

### 9.4 Audit Log Entry

```json
{
  "timestamp": "2026-07-21T15:00:00Z",
  "tokenId": "tok-abc123",
  "recipient": "researcher@example.com",
  "action": "read",
  "dataType": "observations",
  "count": 500,
  "allowed": true
}
```

---

## 10. Encryption

Encryption protects data at rest, in transit, and during export. The system provides encryption options without mandating them — the Builder chooses the level of protection.

### 10.1 At Rest

- **Default:** SQLite with no encryption. Suitable for local, single-user devices.
- **Optional:** SQLite encryption via `sqlcipher` or equivalent. Opt-in at database initialization.
- **Key management:** The encryption key is derived from the Builder's passphrase using PBKDF2. The key never leaves the device.
- **Performance impact:** ~10-20% overhead on write operations. No significant impact on reads.

### 10.2 In Transit

- **Default:** No network code is included in the default build. There is nothing to encrypt.
- **Optional:** If the Builder enables network features (sync, sharing), all transmissions use TLS 1.3.
- **Certificate pinning:** The system pins certificates for known endpoints. No self-signed certificates are accepted for data transmission.
- **Forward secrecy:** All encrypted transmissions use ephemeral Diffie-Hellman key exchange.

### 10.3 At Export

- **Default:** Exports are unencrypted. The Builder can add encryption.
- **Optional encryption:** AES-256-GCM with a password-derived key.
- **Optional PGP:** The Builder can supply a PGP public key for encryption.
- **Metadata:** Encrypted exports include a detached header with algorithm and nonce. The key is stored separately.

### 10.4 Key Management

| Key | Purpose | Storage | Backup |
|-----|---------|---------|--------|
| Builder passphrase | Local database encryption | Builder's memory | Builder's responsibility |
| TLS certificates | Network encryption | OS certificate store | OS-managed |
| PGP key | Export encryption | Builder's keyring | Builder's responsibility |
| Session keys | Ephemeral network sessions | Memory only | Not backed up |

No cloud key escrow. No key recovery service. If the Builder loses their passphrase, the data cannot be recovered. This is a feature, not a bug.

---

## 11. Auditing

Every data access is logged. The audit log is append-only and tamper-evident.

### 11.1 Audit Log Schema

```typescript
interface DataAccessLog {
  timestamp: string    // ISO 8601
  actor: 'builder' | 'runtime' | 'cognitive' | 'experience' | 'ai_model' | 'third_party'
  action: 'read' | 'write' | 'delete' | 'export' | 'share' | 'revoke'
  dataType: 'observation' | 'metric' | 'insight' | 'reflection' | 'evidence' | 'profile'
  count: number        // records affected
  allowed: boolean     // was the access permitted
  reason?: string      // why the access was attempted
  tokenId?: string     // for shared access
  recipient?: string   // for share/revoke actions
}
```

### 11.2 Audit Properties

- **Append-only:** The audit log is an append-only structure. Records cannot be modified or deleted.
- **Tamper-evident:** Each record includes a hash of the previous record. Tampering with a record breaks the chain.
- **Builder-accessible:** The Builder can review the audit log at any time via `ascend audit`.
- **Filterable:** The Builder can filter by actor, action, data type, and date range.
- **Exportable:** The audit log can be exported alongside the data.

### 11.3 Audit Log Example

```
2026-07-21T14:30:00Z | builder     | write   | observation | 1    | allowed | evidence submission
2026-07-21T14:30:01Z | cognitive   | read    | observation | 42   | allowed | insight generation
2026-07-21T14:30:02Z | cognitive   | write   | insight     | 1    | allowed | struggle detection
2026-07-21T14:35:00Z | experience  | read    | insight     | 3    | allowed | display dashboard
2026-07-21T15:00:00Z | builder     | read    | audit       | 50   | allowed | review activity
```

---

## 12. No-Telemetry Guarantee

The ASCEND cognitive system has zero telemetry by default. It sends no data to any server without explicit consent. It has no "phone home" mechanism. It can be fully air-gapped.

### 12.1 What This Means

- The default build contains no network code in the core engine, cognitive layer, or CLI.
- The system does not check for updates automatically.
- The system does not send crash reports.
- The system does not collect usage statistics.
- The system does not ping a license server.
- The system does not download content from a remote server without explicit user action.
- The system does not embed analytics SDKs, tracking pixels, or beacon calls.

### 12.2 Air-Gap Verification

To verify that a given installation is fully air-gapped:

1. Check that no network services are listening: `netstat -an | find "LISTEN"`
2. Check that no outbound connections are established: `netstat -an | find "ESTABLISHED"`
3. Verify that the system directory contains no network libraries beyond standard TLS.
4. Run `ascend doctor` — it reports the network status.

### 12.3 Network-Optional Features

The following features require network access and are disabled by default:

- Data sharing (Section 9)
- AI model download (installation of optional local models)
- Package updates (downloading new mission packages from registries)
- Sync to alternative device

Each of these requires explicit opt-in. Each is implemented as a separate module that is not loaded by default.

---

## 13. Regulatory Alignment

While the architecture is designed for Builder sovereignty first, it also aligns with major data protection regulations. Alignment is a side effect of the architecture, not the driver.

### 13.1 GDPR (General Data Protection Regulation)

| Requirement | How ASCEND Meets It |
|-------------|---------------------|
| Right to access (Art. 15) | Builder can access all data via the CLI or SDK. |
| Right to rectification (Art. 16) | Builder can annotate and correct observations. |
| Right to erasure (Art. 17) | Three-tier deletion including cryptographic delete. |
| Right to restrict processing (Art. 18) | Builder can pause the Cognitive Layer. |
| Right to data portability (Art. 20) | Export in JSON/CSV via `ascend export`. |
| Right to object (Art. 21) | Builder can disable any cognitive component. |
| Automated decision-making (Art. 22) | All insights are explainable and reviewable. |

### 13.2 LGPD (Lei Geral de Proteção de Dados Pessoais)

Same rights as GDPR for Brazilian users, plus:

| Requirement | How ASCEND Meets It |
|-------------|---------------------|
| Consent for sensitive data (Art. 11) | Granular consent per data category. |
| Shared responsibility (Art. 42) | Builder controls all sharing decisions. |

### 13.3 CCPA (California Consumer Privacy Act)

| Requirement | How ASCEND Meets It |
|-------------|---------------------|
| Right to know (1798.110) | Audit log provides complete access history. |
| Right to delete (1798.105) | Cryptographic deletion available. |
| Right to opt-out (1798.120) | No data sale — no opt-out needed. |
| Non-discrimination (1798.125) | Full functionality without data sharing. |

### 13.4 COPPA (Children's Online Privacy Protection Act)

If ASCEND is used by minors (under 13 in the US):

- Parental consent is required for any data collection beyond what is locally stored.
- The default configuration (local only, no telemetry) satisfies COPPA without additional measures.
- If sharing is enabled for a minor, parental controls are enforced.

---

## 14. Enforcement

Data sovereignty is not optional. Violations are architectural breaches and are subject to the Architectural Enforcement and Governance System (AEGS).

### 14.1 Architectural Breach Classification

Any violation of the rules in this document is classified as an architectural breach.

| Violation | Severity | Consequence |
|-----------|----------|-------------|
| Data leaves device without consent | Critical | Immediate revert, architecture review |
| Backdoor added for Developer access | Critical | Immediate revert, TSC review |
| Telemetry added without opt-in | Critical | Immediate revert, architecture review |
| Consent mechanism bypassed | Critical | Immediate revert, TSC review |
| Encryption weakened or removed | High | Immediate revert, architecture review |
| Audit log disabled or truncated | High | Immediate revert, architecture review |
| Anonymization pipeline bypassed | High | Immediate revert, architecture review |
| Export format made proprietary | Medium | Revert, documentation update |
| Deletion made incomplete | Critical | Immediate revert, architecture review |

### 14.2 I14 — Cognitive Independence Invariant

The I14 invariant (Cognitive Independence) includes data sovereignty as a core requirement. The invariant states:

> *The Cognitive Layer must be fully functional with zero external dependencies. Builder data must never leave the device without explicit consent. The Cognitive Layer must never depend on a third-party service for its core functions.*

Any PR that weakens I14 is automatically rejected. The CI system checks for I14 compliance before merging.

### 14.3 PR Gate

Every pull request that touches data handling must pass the following checks:

1. **Data flow review:** A reviewer traces every new data path to ensure it does not violate ownership rules.
2. **Consent check:** If the PR adds a new data collection point, it must also add the corresponding consent mechanism.
3. **Deletion check:** If the PR adds a new data type, it must also add the deletion path for that type.
4. **Audit check:** If the PR adds a new data access pattern, it must also log it to the audit trail.
5. **Anonymization check:** If the PR adds data that could identify the Builder, it must include an anonymization path.

### 14.4 Final Authority

The Chief Architect is the final authority on data sovereignty disputes. If there is ambiguity in how a rule applies, the Chief Architect resolves it. In all cases, the resolution must favor Builder sovereignty. There is no appeal to commercial interest. There is no appeal to convenience. The Builder's ownership is absolute.

---

## 15. Appendix A — Threat Model

This section identifies threat vectors against Builder data sovereignty and the architectural countermeasures in place.

| Threat | Description | Countermeasure |
|--------|-------------|---------------|
| **Supply chain attack** | Malicious dependency exfiltrates data | Dependency pinning, audit, air-gap compatible |
| **Developer backdoor** | Contributor adds hidden data access | Code review, architectural gates, CI checks |
| **Cloud provider access** | Hosting provider accesses local data | Local-first, no cloud dependency |
| **AI model exfiltration** | Model captures data in training | Anonymization pipeline, local-only model |
| **Third-party abuse** | Recipient shares data further | Non-redistribution clause, audit log |
| **Device theft** | Physical access to database | Optional SQLCipher encryption |
| **Insider threat** | Project maintainer accesses Builder data | No remote access, no admin panel |
| **Legal demand** | Government requests Builder data | ASCEND has no data to hand over — data is on Builder's device |

---

## 16. Appendix B — Glossary

| Term | Definition |
|------|------------|
| **Builder** | The end user of ASCEND — the person developing competencies. |
| **Cognitive Layer** | The system component that observes, analyzes, and infers from Runtime data. |
| **Cognitive data** | Any data generated by or derived from Builder activity within ASCEND. |
| **Experience Layer** | The UI/SDK layer that presents data to the Builder. |
| **Runtime** | The core engine that executes missions, manages state, and fires events. |
| **Observation** | A raw, timestamped record of a Runtime event or state snapshot. |
| **Insight** | A derived conclusion or pattern detected from observations. |
| **Recommendation** | A suggested action generated from insights. |
| **Anonymization** | The irreversible transformation of data to remove personal identifiers. |
| **Consent** | An affirmative, granular, revocable authorization to access data. |
| **Telemetry** | Automatic data collection sent to a remote server. |
| **Air-gapped** | A system with no network connectivity. |
| **Nonce** | A random identifier used as a one-time replacement for a real identifier. |
| **VACUUM** | A SQLite command that rebuilds the database file to reclaim space. |
| **AEGS** | Architectural Enforcement and Governance System. |
| **TSC** | Technical Steering Committee. |

---

*This document is frozen per the v1 architecture freeze. Any amendment requires TSC approval and must not reduce Builder data sovereignty.*
