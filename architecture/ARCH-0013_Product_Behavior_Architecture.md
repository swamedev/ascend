# ARCH-0013 — Product Behavior Architecture

| Field | Value |
|-------|-------|
| **ID** | ARCH-0013 |
| **Name** | Product Behavior Architecture |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | ARCH-0011 Experience Layer, UI-0002 Builder Journey, DOC-0003 First Principles |
| **Referenced by** | ARCH-0014 Ascension Ring, Frontend Implementation |

---

## 1. Purpose

This document defines how ASCEND behaves **over time** — not just how screens look, but how the product responds to the Builder across days, weeks, months, and years.

It is the bridge between **interface design** and **product behavior**.

---

## 2. Behavioral Philosophy

> *ASCEND does not entertain. It evolves.*

| Principle | Statement |
|-----------|-----------|
| **Competence over dopamine** | Motivation comes from proven growth, not empty rewards |
| **Respect over retention** | Never use dark patterns to keep the Builder engaged |
| **Pacing over grinding** | The system respects the Builder's life, schedule, and limits |
| **Autonomy over dependency** | The goal is to make the Mentor unnecessary over time |

---

## 3. Time Loops

### 3.1 Daily Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY LOOP                                │
│                                                              │
│  Open ASCEND                                                 │
│       │                                                      │
│       ▼                                                      │
│  Dashboard loads                                              │
│       │                                                      │
│       ├── Mission active? ───► Resume Mission                │
│       │                          │                          │
│       │                          ▼                          │
│       │                    Focus Mode                        │
│       │                          │                          │
│       │                          ▼                          │
│       │                    Complete / Submit Evidence         │
│       │                          │                          │
│       │                          ▼                          │
│       │                    XP + Progress update               │
│       │                          │                          │
│       │                          ▼                          │
│       │                    Feedback (if reviewed)            │
│       │                                                      │
│       └── No mission? ───► Suggested Next Mission            │
│                              │                              │
│                              ▼                              │
│                        Quick start (≤30min)                 │
│                              │                              │
│                              ▼                              │
│                        XP + Streak maintained               │
│                                                              │
│  Close satisfied                                             │
└─────────────────────────────────────────────────────────────┘
```

**Duration target:** 15–45 minutes per session.

**Emotional arc:** Entry → Focus → Accomplishment → Satisfaction.

### 3.2 Weekly Loop

The weekly loop is driven by the **Sunday Summary** — a gentle, non-intrusive report.

```
┌─────────────────────────────────────────────────────────────┐
│                   WEEKLY LOOP                                │
│                                                              │
│  Monday–Saturday: Daily Loops                                │
│       │                                                      │
│       ▼                                                      │
│  Sunday: Weekly Summary                                      │
│       │                                                      │
│       ▼                                                      │
│  ┌─ Weekly Report ───────────────────────────────────────┐  │
│  │                                                       │  │
│  │  📊 This Week                                         │  │
│  │  • 5 missions completed (+450 XP)                     │  │
│  │  • 2 competencies advanced                            │  │
│  │  • 1 new badge earned                                 │  │
│  │  • 7-day streak maintained 🔥                         │  │
│  │                                                       │  │
│  │  📈 Learning Velocity: 350 XP/week (vs 320 last week) │  │
│  │                                                       │  │
│  │  🎯 Next Week Suggestions:                            │  │
│  │  • Mission 5: Network Configuration                   │  │
│  │  • Challenge: Boss Fight preparation                  │  │
│  │                                                       │  │
│  │  [View Full Report]  [Dismiss]                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key behaviors:**
- Report appears Monday morning (not Sunday night — avoid Sunday scaries)
- Always shows comparison to *self*, never to others
- Suggests, never demands
- Can be dismissed permanently if the Builder prefers

### 3.3 Monthly Loop

