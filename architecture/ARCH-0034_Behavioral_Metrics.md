# ARCH-0034 — Behavioral Metrics

| Field | Value |
|-------|-------|
| **ID** | ARCH-0034 |
| **Name** | Behavioral Metrics |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, ARCH-0003 Core Engine Specification, ARCH-0031 Observation Model |
| **Principle** | Every claimed competency must be a proven competency — every behavioral insight must be a computed metric |

---

## 1. Introduction

Behavioral metrics are the quantitative foundation of the Cognitive Layer. They describe **how** the Builder learns — their focus, persistence, consistency, recovery patterns, exploration habits, and cognitive state — rather than **what** they learned (XP, level, competencies).

**Key distinction:** Domain metrics (XP, level, competency scores) answer the question *"How far has the Builder progressed?"* Behavioral metrics answer *"How does the Builder learn?"* A Builder can have high XP but poor consistency, or master many competencies but burn out due to high cognitive load. These metrics enable the system to detect patterns, adapt recommendations, and provide insight without any AI or ML dependency.

### 1.1 Design Principles

- **Zero AI, Zero ML, Pure Mathematics** — every metric is a deterministic function of observed events. No models, no training, no inference.
- **Formula-First** — every metric has an explicit, implementable formula with defined inputs, outputs, limits, and edge cases.
- **Rolling Windows** — all metrics operate on time windows (default 7-day rolling) to capture recent behavior while maintaining history.
- **Decay Over Static** — exponential moving averages are preferred over raw averages to favor recent behavior.
- **Weighted Composition** — metrics combine into composite scores with explicit, versioned weight allocations.
- **Resilient by Default** — every metric defines behavior for missing data, boundary conditions, and anomalous inputs.

### 1.2 The Behavioral Observation Pipeline

```
Runtime Events → Signal Extraction → Metric Computation → Composite Scores → Insights
     │                                                          │
     └── persisted in Event Store                              └── persisted in Metric Store
```

Each metric is computed on demand or on event arrival. Results are persisted as time-series data points. Composite scores are derived from individual metrics using weighted formulas. No component in this pipeline requires AI.

---

## 2. Common Definitions

### 2.1 Universal Parameters

| Symbol | Name | Default | Description |
|--------|------|---------|-------------|
| `t` | Time window | 7 days (rolling) | The lookback period for metric computation |
| `n` | Event count | computed | Number of relevant events in the time window |
| `w` | Weight factor | varies (0.0–1.0) | Contribution weight of a metric in composite calculations |
| `α` | Decay factor | varies (0.0–1.0) | Smoothing factor for exponential moving average; higher = more weight on recent data |
| `σ` | Standard deviation | computed | Measure of variance in a data set |
| `μ` | Mean | computed | Arithmetic mean of a data set |

### 2.2 Exponential Moving Average

The exponential moving average (EMA) is the primary smoothing function used across all behavioral metrics. It gives more weight to recent observations while retaining memory of past behavior.

```
EMA(new_value, previous_ema, α) = α × new_value + (1 - α) × previous_ema
```

**Initialization:** When no previous EMA exists, the first raw value is used as the initial EMA.

**Decay behavior:** Over time, the influence of past values decays exponentially. After `k` observations, the weight of the initial value is `(1 - α)^k`.

### 2.3 Clamping

All metrics with a defined output range `[min, max]` must clamp their computed value:

```
clamp(value, min, max) = max(min, min(max, value))
```

### 2.4 Neutral Defaults

When no data is available for a metric, a neutral default is returned:

| Condition | Default |
|-----------|---------|
| No events in window | Metric-specific neutral value (defined per metric) |
| Builder has no history | All metrics return their neutral defaults |
| Data loss detected | All metrics recompute from available events on next trigger |

### 2.5 Weight Versioning

Each metric has a `weight` and `version` field. The weight defines the metric's contribution to composite scores. The version enables future recalibration without breaking historical comparisons. When a weight changes, the system records the previous weight alongside the new one in the metric store.

---

## 3. Focus Score

**Purpose:** Measures how consistently the Builder maintains focused work sessions, quantifying the ratio of undistracted deep work to total session time.

### 3.1 Formula

```
Focus_Score = (Σ focused_duration_i / Σ total_session_duration_i) × (1 - interruption_rate)
```

Where:

- `focused_duration_i` = time in Focus Mode for session i (in minutes)
- `total_session_duration_i` = total time for session i (in minutes)
- `interruption_rate` = interruptions / total_hours_in_window

The interruption rate is computed as:

```
interruption_rate = count(focus.flow.lost events) / total_session_hours
```

### 3.2 Input Events

| Event | Role |
|-------|------|
| `focus.mode.entered` | Marks the start of a focused session segment |
| `focus.mode.exited` | Marks the end of a focused session segment; used to compute focused_duration |
| `focus.flow.lost` | Records an interruption event (context switch, notification, break) |

