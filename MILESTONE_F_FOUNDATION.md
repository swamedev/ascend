# Milestone F — Intelligence Foundation

| Field | Value |
|-------|-------|
| **Version** | 1.1 |
| **Status** | Approved |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, MILESTONES.md, ARCH-0030 Cognitive Architecture, DOC-0010 Cognitive Principles |

---

> *"Antes de pensar, o ASCEND precisa aprender a observar."*

---

## Overview

Milestone F — Intelligence is divided into five capability phases (F1–F5). Each phase builds on the previous, and each phase is **optional, independent, and model-agnostic**.

The entire milestone is governed by:
- **DOC-0010** — Cognitive Principles (the Constitution)
- **ARCH-0030** — Cognitive Architecture (the blueprint)
- **ARCH-0031** — Observation Model (the formal definitions)
- **SPEC-0005** — Cognitive Protocol (the communication rules)
- **I14** — Cognitive Independence (the invariant)

---

## Phases

```
F1 ─── Observation Engine
  │
  ├── F1.0 — Observation Collector
  ├── F1.05 — Observation Normalizer
  ├── F1.1 — Signal Extractor
  ├── F1.2 — Basic Pattern Detector
  └── F1.3 — Insight Stream
          │
F2 ─── Reasoning Engine
  │
  ├── F2.0 — Deterministic Reasoner
  ├── F2.1 — Model Adapter Interface
  ├── F2.2 — Confidence Scorer
  └── F2.3 — Recommendation Builder
          │
F3 ─── Mentor Engine
  │
  ├── F3.0 — Mentor UI Shell
  ├── F3.1 — Insight Presentation
  ├── F3.2 — Recommendation UX
  └── F3.3 — Feedback Loop
          │
F4 ─── Adaptive Learning
  │
  ├── F4.0 — Trajectory Predictor
  ├── F4.1 — Difficulty Scorer
  ├── F4.2 — Content Sequencer
  └── F4.3 — Personalization Profile
          │
F5 ─── Cognitive Network
  │
  ├── F5.0 — Anonymized Pattern Aggregator
  ├── F5.1 — Privacy Layer
  ├── F5.2 — Collective Insight Engine
  └── F5.3 — Cross-Builder Recommendations
```

---

## F1 — Observation Engine

**Status:** ⬜ Planned (first to implement)
**Theme:** *Learn to see.*

### F1.0 — Observation Collector

| Aspect | Detail |
|--------|--------|
| **What** | Subscribes to Runtime domain events, converts to Observations per ARCH-0031 |
| **Input** | Domain events (ARCH-0026) + state snapshots |
| **Output** | `Observation[]` persisted locally |
| **Model needed?** | No — pure event subscription |
| **Effort** | S |

### F1.05 — Observation Normalizer

| Aspect | Detail |
|--------|--------|
| **What** | Transforms raw Observations into canonical NormalizedObservations: ULID identifiers, ISO 8601 UTC timestamps, canonical field mapping (snake_case → camelCase), PII and sensitive data stripping, correlation/causation trace IDs |
| **Input** | `Observation[]` (raw, source-native format) |
| **Output** | `NormalizedObservation[]` (canonical, analysis-ready) |
| **Model needed?** | No — deterministic field mapping, regex, pure functions |
| **Effort** | S |
| **Specification** | ARCH-0039 Observation Normalization |

### F1.1 — Signal Extractor

| Aspect | Detail |
|--------|--------|
| **What** | Extracts structured signals from raw observations |
| **Input** | `Observation[]` |
| **Output** | `Signal[]` with confidence scores |
| **Model needed?** | No — deterministic rules |
| **Effort** | M |

### F1.2 — Basic Pattern Detector

| Aspect | Detail |
|--------|--------|
| **What** | Identifies meaningful patterns across signals over time |
| **Input** | `Signal[]` |
| **Output** | `Pattern[]` with confidence scores |
| **Model needed?** | No — heuristics (thresholds, moving averages, frequency analysis) |
| **Effort** | M |

### F1.3 — Insight Stream

| Aspect | Detail |
|--------|--------|
| **What** | Produces structured insights from patterns and publishes to Experience Layer |
| **Input** | `Pattern[]` |
| **Output** | `Insight[]` via SPEC-0005 |
| **Model needed?** | No — decision tree rules |
| **Effort** | S |

### F1 Gate

- [ ] Observations are collected from Runtime events
- [ ] Observations are normalized to canonical format (ULID, camelCase, PII-free, traceable)
- [ ] Signals are extracted deterministically
- [ ] Basic patterns (plateau, streak, momentum) are detected
- [ ] Insights are published to a stream
- [ ] **Zero ML dependencies**

---

## F2 — Reasoning Engine

**Status:** ⬜ Planned
**Theme:** *Learn to reason.*

### F2.0 — Deterministic Reasoner

