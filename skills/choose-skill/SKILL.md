---
name: choose-skill
description: Triage EVERY request by complexity first, then route to the lightest flow that is sufficient — do trivial work directly, use a single Matt-Pocock skill for focused work, and for large/multi-session work pick between Matt's ticket-driven flow and Superpowers' full flow by the shape of the work. Small work never enters Superpowers; large work may. Use this before invoking any other engineering skill.
---

# choose-skill — complexity triage & routing

The default failure mode here is **over-process**: reaching for `brainstorming` -> `writing-plans` -> `subagent-driven-development` on work that needed one edit. choose-skill fixes that. Before invoking any other skill, classify the request into one tier and route to the **lightest flow that is sufficient**. Matt-Pocock skills are the default at L1 and L2; Superpowers enters only at L3, and even there as one of two equal options — never the reflexive default.

**Bias down.** When torn between two tiers, pick the lower one. You can always escalate mid-task if reality proves heavier; you cannot cheaply refund tokens already burned on ceremony.

**Tiering is dynamic, not a one-shot label.** The initial request often lacks the information to tier confidently — real complexity only surfaces as the work is clarified. Two rules follow:

1. **Can't tier yet => it is NOT L1.** L1 requires an obvious, fully-specified change. If a request is too vague to place (e.g. "optimize this module", "make auth better"), that vagueness is itself the signal: route to an L2 *clarifying* entry first — `grill-me` (sharpen the goal), `research` (gather missing facts), `prototype` (settle a shape), or `domain-modeling` (fix the vocabulary) — **without touching code**. Re-tier once the goal is clear.
2. **Re-tier whenever new complexity appears.** Don't treat the first announced tier as final. Whenever the conversation exposes a heavier reality — the change now spans more files, several design decisions open up, "actually we also need X" — **stop and re-announce**: `choose-skill: L2 -> L3 — {reason}`. Escalating to L3 still requires the confirm-first step.

## Step 1 — announce the tier

Before acting, state one line: `choose-skill: L{n} — {≤10-word reason}`. This makes the routing visible and correctable — the user can override ("no, do it properly" / "just fix it") in one word.

If the request is too vague to tier, do NOT default to L1. Announce the clarifying route instead — e.g. `choose-skill: L2 (clarify) — goal underspecified, grilling first` — then re-tier once the goal is clear (see **Tiering is dynamic** above).

## Step 2 — route

### L1 · Do it directly (no skill)
One obvious change, or a question with a knowable answer.
- typo, rename, config value, one-line fix, add a log line
- a factual/where-is-X/how-does-X-work question
- any change fully specified and confined to a single spot

-> Just do it. Do **not** invoke brainstorming, plans, or subagents.

### L2 · One focused skill (Matt-Pocock set — lightweight)
A single concern, roughly ≤3 files, goal already clear enough. Invoke skills **one at a time, stopping after each** for the user to confirm the next hop.

**Step A — pick the ENTRY skill by intent.** Match the request to a row; the "Then" column is the pre-arranged chain so the user never has to ask "what now". Each `->` is a manual, confirmed hop. A `(U)` prefix marks a **user-only** skill: the model cannot auto-invoke it — instead tell the user `Run /<skill> to continue` and wait. Legend: `(U)` = user-only (model prints the `/command` and waits); bare name = model auto-invokes via the Skill tool.

| The request is… | Enter at | Then (pre-arranged chain) |
|---|---|---|
| A feature, and it's already clear what's wanted | `tdd` (or (U)`implement` if no tests) | -> `code-review` |
| A feature, but not fully pinned down | (U)`grill-me` | -> (U)`to-spec` -> (U)`implement`/`tdd` -> `code-review` |
| A feature already discussed in this chat | (U)`to-spec` | -> (U)`implement`/`tdd` -> `code-review` |
| A bug / crash / perf regression | `diagnosing-bugs` | -> `tdd` (failing test -> fix to green) -> `code-review` |
| Unsure how to model it (state/UI) | `prototype` | -> back to (U)`to-spec` once the shape is clear |
| Unsure of the domain terms | `domain-modeling` | -> (U)`to-spec` |
| A module's interface/seam feels wrong | `codebase-design` | -> `tdd`/(U)`implement` -> `code-review` |
| Need facts/docs/APIs first | `research` | -> back to the matching row above |
| Reviewing existing changes | `code-review` | done |
| A merge/rebase conflict | `resolving-merge-conflicts` | done |
| Big enough to need tickets | (U)`to-spec` -> (U)`to-tickets` | -> (U)`implement` per ticket -> `code-review` |
| Teach a concept | (U)`teach` | done |
| Hand off this conversation | (U)`handoff` | done |