### 3.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = constant interruptions, no focus; 1.0 = perfect focus, zero interruptions |
| Neutral default | 0.5 (no session data available) |

### 3.4 Limits

Clamped to `[0.0, 1.0]`. If computed value exceeds 1.0 (should not occur under normal conditions), clamp to 1.0. If computed value falls below 0.0 (possible if interruption_rate > 1), clamp to 0.0.

### 3.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No sessions recorded | Return neutral default: 0.5 |
| Zero interruptions, all time focused | Return 1.0 |
| All interruptions, no focus time | Return 0.0 |
| Partial session data (entered without exit) | Treat as interrupted; include in interruption count |
| Single session | Compute normally; single session metrics have higher variance |
| Session with zero duration | Exclude from computation (division by zero guard) |

### 3.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 15 (in composite calculations) |
| Version | 1 |
| Time window | Rolling 7 days |
| Minimum sessions for non-default | 1 |

---

## 4. Learning Velocity

**Purpose:** Measures the rate at which the Builder acquires new competencies and XP, representing the speed of skill accumulation over time.

### 4.1 Formula

```
Learning_Velocity = EMA(ΔXP / Δt, previous_velocity, α=0.3)
```

Where:

- `ΔXP` = XP gained in the time window
- `Δt` = time elapsed in the window (in hours)
- `α` = 0.3 (favors recent velocity over historical)

The raw velocity for each observation is:

```
raw_velocity = ΔXP / Δt
```

### 4.2 Input Events

| Event | Role |
|-------|------|
| `behavior.mission.completed` | Carries XP reward data |
| `learning.competency.unlocked` | Carries XP bonus data |
| Any XP-related event | Provides ΔXP data points |

### 4.3 Output

| Property | Value |
|----------|-------|
| Range | `[0, system_max_XP_rate]` |
| Unit | XP per hour |
| Neutral default | 0 (no activity → decays toward 0) |

### 4.4 Limits

The upper bound is determined by the system's maximum achievable XP rate (sum of fastest possible mission completions multiplied by maximum XP rewards per hour). The lower bound is 0.

### 4.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No activity in window | EMA decays toward 0; after sufficient empty windows, approaches 0 |
| First session (no previous_velocity) | Use raw value directly; `EMA(raw, raw, 0.3) = raw` |
| Negative XP (should not occur) | Treat as 0; negative XP violates domain invariants |
| Δt = 0 (two events same timestamp) | Skip duplicate; do not divide by zero |
| Very small Δt (< 1 minute) | Use 1 minute as minimum divisor to avoid extreme inflation |
| XP cap hit | Velocity saturates at system maximum |

### 4.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 20 (in composite calculations) |
| Version | 1 |
| α | 0.3 |
| Time window | Rolling 7 days |

---

## 5. Recovery Rate

**Purpose:** Measures how quickly the Builder resumes focused work after interruptions or breaks. A high recovery rate indicates strong discipline and low friction in returning to work.

### 5.1 Formula

```
Recovery_Rate = EMA(1 / (resume_time - break_time), previous_rate, α=0.2)
```

With normalization:

```
normalized_recovery = min(1.0, 60 / minutes_away)
```

Where:

- `resume_time - break_time` = time between pause and resume (in minutes)
- `minutes_away` = the same interval, in minutes
- `α` = 0.2 (moderate smoothing)

The per-event recovery score is:

```
recovery_event_score = min(1.0, 60 / minutes_away)
```

A Builder who resumes in 1 minute scores `min(1.0, 60/1) = 1.0`. A Builder who resumes in 60 minutes scores `min(1.0, 60/60) = 1.0`. A Builder who resumes in 120 minutes scores `min(1.0, 60/120) = 0.5`.

### 5.2 Input Events

| Event | Role |
|-------|------|
| `recovery.pause.started` | Builder paused or was interrupted |
| `recovery.pause.ended` | Builder ended the pause |
| `recovery.resume.after_absence` | Builder returned after extended absence |

### 5.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = very slow to recover; 1.0 = instant recovery |
| Neutral default | 1.0 (no breaks needed = perfect recovery) |

### 5.4 Limits

Clamped to `[0.0, 1.0]`. The normalization function ensures the per-event score never exceeds 1.0.

### 5.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No breaks recorded | Return 1.0 — Builder never needed to recover |
| Very long absence (> 24 hours) | Decay to 0.1; extended absence indicates low recovery readiness |
| Multiple rapid pause/resume cycles | Each cycle contributes a data point; EMA smooths variance |
| Break time = resume time (instant) | `minutes_away = 0`; guard with `max(1, minutes_away)` to avoid division by zero |
| Back-to-back pauses without resume | Ignore second pause until first is resolved; pend the open interval |

### 5.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 10 (in composite calculations) |
| Version | 1 |
| α | 0.2 |
| Time window | Rolling 7 days |

---

## 6. Persistence Index

