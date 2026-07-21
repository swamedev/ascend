# WF-0008 — AI Mentor

| Campo | Valor |
|-------|-------|
| **ID** | WF-0008 |
| **Nome** | AI Mentor |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, ARCH-0004, UI-0001, UI-0002 |
| **Será utilizado por** | Frontend Sprint 4 |

---

## 1. Propósito

O AI Mentor é a interface entre o Builder e o Mentor Agent do Core Engine.

**Princípio fundamental:** O Mentor NÃO é um chat.

É um **painel lateral permanente** que:

- Observa o progresso do Builder silenciosamente
- Intervém apenas quando tem algo relevante a dizer
- Jamais responde tudo — sempre ensina
- Sugere, não resolve
- Pergunta, não afirma

---

## 2. Filosofia de Design

| Princípio | Descrição |
|-----------|-----------|
| **Observador silencioso** | O Mentor fica visível mas não interfere |
| **Intervenção contextual** | Aparece apenas quando relevante |
| **Ensina a pescar** | Dá direções, não respostas prontas |
| **Progresso como base** | Sugestões baseadas no que o Builder já fez |
| **Tom Socrático** | Perguntas > Respostas |

### Tom do Mentor

| Característica | Tom |
|----------------|-----|
| Profissional | Sim, como um líder técnico |
| Amigável | Sim, mas sem forçar |
| Direto | Sim, sem rodeios |
| Paciente | Sim, sempre |
| Motivador | Sim, mas sem exageros |

---

## 3. Wireframe Desktop — Painel Lateral

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Linux Basics  >  Mission 4                        │
│ ┌──────┬──────────────────────────────────────┬────────────────┐ │
│ │      │  (Mission Workspace Content)          │ 🤖 AI Mentor   │ │
│ │      │                                       │                │ │
│ │      │                                       │ 🟢 Online      │ │
│ │      │                                       │                │ │
│ │      │                                       │ ┌─ Suggestion┐ │ │
│ │      │                                       │ │ 💡 Based on │ │ │
│ │      │                                       │ │ your recent │ │ │
│ │      │                                       │ │ progress in │ │ │
│ │      │                                       │ │ Linux, try  │ │ │
│ │      │                                       │ │ using -m    │ │ │
│ │      │                                       │ │ flag with   │ │ │
│ │      │                                       │ │ useradd     │ │ │
│ │      │                                       │ └────────────┘ │ │
│ │      │                                       │                │ │
│ │      │                                       │ ┌─ Quick ────┐ │ │
│ │      │                                       │ │ 🎯 Suggest │ │ │
│ │      │                                       │ │    next    │ │ │
│ │      │                                       │ │    mission │ │ │
│ │      │                                       │ │ 📚 Explain  │ │ │
│ │      │                                       │ │    concept │ │ │
│ │      │                                       │ │ 🔍 Review  │ │ │
│ │      │                                       │ │    my work │ │ │
│ │      │                                       │ └────────────┘ │ │
│ │      │                                       │                │ │
│ │      │                                       │ ┌─ Context ──┐ │ │
│ │      │                                       │ │ You're on   │ │ │
│ │      │                                       │ │ Mission 4   │ │ │
│ │      │                                       │ │ of Linux    │ │ │
│ │      │                                       │ │ Journey.    │ │ │
│ │      │                                       │ │ 65% done.   │ │ │
│ │      │                                       │ └────────────┘ │ │
│ │      │                                       │                │ │
│ │      │                                       │ [💬 Ask Mentor]│ │
│ └──────┴──────────────────────────────────────┴────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Painel Expandido

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  AI Mentor                                          │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │                                                      │ │
│ │      │  ← Back                                           🤖 │ │
│ │      │                                                      │ │
│ │      │  AI Mentor                                           │ │
│ │      │  ────────────────────────────────────────────        │ │
│ │      │                                                      │ │
│ │      │  ┌─ Messages ─────────────────────────────────────┐ │ │
│ │      │  │                                                  │ │
│ │      │  │ 🤖 Mentor: Hello! I see you're working on       │ │ │
│ │      │  │   Linux User Management. How can I help?        │ │ │
│ │      │  │                                                  │ │
│ │      │  │ 🙋 You: What's the difference between useradd   │ │ │
│ │      │  │   and adduser?                                  │ │ │
│ │      │  │                                                  │ │
│ │      │  │ 🤖 Mentor: Great question.                      │ │ │
│ │      │  │   useradd is the low-level binary.              │ │ │
│ │      │  │   adduser is a Perl script that uses            │ │ │
│ │      │  │   useradd with interactive prompts.             │ │ │
│ │      │  │                                                  │ │
│ │      │  │   For scripting, prefer useradd.                │ │ │
│ │      │  │   For interactive, adduser is friendlier.       │ │ │
│ │      │  │                                                  │ │
│ │      │  │   💡 Try: man useradd to see all flags          │ │ │
│ │      │  └──────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │  ┌─ Quick Actions ────────────────────────────────┐  │ │
│ │      │  │  🎯 Suggest my next mission                    │ │ │
│ │      │  │  📚 Explain Linux permissions                  │ │ │
│ │      │  │  🔍 Review my evidence draft                   │ │ │
│ │      │  │  🗺️ Show my career path                        │ │ │
│ │      │  │  💡 Give me a study tip                        │ │ │
│ │      │  └──────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │  ┌────────────────────────────────────────────┐      │ │
│ │      │  │ Type your question...                   ➤  │      │ │
│ │      │  └────────────────────────────────────────────┘      │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Mentor Suggestion Types