**Step B — if no row fits, or two seem equally right:** `ask-matt` is the router, but it is user-only `(U)` — so tell the user `Not sure which fits — run /ask-matt to route` rather than guessing or auto-invoking it.

**User-only skills `(U)`** (`to-spec`, `to-tickets`, `implement`, `grill-me`, `grill-with-docs`, `teach`, `handoff`, `ask-matt`, `wayfinder`, `improve-codebase-architecture`) can only be triggered by the user typing `/<name>`. When routing lands on one, do NOT pretend to invoke it — announce the tier/next step and print the exact `/command` for the user to run. Auto-invokable entries (`tdd`, `diagnosing-bugs`, `prototype`, `domain-modeling`, `codebase-design`, `research`, `code-review`, `resolving-merge-conflicts`) you invoke directly via the Skill tool.

**Small-request shortcut:** the smaller the task, the more hops to skip. Clear single-file change -> skip spec entirely, go straight to `tdd`/`implement` -> `code-review`. If it's a one-liner/typo/config, it's L1, not L2 — just do it.

If two L2 skills apply in sequence (e.g. `to-spec` then `implement`), run them one at a time — that is still L2, not L3.

### Overlapping skills — L1/L2 default to Matt, L3 may use either
Several Matt and Superpowers skills do the same job. At L1/L2, default to the Matt one — Superpowers stays out of the light tiers. At L3, either side may serve depending on the shape of the work.

| Job | L1/L2 default (Matt) | Superpowers equivalent (L3 option) |
|---|---|---|
| Test-first loop | `tdd` | `test-driven-development` |
| Diagnose a bug | `diagnosing-bugs` | `systematic-debugging` |
| Review changes | `code-review` | `requesting-code-review` |
| Interview to sharpen a plan | `(U)grill-me` | `brainstorming` |

Not overlapping — complementary, can be used in sequence: `(U)to-spec` (WHAT/why, -> tracker) then, in L3, Superpowers `writing-plans` (HOW, code-level -> repo) if you picked the Superpowers flow.

### After every L2 skill: signpost the next step
Matt-Pocock skills are discrete steps that STOP when done — they never auto-chain into implementation/tests/review. So on finishing any L2 skill, do NOT go silent and do NOT auto-continue. End with one line naming the next hop from the entry table's "Then" column: `Next: {skill or "done"} — continue? (or /ask-matt to explore options)`. The user decides whether to take the next step.

If the natural next step is unclear, say so and tell the user to run `/ask-matt` rather than guessing.

### L3 · Large work (CONFIRM FIRST)
Escalate only when **at least one** hard trigger is met:
- change spans more than ~3 files or multiple modules
- work is too big for one session / needs a shared map across sessions
- several branching design decisions still open
- user explicitly asks to build a whole feature end-to-end, or to run autonomously for a long stretch

**Before entering L3, stop and confirm** with the user ("This looks L3 — I'll run: {list}. Proceed?"). Then pick **one** of the two L3 flows — don't run both:

- **Matt ticket-driven flow** -> `(U)to-spec` -> `(U)to-tickets` -> `(U)implement` per ticket -> `code-review`
  - Best when the work splits into independent tickets you want to ship one at a time.
  - For work larger than one session: `(U)wayfinder` (decision-ticket map) first, then drop back to L2 per ticket.
  - For architecture-wide scan & deepening: `(U)improve-codebase-architecture`.
- **Superpowers full flow** -> `brainstorming` -> `using-git-worktrees` -> `writing-plans` -> `subagent-driven-development` (or `executing-plans`) -> `requesting-code-review` -> `finishing-a-development-branch`
  - Best when you want the agent to run autonomously for a long stretch, or need subagent parallelism / isolated worktrees.

Pick by the shape of the work, not by habit. If unsure, default to Matt's ticket flow — it's easier to interrupt and re-steer mid-flight.

## Anti-rationalizations
- "Better safe — I'll plan it properly" -> no; that is the over-process failure. Match effort to size.
- "It's L3 so I should use Superpowers" -> only if the work needs autonomous long-stretch execution or subagent parallelism. Otherwise Matt's ticket flow is lighter and just as valid for L3.
- "It's L1/L2 but I'll quickly use a Superpowers skill" -> no; Superpowers stays out of L1 and L2. It only enters at L3, and even then as one of two equal options, not the default.
- "It's L1 but I'll quickly write a spec" -> no; L1 means do it.
- Uncertain between L2 and L3 -> treat as L2, note the risk, escalate only if a hard trigger actually fires.