**Purpose:** Measures the Builder's ability to continue working toward a goal despite difficulty, failure, or discouragement. Rewards retrying failed missions.

### 6.1 Formula

```
Persistence_Index = (completed_missions / started_missions) × retry_factor
```

Where:

- `completed_missions` = count of missions completed in current window
- `started_missions` = count of missions started in current window
- `retry_factor` = multiplicative bonus for retrying failed missions

```
retry_factor = min(1.0, 1.0 + (0.2 × retried_missions / started_missions))
```

Only missions started within the current time window are considered. A mission that was started in a previous window and completed in the current window is not counted toward this metric (it belongs to the window where it started).

### 6.2 Input Events

| Event | Role |
|-------|------|
| `behavior.mission.started` | Counts as started mission |
| `behavior.mission.completed` | Counts as completed mission |
| `behavior.mission.abandoned` | Counts as neither completed nor retried |
| `behavior.mission.retried` | A previously abandoned/failed mission was retried |

### 6.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = all started missions abandoned; 1.0 = all completed, retried failures |
| Neutral default | 0.5 (no missions started) |

### 6.4 Limits

Clamped to `[0.0, 1.0]`. The retry_factor is capped at 1.0 to prevent the multiplier from pushing the score above the maximum.

### 6.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No missions started | Return neutral default: 0.5 |
| All started missions completed | Return 1.0 (retry_factor = 1.0 if no failures, or up to 1.0 with retries) |
| All missions abandoned | Return 0.0 |
| All missions failed and none retried | Return 0.0 |
| All missions failed, all retried and completed | Return 1.0 (completion ratio 1.0 × retry_factor 1.0) |
| Single mission started and completed | Return 1.0 |
| Single mission abandoned | Return 0.0 |

### 6.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 18 (in composite calculations) |
| Version | 1 |
| Time window | Rolling 7 days |

---

## 7. Consistency

**Purpose:** Measures the regularity of learning sessions over time. Consistency rewards daily engagement and penalizes erratic attendance patterns, regardless of session duration.

### 7.1 Formula

```
Consistency = (active_days / total_days_in_window) × streak_bonus
```

Where:

- `active_days` = number of days in the window with at least one `behavior.*` event
- `total_days_in_window` = total calendar days in the rolling window (default: 7)
- `streak_bonus` = logarithmic reward for consecutive active days

```
streak_bonus = log₂(1 + current_streak_length) / log₂(1 + max_possible_streak)
```

- `current_streak_length` = number of consecutive active days ending today
- `max_possible_streak` = total_days_in_window (maximum possible streak)

The streak_bonus ratio approaches 1.0 as the current streak approaches the maximum possible streak. The logarithmic scaling means early streak days contribute more proportionally than later days.

### 7.2 Input Events

| Event | Role |
|-------|------|
| Any `behavior.*` event | Signals an active day (presence) |
| Daily activity heartbeat | Optional fallback if no other events fire |

### 7.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = no active days; 1.0 = every day active with max streak |
| Neutral default | 0.0 (no events → no active days) |

### 7.4 Limits

Clamped to `[0.0, 1.0]`. Both `active_days / total_days_in_window` and `streak_bonus` naturally fall within `[0, 1]`, so the product is also bounded.

### 7.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| Single active day in window | `active_days = 1`, `total_days = 7`, `streak_length = 1`, `streak_bonus = log₂(2)/log₂(8) ≈ 0.33`; `Consistency ≈ 0.05` |
| All days active with full streak | Return 1.0 |
| Perfect attendance alternating (on, off, on, off...) | `active_days = 4`, `total_days = 7`, streak breaks daily; `streak_bonus = log₂(2)/log₂(8) ≈ 0.33`; `Consistency ≈ 0.19` |
| First day (streak = 1) with activity | Low but non-zero score |
| Zero days active | Return 0.0 |

### 7.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 12 (in composite calculations) |
| Version | 1 |
| Time window | Rolling 7 days |
| Minimum events per active day | 1 behavior.* event |

---

## 8. Reflection Score

**Purpose:** Measures the Builder's engagement with metacognitive activities — journaling, self-assessment, goal setting, and retrospective analysis. Reflection is a leading indicator of deep learning.

### 8.1 Formula

```
Reflection_Score = (reflection_events / total_sessions) × quality_factor
```

Where:

- `reflection_events` = count of `reflection.*` events in the window
- `total_sessions` = count of learning sessions in the window
- `quality_factor` = estimated depth of reflection

For V1, the quality factor is simplified:

```
quality_factor = min(1.0, reflection_notes / max(1, missions_completed))
```

- `reflection_notes` = count of reflection notes written (each `reflection.note.created` event)
- `missions_completed` = count of completed missions in the window

### 8.2 Input Events

| Event | Role |
|-------|------|
| `reflection.session.started` | Marks a reflection session |
| `reflection.note.created` | A written reflection note |
| `reflection.assessment.completed` | A self-assessment event |
| `reflection.goal.set` | A learning goal was articulated |