### 5.1 Contextual Tip

```
💡 Based on your progress in Linux Mission 4,
try using the -m flag with useradd to
automatically create the home directory.

[Dismiss] [Ask More]
```

### 5.2 Progress Insight

```
📊 You've completed 4/12 Linux missions.
Your file management skills are strong (L3).
Next growth area: User Administration (L1).

Ready to tackle Mission 5?
[View Mission] [Dismiss]
```

### 5.3 Streak Encouragement

```
🔥 7-day streak! Consistency is the #1
predictor of skill development.
Keep going — Level 6 is within reach.

[View Progress] [Dismiss]
```

### 5.4 Intervention

```
💡 I noticed you're resubmitting evidence.
Common issue: missing documentation.

Try adding a brief explanation of each
command and its expected output.

[Show Example] [Dismiss]
```

---

## 6. Mentor Panel Layout

### 6.1 Default (collapsed)

```
┌────┐
│ 🤖 │
│ 🟢 │
└────┘
```

### 6.2 Expanded (com sugestão)

```
┌────────────────────┐
│ 🤖 AI Mentor  🟢   │
│                    │
│ 💡 Dica rápida...  │
│                    │
│ ┌─ Quick ───────┐  │
│ │ 🎯 Suggest    │  │
│ │ 📚 Explain    │  │
│ └──────────────┘  │
│                    │
│ [💬 Ask Mentor]   │
└────────────────────┘
```

---

## 7. Wireframe Tablet (768px)

```
┌──────────────────────────────────────────────┐
│ 🔷 Mission 4                     🤖 [Mentor] │
├──────────────────────────────────────────────┤
│                                                │
│ (Mission Workspace content)                    │
│                                                │
├──────────────────────────────────────────────┤
│ [💬 Ask Mentor]   (floating button)           │
└──────────────────────────────────────────────┘
```

---

## 8. Wireframe Mobile (<768px)

```
┌──────────────────────────┐
│ 🔷 Mission 4             │
│                          │
│ (Mission content)        │
│                          │
├──────────────────────────┤
│      🤖 [Ask Mentor]     │
└──────────────────────────┘
```

---

## 9. Mentor Behavior Rules

### 9.1 Intervention Frequency

| Builder Activity | Mentor Behavior |
|-----------------|-----------------|
| Browsing | Silent (no suggestions) |
| On mission >5min | One contextual tip |
| Stuck >10min | Gentle intervention |
| Submitted evidence | Wait for review result |
| Received feedback | Comment on feedback |
| Level up | Congratulate + suggest next |
| Inactive >24h | Encouraging message |
| Streak active | Periodic encouragement |

### 9.2 When NOT to Intervene

- During Focus Mode (unless called)
- While reading rubric
- During evidence upload
- Right after an error (let the Builder try again first)

### 9.3 Message Length

| Type | Max length |
|------|------------|
| Tip | 3 lines |
| Suggestion | 5 lines |
| Explanation | 10 lines |
| Encouragement | 3 lines |

---

## 10. States

| State | Visual |
|-------|--------|
| **Idle (online)** | 🤖 🟢 Ready |
| **Thinking** | 🤖 ⏳ Thinking... + typing indicator |
| **Suggestion** | 💡 card with tip |
| **Conversation** | Chat messages |
| **Offline** | 🤖 🔴 Mentor unavailable |
| **Error** | Could not reach mentor + [Retry] |

---

## 11. Motion Timeline

| Component | Animation | Duration | Delay |
|-----------|-----------|----------|-------|
| Panel slide-in | slide-left | 300ms | 0 |
| Suggestion card | slide-down | 300ms | 200ms |
| Messages | slide-up new message | 200ms | per message |
| Typing indicator | pulse dots | 1s loop | — |
| Button hover | scale(1.02) | 150ms | 0 |

---

## 12. Definition of Done

WF-0008 aprovado quando:

- [ ] Filosofia de design documentada (Mentor não é chat)
- [ ] Tom do Mentor definido
- [ ] Wireframe Desktop — painel lateral completo
- [ ] Painel expandido (conversação) documentado
- [ ] Tipos de sugestão (contextual, insight, encouragement, intervention)
- [ ] Layout do painel (collapsed, expanded, conversation)
- [ ] Wireframe Tablet completo
- [ ] Wireframe Mobile completo
- [ ] Mentor Behavior Rules (frequência, quando não intervir, tamanho)
- [ ] Estados documentados
- [ ] Motion timeline completa

---

## Status

**WF-0008 — AI Mentor**

- Estado: ✅ Completo
- Próximo: WF-0009 — Command Palette