| Aspect | Detail |
|--------|--------|
| **What** | Rule-based engine that produces recommendations from insights |
| **Input** | `Insight[]` |
| **Output** | `Recommendation[]` |
| **Model needed?** | No — if-then rules |
| **Effort** | M |

### F2.1 — Model Adapter Interface

| Aspect | Detail |
|--------|--------|
| **What** | Defines the ModelAdapter protocol per SPEC-0005. Enables plugging in any AI model. |
| **Input** | `Observation[]`, `AnalysisContext` |
| **Output** | `Insight[]` |
| **Model needed?** | Optional — interface only |
| **Effort** | S |

### F2.2 — Confidence Scorer

| Aspect | Detail |
|--------|--------|
| **What** | Calculates confidence for each insight and recommendation |
| **Input** | Historical outcome data |
| **Output** | Confidence scores (0.0–1.0) |
| **Model needed?** | No — statistics (Bayesian update, moving average) |
| **Effort** | M |

### F2.3 — Recommendation Builder

| Aspect | Detail |
|--------|--------|
| **What** | Builds actionable recommendations with explanation and rationale |
| **Input** | `Insight`, `BuilderState` |
| **Output** | `Recommendation` |
| **Model needed?** | Optional — NLG can enhance but deterministic templates work |
| **Effort** | M |

### F2 Gate

- [ ] Recommendations are generated from insights
- [ ] Model Adapter Interface is defined and documented
- [ ] Confidence scoring is implemented
- [ ] Recommendations include rationale and are explainable
- [ ] **Rule-based fallback works when no model is connected**

---

## F3 — Mentor Engine

**Status:** ⬜ Planned
**Theme:** *Learn to guide.*

### F3.0 — Mentor UI Shell

| Aspect | Detail |
|--------|--------|
| **What** | UI component that displays insights and recommendations |
| **Input** | Insight Stream |
| **Output** | Rendered insights in Dashboard, Mentor panel |
| **Model needed?** | No — pure UI |
| **Effort** | M |

### F3.1 — Insight Presentation

| Aspect | Detail |
|--------|--------|
| **What** | Visual components for each insight type (cards, badges, charts) |
| **Input** | `Insight` |
| **Output** | Rendered insight with severity color, confidence bar, explanation |
| **Model needed?** | No — UI rendering |
| **Effort** | S |

### F3.2 — Recommendation UX

| Aspect | Detail |
|--------|--------|
| **What** | Interactive recommendation cards with accept/dismiss/snooze |
| **Input** | `Recommendation` |
| **Output** | Decision input |
| **Model needed?** | No — interactive UI |
| **Effort** | S |

### F3.3 — Feedback Loop

| Aspect | Detail |
|--------|--------|
| **What** | Captures decisions and outcomes, feeds back into confidence scoring |
| **Input** | `Decision`, `Outcome` |
| **Output** | Updated confidence scores |
| **Model needed?** | No — data collection |
| **Effort** | M |

### F3 Gate

- [ ] Mentor UI is implemented (can be empty state if no insights)
- [ ] Insights are displayed with confidence and rationale
- [ ] Recommendations can be accepted or dismissed
- [ ] Feedback loop closes the cognitive cycle
- [ ] **Works identically with or without AI**

---

## F4 — Adaptive Learning

**Status:** ⬜ Planned
**Theme:** *Learn to adapt.*

### F4.0 — Trajectory Predictor

| Aspect | Detail |
|--------|--------|
| **What** | Predicts likely next goals and milestones based on patterns |
| **Input** | `Pattern[]`, `BuilderState` |
| **Output** | Goal predictions with confidence |
| **Model needed?** | Recommended — ML improves accuracy but heuristics work |
| **Effort** | L |

### F4.1 — Difficulty Scorer

| Aspect | Detail |
|--------|--------|
| **What** | Scores mission/journey difficulty relative to Builder's current level |
| **Input** | Builder competencies, mission requirements |
| **Output** | Difficulty score (1–10) |
| **Model needed?** | No — formula-based |
| **Effort** | S |

### F4.2 — Content Sequencer

| Aspect | Detail |
|--------|--------|
| **What** | Dynamically sequences content based on Builder's pace and gaps |
| **Input** | Competency state, available journeys/missions |
| **Output** | Ordered list of recommended next content |
| **Model needed?** | Optional — graph traversal works without ML |
| **Effort** | L |

### F4.3 — Personalization Profile

| Aspect | Detail |
|--------|--------|
| **What** | Builder profile that captures learning style, pace, preferences |
| **Input** | Historical observations, decisions, outcomes |
| **Output** | Personalization config |
| **Model needed?** | No — aggregated statistics |
| **Effort** | M |

### F4 Gate

- [ ] Content can be dynamically sequenced
- [ ] Difficulty scoring is calibrated
- [ ] Personalization profile is maintained locally
- [ ] Builder can override any adaptive suggestion
- [ ] **[Optional] ML improves quality but architecture works without it**

---

## F5 — Cognitive Network