### 8.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = no reflection activity; 1.0 = reflection on every mission with high quality |
| Neutral default | 0.0 (no reflections → no metacognitive engagement) |

### 8.4 Limits

Clamped to `[0.0, 1.0]`. The quality factor is capped at 1.0 to prevent over-scoring from excessive note-taking.

### 8.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No reflection events at all | Return 0.0 |
| Reflections but no sessions | `total_sessions = 0`; guard with `max(1, total_sessions)`; score approaches `reflection_events / 1 × quality_factor` but limited by low missions_completed |
| Reflection on every mission, at least one note per mission | `reflection_events ≥ total_sessions`, `quality_factor ≥ 1.0` → return 1.0 |
| Many reflections but zero missions | quality_factor = 0 (zero missions), so score = 0 |
| Single session with one reflection note | Return `(1/1) × min(1.0, 1/1) = 1.0` (trivially perfect in small sample) |

### 8.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 8 (in composite calculations) |
| Version | 1 |
| Time window | Rolling 7 days |

---

## 9. Exploration Index

**Purpose:** Measures the Builder's willingness to explore new topics and domains beyond their established comfort zone. Rewards breadth and balanced topic distribution.

### 9.1 Formula

```
Exploration_Index = (unique_topics_explored / total_available_topics) × depth_balance
```

Where:

- `unique_topics_explored` = number of distinct topic tags engaged in the window
- `total_available_topics` = total number of topic tags available in the system
- `depth_balance` = evenness of engagement across explored topics

```
depth_balance = 1 - |0.5 - (missions_per_topic / avg_missions_per_topic)|
```

Where:

- `missions_per_topic` = missions completed for a given topic
- `avg_missions_per_topic` = total_missions / unique_topics_explored

The depth_balance is computed per topic, then averaged across all explored topics. A value near 1.0 indicates the Builder distributes effort evenly. A value near 0.0 indicates near-exclusive focus on a single topic.

### 9.2 Input Events

| Event | Role |
|-------|------|
| `behavior.journey.started` | Carries journey topic tags |
| `behavior.mission.completed` | Carries mission topic tags |
| Topic metadata | Defines `total_available_topics` |

### 9.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = only one topic explored; 1.0 = all topics explored evenly |
| Neutral default | 0.0 (no exploration beyond default) |

### 9.4 Limits

Clamped to `[0.0, 1.0]`. Both components naturally fall in `[0, 1]`, so the product is bounded.

### 9.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| Only one topic explored | `unique_topics_explored / total_available_topics` is low; `depth_balance` for single topic = `1 - |0.5 - 1| = 0.5`; overall score is low |
| All topics explored evenly | Both components approach 1.0 → overall approaches 1.0 |
| All topics explored but one heavily favored | Breadth is high, depth_balance penalizes → moderate score |
| No missions completed | Return 0.0 |
| Only one topic available in system | Topic ratio = 1.0, depth_balance = 1.0 → score = 1.0 (trivially perfect, system has no breadth) |

### 9.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 7 (in composite calculations) |
| Version | 1 |
| Time window | Rolling 7 days |

---

## 10. Mastery Progress

**Purpose:** Measures the Builder's overall progress toward competency mastery across all active competencies. This is the bridge between behavioral metrics and domain state.

### 10.1 Formula

```
Mastery_Progress = Σ (competency_score_i / max_score_i) / count_of_competencies
```

Where:

- `competency_score_i` = current accumulated score for competency i
- `max_score_i` = maximum achievable score for competency i (the mastery threshold)
- `count_of_competencies` = total number of competencies the Builder has unlocked or is tracking

Each competency's progress ratio is clamped to `[0.0, 1.0]` before averaging.

### 10.2 Input Events

| Event | Role |
|-------|------|
| `learning.competency.unlocked` | A new competency became active |
| `learning.competency.leveled_up` | Competency score increased |
| `learning.competency.mastered` | Competency reached maximum score |
| Competency state snapshot | Provides `competency_score_i` and `max_score_i` for all active competencies |

### 10.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = no progress on any competency; 1.0 = all competencies mastered |
| Neutral default | 0.0 (no competencies → no progress) |

### 10.4 Limits

Clamped to `[0.0, 1.0]`. Each competency's progress ratio is individually clamped before averaging.

### 10.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No competencies unlocked | Return 0.0 |
| Single competency at 50% | Return 0.5 |
| All competencies at 100% | Return 1.0 |
| Some competencies at 0%, some at 100% | Return average of extremes |
| Competency removed or deprecated | Remove from count; recompute on next event |
| `max_score_i` = 0 (should not occur) | Guard: treat progress ratio as 0 for that competency |

### 10.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 20 (in composite calculations) |
| Version | 1 |
| Time window | No window (aggregate over entire history) |
| Snapshot frequency | Recalculated on any `learning.competency.*` event |

---