```
┌─────────────────────────────────────────────────────────────┐
│                   MONTHLY LOOP                               │
│                                                              │
│  First day of the month                                      │
│       │                                                      │
│       ▼                                                      │
│  ┌─ Monthly Review ──────────────────────────────────────┐   │
│  │                                                       │   │
│  │  📊 Month in Review                                   │   │
│  │                                                       │   │
│  │  • 22 missions completed (+2,100 XP)                  │   │
│  │  • 3 competencies leveled up                          │   │
│  │  • 5 badges earned                                    │   │
│  │  • Average session: 32 min                            │   │
│  │  • Consistency: 26/30 days active                     │   │
│  │                                                       │   │
│  │  🧠 Competency Growth:                                │   │
│  │  ┌────────────────────────────────────┐               │   │
│  │  │ File Mgmt    L2 ▓▓▓▓▓▓▓ 100% ▲     │               │   │
│  │  │ User Admin   L1 ▓▓▓▓░░  45%  ▲▲    │               │   │
│  │  │ Network      L0 ░░░░░░   0%        │               │   │
│  │  └────────────────────────────────────┘               │   │
│  │                                                       │   │
│  │  🏆 Milestones:                                       │   │
│  │  • 100th mission completed                            │   │
│  │  • 5,000 total XP                                     │   │
│  │                                                       │   │
│  │  [View Full Report]  [Share Progress]                 │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Key behaviors:**
- Compare only against the Builder's own previous month
- Celebrate milestones explicitly
- Never show leaderboard position in the monthly report

### 3.4 Long-Term Loop

The long-term loop defines how the experience evolves across the Builder's entire journey.

```
┌─────────────────────────────────────────────────────────────┐
│                  LONG-TERM EVOLUTION                         │
│                                                              │
│  0–100 hours (Discovery)                                     │
│  ├── Onboarding complete                                     │
│  ├── First competency earned                                 │
│  ├── First certificate                                       │
│  ├── System feels guided, hand-holdy                         │
│  └── Mentor is proactive, frequent tips                      │
│                                                              │
│  100–300 hours (Growth)                                      │
│  ├── Multiple competencies in progress                       │
│  ├── Independent workflow established                        │
│  ├── Focus Mode is natural                                   │
│  ├── Less hand-holding, more autonomy                        │
│  └── Mentor shifts to Socratic questioning                   │
│                                                              │
│  300–1000 hours (Mastery)                                    │
│  ├── Deep specialization in chosen areas                     │
│  ├── Creating original projects                              │
│  ├── Reviewing other Builders' work                          │
│  ├── Mentor becomes peer-like                                │
│  └── System recedes — Builder owns the journey               │
│                                                              │
│  1000–5000 hours (Sovereignty)                               │
│  ├── Builder becomes Mentor                                  │
│  ├── Creating packages for others                            │
│  ├── Leading community initiatives                           │
│  ├── ASCEND is a tool, not a guide                           │
│  └── Mentor is rarely needed                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Motivation Engine

### 4.1 Design Principles

| Principle | Application |
|-----------|-------------|
| **Competence-based** | Motivation comes from seeing proven growth, not artificial streaks |
| **Self-referential** | Compare only against the Builder's past self |
| **Transparent** | Every metric is explainable and attributable |
| **Respectful** | No urgency, no FOMO, no "you'll lose your streak" anxiety |
| **Optional** | Every motivation mechanism can be disabled |

### 4.2 Motivation Mechanisms

| Mechanism | How it works | When it activates |
|-----------|--------------|-------------------|
| **Streak** | Consecutive days with at least one mission | Daily |
| **XP** | Experience points for completed work | Per mission |
| **Level** | Every N XP unlocks a new level | Periodic |
| **Badge** | Milestone achievements | Milestone reached |
| **Certificate** | Formal competency recognition | Competency mastered |
| **Title** | Progression titles (Apprentice → Master) | Level milestones |
| **Competency growth** | Visual tree fill | Per skill advance |
| **Learning velocity** | XP/week trend | Weekly |
| **Personal record** | Best weekly/monthly performance | Weekly/monthly |

### 4.3 Non-Mechanisms

These are **explicitly excluded**:

| Excluded | Reason |
|----------|--------|
| Leaderboard anxiety | Comparison is self-referential only |
| Countdown timers | Artificial urgency creates stress |
| "Losing" progress | Progress is permanent |
| Pay-to-accelerate | ASCEND is not a game |
| Random rewards | Every reward is earned, not gambled |
| Social pressure | Community is supportive, not competitive |

---

## 5. Progression Engine

### 5.1 XP System

| Action | Base XP | Quality Bonus | Max |
|--------|---------|---------------|-----|
| Mission complete | 100 | Up to +50 for quality evidence | 150 |
| Boss fight | 500 | Up to +250 | 750 |
| Quick mission | 25 | None | 25 |
| Peer review | 75 | None | 75 |
| Package creation | 200 | Up to +200 | 400 |
| Community contribution | 100 | Up to +100 | 200 |

### 5.2 Level Thresholds

| Level | Title | XP Required | Cumulative XP |
|-------|-------|-------------|---------------|
| 1 | Explorer | 0 | 0 |
| 2 | Apprentice | 300 | 300 |
| 3 | Practitioner | 700 | 1,000 |
| 4 | Specialist | 1,500 | 2,500 |
| 5 | Expert | 3,000 | 5,500 |
| 6 | Mentor | 5,000 | 10,500 |
| 7 | Leader | 8,000 | 18,500 |
| 8 | Master | 12,000 | 30,500 |
| 9 | Sage | 20,000 | 50,500 |
| 10 | Architect | 30,000 | 80,500 |