**Status:** 🌌 Vision
**Theme:** *Learn together.*

### F5.0 — Anonymized Pattern Aggregator

| Aspect | Detail |
|--------|--------|
| **What** | Aggregates anonymized patterns across Builders for collective insight |
| **Input** | Anonymized observations (opt-in only) |
| **Output** | Aggregate pattern database |
| **Model needed?** | Yes — statistical/ML models benefit from scale |
| **Effort** | XL |

### F5.1 — Privacy Layer

| Aspect | Detail |
|--------|--------|
| **What** | Ensures all cross-Builder data is anonymized, aggregated, and consent-based |
| **Input** | Raw observations |
| **Output** | Anonymized data points |
| **Model needed?** | No — deterministic PII stripping |
| **Effort** | M |

### F5.2 — Collective Insight Engine

| Aspect | Detail |
|--------|--------|
| **What** | Generates insights based on cross-Builder patterns |
| **Input** | Aggregate patterns + individual observations |
| **Output** | Collective insights |
| **Model needed?** | Optional — statistics work at scale |
| **Effort** | L |

### F5.3 — Cross-Builder Recommendations

| Aspect | Detail |
|--------|--------|
| **What** | Recommends content based on what similar Builders found effective |
| **Input** | Collective insights + individual profile |
| **Output** | Recommendations with "similar Builders" context |
| **Model needed?** | Recommended — collaborative filtering |
| **Effort** | XL |

### F5 Gate

- [ ] Privacy layer is in place (anonymization, consent, opt-in)
- [ ] Cross-Builder patterns are aggregated without exposing individual data
- [ ] Collective insights are available as optional enhancement
- [ ] **Builder can disable network features and lose zero core functionality**

---

## Dependency Map

```
F1.0 ──→ F1.05 ──→ F1.1 ──→ F1.2 ──→ F1.3
                                         │
                                         ↓
                                  F2.0 ──→ F2.1 ──→ F2.2 ──→ F2.3
                                                              │
                                                              ↓
                                                       F3.0 ──→ F3.1 ──→ F3.2 ──→ F3.3
                                                                                      │
                                                                                      ↓
                                                                               F4.0 ←─┘
                                                                                │
                                                                                ↓
                                                                          F4.1 → F4.2 → F4.3
                                                                                            │
                                                                                            ↓
                                                                                     F5.0 → F5.1 → F5.2 → F5.3
```

Each phase depends on the previous. Within a phase, components can be built independently.

---

## Effort Estimate

| Phase | Components | Effort (days) | Model Required? |
|-------|------------|---------------|-----------------|
| F1 | 5 | 6-8 | ❌ No |
| F2 | 4 | 6-8 | ❌ Optional |
| F3 | 4 | 5-7 | ❌ No |
| F4 | 4 | 8-12 | ❌ Optional |
| F5 | 4 | 15-20 | ⚠️ Recommended |
| **Total** | **20** | **39-54** | **—** |

---

## Invariant Compliance

| Invariant | How F1–F5 complies |
|-----------|-------------------|
| **I1** — Domain independent | Cognitive Layer never imports `ascend.domain` |
| **I5** — AI never alters rules | Cognitive Layer only observes/recommends |
| **I6** — Offline core | F1–F3 work fully offline; F4 optional; F5 requires network |
| **I7** — Testable without UI | Every cognitive component is testable via its protocol |
| **I8** — Data belongs to user | All observations local by default; F5 requires opt-in |
| **I9** — Inward communication | Cognitive → Experience only; no layer skipping |
| **I12** — SDK Independence | Insights consumed via SDK, not direct HTTP |
| **I14** — Cognitive Independence | Zero write access to Runtime |
| **I15** — Observation Determinism | Replay produces identical results |
| **I16** — Observation Append Only | Observations are never modified after write |

---

## Prerequisites

Before implementing F1:

- [x] **ARCH-0030** — Cognitive Architecture (approved)
- [x] **DOC-0010** — Cognitive Principles (ratified)
- [x] **ARCH-0031** — Observation Model (approved)
- [x] **ARCH-0039** — Observation Normalization (approved)
- [x] **ARCH-0040** — Signal Extraction Architecture (approved)
- [x] **ARCH-0041** — Timeline and Replay (approved)
- [x] **SPEC-0005** — Cognitive Protocol (approved)
- [x] **I14** — Cognitive Independence (added to DOC-0009)
- [x] **I15** — Observation Determinism (added to DOC-0009)
- [x] **I16** — Observation Append Only (added to DOC-0009)
- [x] **F0 Gate** — All architectural documents reviewed and approved
- [x] **F0 Gate** — Zero vendor lock-in verified
- [x] **F0 Gate** — Runtime sovereignty confirmed

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.1 | 2026-07-21 | Chief Architect | Added F1.05 Observation Normalizer, updated dependencies and invariants (OPERAÇÃO PROMETHEUS) |
| 1.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO ATHENA |