## 11. Cognitive Load

**Purpose:** Estimates the mental demand on the Builder based on observable activity patterns. Higher values indicate higher cognitive load and increased risk of burnout. This metric is used inversely in composite scores — lower cognitive load is better.

### 11.1 Formula

```
Cognitive_Load = min(1.0,
  (missions_in_window × 0.3) +
  (avg_session_duration_minutes × 0.01) +
  (concurrent_missions × 0.2) -
  (break_frequency × 0.1)
)
```

Where:

- `missions_in_window` = number of missions started in the time window
- `avg_session_duration_minutes` = average duration of all sessions in the window
- `concurrent_missions` = maximum number of missions active simultaneously in the window
- `break_frequency` = number of breaks taken per hour (inverse indicator)

Break frequency reduces load:

```
break_frequency = count(recovery.pause.started) / total_hours_in_window
```

### 11.2 Input Events

| Event | Role |
|-------|------|
| `behavior.mission.started` | Contributes to missions_in_window and concurrency |
| `focus.session.started` | Marks session boundaries for duration |
| `focus.session.ended` | Marks session end for duration |
| `recovery.pause.started` | Contributes to break_frequency |

### 11.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = resting, no load; 1.0 = overloaded, burnout risk |
| Neutral default | 0.0 (no activity → no load) |

### 11.4 Limits

Clamped to `[0.0, 1.0]` via the `min(1.0, ...)` in the formula. Individual term values are not clamped independently, but the sum is capped.

### 11.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No activity at all | Return 0.0 |
| Very long session (> 100 minutes) without breaks | `avg_session_duration` term dominates; approaches 1.0 |
| Many concurrent missions | Concurrency term amplifies load |
| Frequent breaks | Break_frequency reduces load score |
| Negative computed value (breaks outweigh all other factors) | Clamp to 0.0 |
| Single short mission with breaks | Low load score |

### 11.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 10 (inverse — lower is better in composites) |
| Version | 1 |
| Time window | Rolling 7 days |

---

## 12. Mission Efficiency

**Purpose:** Measures how efficiently the Builder completes missions relative to expected durations. Values above 1.0 indicate faster-than-expected completion; values below 1.0 indicate slower-than-expected completion.

### 12.1 Formula

```
Mission_Efficiency = Σ (expected_duration_i / actual_duration_i) / n
```

Where:

- `expected_duration_i` = the expected duration for mission i (from mission metadata)
- `actual_duration_i` = the actual time taken to complete mission i
- `n` = number of completed missions in the window

Each per-mission efficiency ratio is clamped to `[0.0, 3.0]` before averaging.

### 12.2 Input Events

| Event | Role |
|-------|------|
| `behavior.mission.completed` | Carries actual duration data |
| Mission metadata | Provides `expected_duration` for each mission |

### 12.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 3.0]` |
| Interpretation | 0.0 = extremely slow; 1.0 = exactly as expected; 3.0 = extremely fast |
| Neutral default | 0.5 (no completed missions) |

### 12.4 Limits

Clamped to `[0.0, 3.0]`. The per-mission ratio is individually clamped before averaging to prevent outlier missions from dominating.

### 12.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No completed missions | Return neutral default: 0.5 |
| Exactly on expected duration for all missions | Return 1.0 |
| Extremely fast (1 minute for a 60-minute mission) | Ratio = 60/1 = 60; clamp to 3.0 |
| Extremely slow (60 minutes for a 1-minute mission) | Ratio = 1/60 ≈ 0.017; clamp to 0.0 |
| expected_duration = 0 (should not occur) | Guard: treat ratio as 1.0 (neutral) for that mission |
| actual_duration = 0 (instant completion) | Guard: use `max(1, actual_duration)` to avoid division by zero |
| Single mission completed | Return its clamped ratio |

### 12.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 5 (in composite calculations) |
| Version | 1 |
| Time window | Rolling 7 days |

---

## 13. Confidence Index

**Purpose:** Measures the Builder's confidence based on assessment performance patterns and self-evaluation trends. An upward-trending confidence index indicates growing self-assurance; erratic or declining trends may indicate uncertainty or impostor syndrome.

### 13.1 Formula

```
Confidence_Index = EMA(assessment_score_avg / max_score, previous_confidence, α=0.3)
```

Where:

- `assessment_score_avg` = average score of all assessments in the window
- `max_score` = maximum possible score for assessments (e.g., 100)
- `α` = 0.3 (moderate smoothing, favors recent assessments)

The per-window raw assessment ratio:

```
raw_confidence = assessment_score_avg / max_score
```

### 13.2 Input Events

| Event | Role |
|-------|------|
| `reflection.assessment.completed` | Carries assessment score data |
| Assessment metadata | Provides `max_score` for normalization |

### 13.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = no confidence (all assessments failed); 1.0 = full confidence (all assessments perfect) |
| Neutral default | 0.5 (no assessment data) |

### 13.4 Limits