### 5.3 Competency Levels

| Level | Label | Criteria |
|-------|-------|----------|
| L0 | Untracked | No evidence submitted |
| L1 | Novice | 1–3 missions completed |
| L2 | Developing | 4–6 missions, basic proficiency |
| L3 | Proficient | 7–10 missions, consistent quality |
| L4 | Advanced | 11–15 missions, complex scenarios |
| L5 | Distinguished | 15+ missions, original projects |

### 5.4 Title System

Titles are **earned, not assigned**. They reflect the Builder's level.

| Level Range | Title | Visual |
|-------------|-------|--------|
| 1–2 | Explorer | 🥉 Bronze border |
| 3–4 | Apprentice | 🥈 Silver border |
| 5–6 | Practitioner | 🥇 Gold border |
| 7–8 | Specialist | 💎 Diamond border |
| 9–10 | Master | 👑 Crown border |

---

## 6. Failure Recovery

### 6.1 What "Failure" Means

Failure is not a judgment. It is **a break in the learning pattern**.

| Scenario | Classification |
|----------|---------------|
| 3 days inactive | Micro-break |
| 7 days inactive | Short break |
| 30 days inactive | Extended break |
| 90 days inactive | Hiatus |
| 180+ days inactive | Return |

### 6.2 Recovery Protocol

```
3 days:
  └── No action. Streak resets silently.

7 days:
  └── Gentle push notification:
      "Your progress is waiting. No pressure — just pick one mission."

30 days:
  └── Email (if enabled):
      "It's been a month. Here's a summary of what you achieved.
       Your competencies are exactly where you left them."
  └── Upon return:
      - Show "Welcome back" screen with last state
      - No guilt. No "you lost X". Just continuation.
      - Suggested: one quick mission (15 min) to rebuild momentum

90 days:
  └── Email: personal check-in
  └── Upon return:
      - Full "Where you left off" summary
      - Option to review past evidence
      - Mentor: "Welcome back. Want a quick refresher?"

180+ days:
  └── Upon return:
      - Optional re-onboarding (can skip)
      - All progress preserved
      - Mentor: "Good to see you. Want to continue or start fresh?"
```

### 6.3 Emotional Design for Return

The system must **never** make the Builder feel guilty for leaving.

| Bad approach | Good approach |
|-------------|---------------|
| "You lost your 30-day streak" | "Welcome back. Your progress is waiting." |
| "You're behind schedule" | "Start where you left off, at your own pace." |
| "Only X% of users return" | No social comparison on return. |

---

## 7. Notification Philosophy

### 7.1 When to Notify

| Event | Channel | Timing | Priority |
|-------|---------|--------|----------|
| Review completed | Push (in-app) | Immediate | High |
| Achievement unlocked | Push | Immediate | High |
| Level up | Push | Immediate | Medium |
| Streak milestone | Push | Morning of milestone | Low |
| Weekly summary | Push | Monday 8AM | Low |
| Monthly summary | Push | 1st of month 8AM | Low |
| Mentor suggestion | Push | When relevant | Medium |
| Inactivity (3d) | Push | Evening | Low |
| Inactivity (7d) | Push | Evening | Low |
| Inactivity (30d) | Email | Morning | Low |

### 7.2 When NOT to Notify

| Situation | Why |
|-----------|-----|
| During Focus Mode | Never interrupt flow |
| Between midnight and 6AM | Respect sleep |
| After 2 notifications in 1 hour | Rate limit |
| Builder has DND enabled | Explicit preference |
| Right after an error | Let the Builder recover |
| During evidence upload | Do not distract |

### 7.3 Notification Principles

| Principle | Description |
|-----------|-------------|
| **Respectful** | Notifications are suggestions, not demands |
| **Rate-limited** | Max 3 push notifications per day |
| **Actionable** | Every notification offers a clear next step |
| **Silence is golden** | No news is good news |
| **Opt-out** | Every notification category can be disabled |
| **Context-aware** | No notifications during Focus Mode, sleep hours, or DND |

---

## 8. Learning Velocity

### 8.1 Definition

Learning Velocity is the **rate of XP earned per active week**.

```
Learning Velocity = Total XP / Active Weeks
```

An "active week" is a week with at least one mission completed.

### 8.2 Display

```
📈 Learning Velocity
350 XP/week
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░   vs last month (+12%)
```

### 8.3 Guardrails