Clamped to `[0.0, 1.0]`. The raw ratio naturally falls within this range.

### 13.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| No assessments completed | Return neutral default: 0.5 |
| Consistently high scores (e.g., 95/100) | EMA approaches ~0.95 |
| Consistently low scores (e.g., 30/100) | EMA approaches ~0.30 |
| Erratic scores (alternating 100 and 0) | EMA fluctuates; moderate average |
| First assessment (no previous_confidence) | Use raw value as initial EMA |
| Single perfect assessment | Return 1.0 (trivially, but decays if not reinforced) |
| max_score = 0 (should not occur) | Guard: treat raw ratio as 0.5 (neutral) |

### 13.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 5 (in composite calculations) |
| Version | 1 |
| α | 0.3 |
| Time window | Rolling 7 days |

---

## 14. Streak Quality

**Purpose:** Measures not just the length of a streak, but its substance. A streak with meaningful work (missions completed) scores higher than a streak with only login events. This prevents gaming the system through minimal daily engagement.

### 14.1 Formula

```
Streak_Quality = min(1.0, streak_length / 30) × content_density
```

Where:

- `streak_length` = current consecutive active days
- `content_density` = missions_completed_in_streak / streak_length

```
content_density = missions_completed_during_streak / streak_length
```

A streak with a mission completed every day has `content_density = 1.0`. A streak with no missions completed has `content_density = 0.0` (only login quality).

### 14.2 Input Events

| Event | Role |
|-------|------|
| `behavior.mission.completed` | Contributes to content_density |
| Daily activity heartbeat | Confirms active day for streak |
| Streak state | Provides `streak_length` and `missions_completed_in_streak` |

### 14.3 Output

| Property | Value |
|----------|-------|
| Range | `[0.0, 1.0]` |
| Interpretation | 0.0 = no streak or empty streak; 1.0 = 30+ day streak with daily missions |
| Neutral default | 0.0 (no streak) |

### 14.4 Limits

Clamped to `[0.0, 1.0]`. The `min(1.0, streak_length / 30)` caps the streak length contribution at 30 days. The content_density naturally falls in `[0, 1]`.

### 14.5 Edge Cases

| Condition | Behavior |
|-----------|----------|
| New streak (1 day) with 1 mission | `min(1.0, 1/30) × (1/1) = 0.033 × 1.0 ≈ 0.03` |
| 30-day streak with daily missions | `min(1.0, 30/30) × (30/30) = 1.0 × 1.0 = 1.0` |
| 30-day streak with no missions | `min(1.0, 30/30) × (0/30) = 1.0 × 0.0 = 0.0` |
| 60-day streak with daily missions | `min(1.0, 60/30) × (60/60) = 1.0 × 1.0 = 1.0` (capped at 30) |
| 15-day streak with missions every other day | `min(1.0, 15/30) × (8/15) ≈ 0.5 × 0.53 ≈ 0.27` |
| No streak (0 days) | Return 0.0 |
| streak_length = 0 (division by zero) | Guard: if streak_length = 0, return 0.0 |

### 14.6 Configuration

| Parameter | Value |
|-----------|-------|
| Weight | 5 (in composite calculations) |
| Version | 1 |
| Cap days | 30 (beyond this, streak_length term saturates at 1.0) |

---

## 15. Composite Scores

Composite scores aggregate individual behavioral metrics into higher-order indicators. Two composite scores are defined: **Engagement Score** and **Learning Health Score**.

### 15.1 Engagement Score

The Engagement Score measures the Builder's overall level of active participation and sustained involvement with the system. It combines focus, consistency, persistence, and streak quality.

```
Engagement_Score = (Focus_Score × 0.20) +
                   (Consistency × 0.25) +
                   (Persistence_Index × 0.30) +
                   (Streak_Quality × 0.25)
```

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Focus_Score | 0.20 | Quality of engagement matters, but less than persistence of engagement |
| Consistency | 0.25 | Regular attendance is foundational |
| Persistence_Index | 0.30 | Highest weight — completing what you start is the strongest engagement signal |
| Streak_Quality | 0.25 | Sustained engagement with meaningful work |

**Output Range:** `[0.0, 1.0]`

**Edge Cases:**

| Condition | Behavior |
|-----------|----------|
| No data for any component | Each returns neutral default; composite converges to ~0.375 |
| All components at maximum | Return 1.0 |
| Single component missing | Missing component returns neutral default; others weighted normally |

### 15.2 Learning Health Score

The Learning Health Score measures the overall health of the Builder's learning journey. It balances progress (velocity, mastery) against well-being (cognitive load, confidence). A high Learning Health Score indicates sustainable, effective learning.