| Rule | Reason |
|------|--------|
| Never compare velocity between Builders | Prevents unhealthy competition |
| Velocity is always trended, not absolute | Context matters |
| Velocity can decrease — and that's OK | Plateaus are part of learning |
| No rewards for high velocity | Quality over quantity |

---

## 9. Burnout Prevention

### 9.1 Detection

The system monitors these signals:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Missions/day > 5 | 3 consecutive days | Gentle suggestion: "You're on fire! Remember to rest." |
| Session time > 3h | Single session | "You've been at it for 3 hours. Want to save and continue tomorrow?" |
| 7 consecutive days active | Streak of 7 | Encouragement, not pressure |
| Resubmitting same evidence | 3+ times | Mentor offers help instead of letting Builder spin |

### 9.2 Active Prevention

| Mechanism | How it works |
|-----------|--------------|
| **Rest reminders** | After 2h of continuous Focus Mode, suggest a break |
| **No grinding incentives** | No bonus XP for consecutive hours |
| **Quality gate** | Rushing missions produces lower quality scores |
| **Mentor intervention** | Mentor notices patterns: "You've done 6 missions today. Quality matters more than quantity." |

---

## 10. AI Mentor Behavior Over Time

### 10.1 Behavioral Phases

```
Discovery Phase (0–100h):
  ├── Mentor is proactive, talkative
  ├── Offers tips before being asked
  ├── Explains concepts in detail
  └── Frequency: every 2–3 missions

Growth Phase (100–300h):
  ├── Mentor shifts to Socratic method
  ├── "Why did you choose that approach?"
  ├── Fewer direct answers, more questions
  └── Frequency: every 4–5 missions

Mastery Phase (300–1000h):
  ├── Mentor is peer-like
  ├── Offers challenges, not solutions
  ├── Debates technical decisions
  └── Frequency: on request mostly

Sovereignty Phase (1000h+):
  ├── Mentor is a thinking partner
  ├── Rarely initiates conversation
  ├── Responds when asked
  └── Focused on meta-growth: teaching others, creating packages
```

### 10.2 Intervention Rules

| Situation | Does the Mentor speak? |
|-----------|----------------------|
| Builder is actively working | Silent |
| Builder is stuck >10min | Gentle nudge |
| Builder repeats the same mistake | Offers targeted help |
| Builder achieves something significant | Brief congratulations |
| Builder is inactive >3 days | Encouraging message |
| Builder is grinding (>5 missions/day) | Quality reminder |
| Builder is in Focus Mode | Silent unless called |

---

## 11. Focus Philosophy

### 11.1 Definition

Focus Mode is **not a feature**. It is a **philosophy of respect for the Builder's attention**.

### 11.2 Principles

| Principle | Description |
|-----------|-------------|
| **Undivided attention** | When in Focus Mode, the system disappears |
| **No notifications** | All alerts are suppressed |
| **No navigation** | Sidebar and menus are hidden |
| **Mentor is dormant** | Only available if explicitly called |
| **Timer is optional** | Can be disabled if distracting |
| **Exit is one click** | Never trap the Builder |

### 11.3 When Focus Mode Activates

| Trigger | Behavior |
|---------|----------|
| User clicks "Start Mission" | Auto-activates |
| User clicks "Focus Mode" toggle | Manual activation |
| User is >5min in a mission | Suggestion appears: "Enter Focus Mode?" |
| System detects deep work | Gentle proposal (non-intrusive) |

---

## 12. Behavioral Invariants

These rules **cannot be violated** by any product behavior:

| Invariant | Statement |
|-----------|-----------|
| **B-1** | Never use artificial urgency to drive engagement |
| **B-2** | Never compare Builder to others without explicit consent |
| **B-3** | Never lose Builder progress or data |
| **B-4** | Never interrupt Focus Mode (except system emergency) |
| **B-5** | Never notify between midnight and 6AM |
| **B-6** | Never force the Builder to see content they've dismissed |
| **B-7** | Never reward quantity over quality |

---

## 13. Definition of Done

ARCH-0013 aprovado quando:

- [ ] Daily loop documented with diagram
- [ ] Weekly loop documented with report spec
- [ ] Monthly loop documented with review spec
- [ ] Long-term evolution mapped (100h to 5000h)
- [ ] Motivation Engine defined (mechanisms + non-mechanisms)
- [ ] Progression Engine defined (XP, levels, titles, competencies)
- [ ] Failure Recovery documented (3d to 180d+)
- [ ] Notification Philosophy defined (when/when not)
- [ ] Learning Velocity defined with guardrails
- [ ] Burnout Prevention documented
- [ ] AI Mentor Behavior phased over time
- [ ] Focus Philosophy codified
- [ ] Behavioral Invariants established

---

## 14. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