```
Learning_Health_Score = (Learning_Velocity × 0.30) +
                        (Mastery_Progress × 0.25) +
                        (Confidence_Index × 0.15) +
                        (Reflection_Score × 0.10) +
                        ((1 - Cognitive_Load) × 0.20)
```

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Learning_Velocity | 0.30 | Speed of progress is the primary signal |
| Mastery_Progress | 0.25 | Depth of competency development |
| Confidence_Index | 0.15 | Self-assurance enables risk-taking |
| Reflection_Score | 0.10 | Metacognition amplifies learning quality |
| 1 - Cognitive_Load | 0.20 | Inverted — low load is healthy; high load is a risk signal |

**Output Range:** `[0.0, 1.0]`

**Edge Cases:**

| Condition | Behavior |
|----------|----------|
| No data for any component | Each returns neutral default; composite converges to ~0.35 |
| All components at maximum, Cognitive_Load at 0 | Return 1.0 |
| High Cognitive_Load (near 1.0) | `1 - Cognitive_Load` approaches 0, significantly reducing composite |
| Cognitive_Load = 0.5 (moderate) | `1 - 0.5 = 0.5`, weighted at 0.20 → contributes 0.10 |

### 15.3 Composite Decay

When a Builder is inactive, individual metrics decay toward their neutral defaults (defined per metric). Composite scores follow accordingly:

- After 7 days of inactivity: composites approach neutral (~0.3–0.5 depending on metric composition)
- After 30 days of inactivity: composites approach minimum neutral floor (~0.2)
- After 90 days of inactivity: composites are effectively reset to new-Builder defaults

### 15.4 Composite Versioning

Composite score formulas are versioned independently from individual metrics. When a metric's weight or definition changes, its version increments. When a composite formula changes, the composite version increments while preserving the metric versions used.

| Composite | Current Version | Last Modified |
|-----------|-----------------|---------------|
| Engagement_Score | 1 | Initial release |
| Learning_Health_Score | 1 | Initial release |

---

## 16. Edge Cases & Resilience

### 16.1 New Builder (No History)

When a Builder has no behavioral history, all metrics return their neutral defaults:

| Metric | Neutral Default | Rationale |
|--------|-----------------|-----------|
| Focus_Score | 0.5 | No data means neither good nor bad |
| Learning_Velocity | 0 | No XP earned yet |
| Recovery_Rate | 1.0 | No breaks needed |
| Persistence_Index | 0.5 | Neutral until pattern emerges |
| Consistency | 0.0 | No active days |
| Reflection_Score | 0.0 | No reflections |
| Exploration_Index | 0.0 | No topics explored |
| Mastery_Progress | 0.0 | No competencies |
| Cognitive_Load | 0.0 | No activity = no load |
| Mission_Efficiency | 0.5 | Neutral until first mission completed |
| Confidence_Index | 0.5 | No assessments = neutral confidence |
| Streak_Quality | 0.0 | No streak |

Composite scores converge to their respective neutral ranges (~0.35 for Engagement, ~0.35 for Learning Health).

### 16.2 Returning Builder (Long Absence)

After a prolonged absence (> 14 days), metrics decay:

- **EMA-based metrics** (Learning_Velocity, Recovery_Rate, Confidence_Index): The EMA continues to decay toward 0 with each empty time window. After `k` empty windows, remaining influence = `(1 - α)^k × last_value`.
- **Ratio-based metrics** (Focus_Score, Persistence_Index, Reflection_Score, Exploration_Index): All events in the window are absent; metrics return neutral defaults.
- **Aggregate metrics** (Consistency, Streak_Quality, Mission_Efficiency, Cognitive_Load): Events in the window are absent; metrics return minimum defaults.
- **Mastery_Progress**: Does not decay (competency progress is permanent). The metric remains at the last computed value, reflecting the Builder's permanent skill state.

After 30 days of inactivity, the system may mark the Builder as "dormant" and all non-permanent metrics are considered reset to neutral defaults.

### 16.3 Data Loss

If event data is partially or fully lost:

| Scenario | Behavior |
|----------|----------|
| Partial event loss within window | Metrics recompute from remaining events; neutral defaults are NOT applied for missing events |
| Complete window data loss | All metrics return neutral defaults for that window |
| Partial event loss across windows | EMA-based metrics retain previous EMA; ratio metrics use available events |
| Event store corruption | Metrics store contains last-computed values; next event triggers recomputation |
| Graceful degradation | System logs data loss event as `system.data_loss.detected` and continues with available data |

The system does not attempt to infer or impute missing data. Behavioral metrics strictly reflect observed events. If data is missing, the metric reflects the absence.

### 16.4 Boundary Conditions

| Condition | Global Behavior |
|-----------|-----------------|
| Division by zero | All divisions guarded: `x / max(epsilon, y)` where `epsilon = 0.001` |
| Overflow (very large values) | All outputs clamped to metric range |
| Underflow (very small values) | All outputs clamped to metric range |
| NaN or Infinity | Treated as missing data; metric returns neutral default |
| Negative values (where impossible) | Clamped to 0 |
| Timestamp skew (future dates) | Events with timestamps > now + 1 hour are rejected |
| Time travel (events out of order) | Events with timestamps older than the window boundary are ignored |
| Duplicate event IDs | Deduplicated by event ID; first occurrence wins |
| Window boundary crossing | Events are assigned to the window containing their timestamp, not processing time |

### 16.5 Building Resilience

All metrics are designed to be **individually resilient** — the failure or absence of one metric does not affect others. Composite scores degrade gracefully: missing components are replaced by their neutral defaults, and the composite renormalizes over the available components.

The metric computation pipeline is **stateless** with respect to external systems. Metric computation does not require:
- Network access
- External APIs
- Database connections (beyond reading events)
- Shared locks or synchronization

Each metric can be computed independently and in parallel.

### 16.6 Testing Guidelines

Each metric must be tested against the following scenarios:

| Scenario | Description |
|----------|-------------|
| Empty input | No events in window → returns neutral default |
| Single event | One event in window → returns expected value |
| Maximum input | Events at system limits → returns clamped maximum |
| Minimum input | Events at floor → returns clamped minimum |
| Boundary transition | Value exactly at boundary → within expected range |
| Monotonic increase | Repeated events with increasing values → output increases monotonically (or stays flat at max) |
| Monotonic decrease | Repeated events with decreasing values → output decreases monotonically (or stays flat at min) |
| Spike (outlier) | Single extreme event → metric reacts but does not break |
| Gap (missing data) | Gap in event stream → metric decays or returns neutral |
| Reset | Complete wipe → all metrics return neutral defaults |

---

## Appendix A: Metric Summary Table

| # | Metric | Output Range | Neutral Default | Weight | Version | Core Function |
|---|--------|-------------|-----------------|--------|---------|---------------|
| 1 | Focus_Score | [0.0, 1.0] | 0.5 | 15 | 1 | Ratio of focused to total time |
| 2 | Learning_Velocity | [0, max] | 0 | 20 | 1 | EMA of XP per hour |
| 3 | Recovery_Rate | [0.0, 1.0] | 1.0 | 10 | 1 | EMA of inverse break duration |
| 4 | Persistence_Index | [0.0, 1.0] | 0.5 | 18 | 1 | Completion ratio × retry bonus |
| 5 | Consistency | [0.0, 1.0] | 0.0 | 12 | 1 | Active days × streak bonus |
| 6 | Reflection_Score | [0.0, 1.0] | 0.0 | 8 | 1 | Reflection ratio × quality |
| 7 | Exploration_Index | [0.0, 1.0] | 0.0 | 7 | 1 | Topic breadth × depth balance |
| 8 | Mastery_Progress | [0.0, 1.0] | 0.0 | 20 | 1 | Average competency completion |
| 9 | Cognitive_Load | [0.0, 1.0] | 0.0 | 10i | 1 | Multi-factor load estimation |
| 10 | Mission_Efficiency | [0.0, 3.0] | 0.5 | 5 | 1 | Expected/actual duration ratio |
| 11 | Confidence_Index | [0.0, 1.0] | 0.5 | 5 | 1 | EMA of assessment scores |
| 12 | Streak_Quality | [0.0, 1.0] | 0.0 | 5 | 1 | Streak length × content density |

*Note: Weight marked with `i` (Cognitive_Load = 10i) indicates inverse weight — lower values are better in composite scores.*

---

## Appendix B: Event-to-Metric Mapping

| Event | Metrics Consumed |
|-------|------------------|
| `focus.mode.entered` | Focus_Score |
| `focus.mode.exited` | Focus_Score |
| `focus.flow.lost` | Focus_Score |
| `focus.session.started` | Cognitive_Load |
| `focus.session.ended` | Cognitive_Load |
| `recovery.pause.started` | Recovery_Rate, Cognitive_Load |
| `recovery.pause.ended` | Recovery_Rate |
| `recovery.resume.after_absence` | Recovery_Rate |
| `behavior.mission.started` | Persistence_Index, Cognitive_Load, Exploration_Index |
| `behavior.mission.completed` | Learning_Velocity, Persistence_Index, Exploration_Index, Mission_Efficiency, Streak_Quality, Reflection_Score |
| `behavior.mission.abandoned` | Persistence_Index |
| `behavior.mission.retried` | Persistence_Index |
| `behavior.journey.started` | Exploration_Index |
| `reflection.session.started` | Reflection_Score |
| `reflection.note.created` | Reflection_Score |
| `reflection.assessment.completed` | Confidence_Index |
| `reflection.goal.set` | Reflection_Score |
| `learning.competency.unlocked` | Learning_Velocity, Mastery_Progress |
| `learning.competency.leveled_up` | Mastery_Progress |
| `learning.competency.mastered` | Mastery_Progress |
| Any `behavior.*` event | Consistency, Streak_Quality |

---

## Appendix C: Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-21 | Chief Architect | Initial release — 12 behavioral metrics, 2 composite scores, resilience framework |
