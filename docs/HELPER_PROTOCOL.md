# HELPER_PROTOCOL — پروتکل عملیاتی Helper Consultation

> ⚠️ **[منجمد — FROZEN HISTORICAL REFERENCE]**
> مدل helper تغییر کرده است. این فایل اکنون یک مرجع تاریخی است و **پروتکل فعال نیست**.
> محتوای این فایل بدون لمس حفظ می‌شود (QL-6 · #۲۴ · part20/part21).
>
> **هدف:** تعریف نقش، حدود، و عملیات helper consultation در پروژه trading-system.
> **نسخه:** v1.0 (D24 از MDRS v2 — parallel to D8-D23)
> **Tier:** T1 (Constitution + Governance)
> **Source chat:** TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure
> **Subject of Review:** Review #003 (See docs/REVIEW_LOG.md, docs/reviews/2026-05-23-helper-infrastructure-d24.md)
> **مرتبط با:** Rule #51 (Explicit Approval), REVIEW_PROTOCOL.md, PRE_ADD_CHECKLIST.md, CLAUDE_CHECKLIST.md, 02_lessons.md (HM-series sub-section در part07)
> **Status:** Active governance doc از این لحظه به بعد

---

## ۱. Purpose و Scope

### ۱.۱ چرا این protocol وجود دارد

در چت `TRADING-phase1-part05-mdrs-v2-s31-redo` یک systemic pattern کشف شد: helper review در ۳ iteration روی Chunk 1 ۱۰+ catches تولید کرد، شامل **Concern C1 critical** — Rule #68 explicit list خود نقض M88 genus بود (eat-your-own-dogfood failure). این pattern به نام "Late-Catch Cascade" formalize شد (M-candidate، شماره در part07).

**درس استراتژیک:** N catches per iteration بدون convergence = signal که PROCESS upstream نیاز به تغییر دارد، نه drafting. ادامه iteration در همان mode = quadratic cost increase بدون fundamental improvement.

این protocol root cause را address می‌کند: persistent context + explicit operating rules + systematic review framework + bounded iteration.

### ۱.۲ Helper چیست (Positive Definition)

helper یک ad-hoc Claude chat جداگانه است که برای **consultation** از سوی user (نه AI-to-AI direct) اجرا می‌شود. helper functionally:

- **Second pair of eyes** — cross-check درافت‌ها قبل از atomic commit
- **Sandbox for exploration** — discussion گزینه‌ها بدون mutation main chat state
- **Manifestation of helper-side intelligence** — context/memory مستقل از main chat
- **Catch upstream pattern violations** — به‌خصوص M88, M77, M98 genus

### ۱.۳ Helper چه چیزی نیست (Negative Definition)

helper:

- ❌ **یک approval gate نیست.** تصمیم نهایی همیشه با user است (Rule #51 absolute برای MCP-mediated actions؛ این principle به helper consultation نیز اعمال می‌شود).
- ❌ **یک replacement برای user review نیست.** user explicit approval در chat جداگانه است.
- ❌ **یک authoritative source نیست.** helper findings فقط input هستند — vetting با main chat Claude + user.
- ❌ **یک iteration partner unbounded نیست.** Bounded Bootstrap pattern (§۳.۳) + escalation criteria (§۳.۴).
- ❌ **یک memory bridge بین چت‌ها نیست.** هر helper invocation فریش (مگر Project chat reused).

### ۱.۴ Authority Hierarchy

برای رفع ابهام part05 (Discovery #10: "helper consultative misinterpretation")، این hierarchy explicit:

1. **User explicit approval در chat** — absolute. (Rule #51 specifically scopes MCP-mediated actions به این principle؛ here we apply آن broader scope به helper consultation context per project decision.)
2. **Constitution** — rules, lessons, principles
3. **Project state-of-record** — SESSION_STATUS, PROJECT_MANIFEST, REVIEW_LOG
4. **Main chat Claude reasoning** — primary draft authority
5. **Helper findings** — advisory input only

اگر helper finding با hierarchy level 1-4 conflict داشت، level 1-4 win. این **نه** به این معنی است که helper finding ignored می‌شود — به این معنی است که conflict explicit به user surfaced می‌شود برای resolution.

### ۱.۵ Scope boundary vs related governance docs

این protocol درباره **helper consultation infrastructure** است. مرز با related docs:

| Document | Scope |
|---|---|
| HELPER_PROTOCOL.md (این) | helper invocation, review framework, helper-side anti-patterns, HM-lessons design |
| REVIEW_PROTOCOL.md | trigger و workflow برای Review Reports (post-trigger procedure) |
| PRE_ADD_CHECKLIST.md | 10-check gate قبل از artifact creation (pre-trigger diagnostic) |
| CLAUDE_CHECKLIST.md | per-chat workflow (boot، phase transitions، chat-end) — Claude operations |
| Chat naming convention | Pattern: TRADING-phase{N}-part{NN}-{topic}. حاکمیت در SESSION_STATUS + handoff files. HM-candidate در part07. |

**Overlap acknowledged:** helper consultation در طی Review process (REVIEW_PROTOCOL §۶ step 3 "Discuss") trigger می‌شود. این یک legitimate overlap point، نه redundancy.

---

## ۲. Scope 1 — Persistent Context Layer

### ۲.۱ Problem statement

قبل از D24: helper invocation pattern = user copies state → pastes در fresh chat → helper responds. مشکلات evidenced در part05:

- helper hasn't read constitution → cross-ref checks superficial
- helper doesn't know conventions → tier classification guess-based
- helper sees fragment → scope closure (M98) hard to verify
- repetitive setup cost → time-sink per consultation

### ۲.۲ Solution structure (دو-لایه)

**Layer A — Project Knowledge (file-based, ~static):**

Project Knowledge باید subset از T1 governance docs را که برای cross-check helper consultation ضروری هستند include کند. **authoritative source برای این subset:** `docs/PROJECT_MANIFEST.md` Tier=T1 entries، با filter:

- شامل: T1 governance + state-of-record core (constitution main + rules + lessons + principles core; REVIEW_PROTOCOL, PRE_ADD_CHECKLIST, HELPER_PROTOCOL, HANDOFF_TEMPLATE)
- خارج: T1 mutable state files که هر چت تغییر می‌کنند (SESSION_STATUS, CHAT_LOG, PENDING_FOR_NEXT_VERSION — این‌ها در user prompt paste می‌شوند نه از Project K)
- on-demand: bugs catalog، architecture module، meta module — اگر review subject این موضوعات را touch می‌کند، user manual upload می‌کند

**اصل کلیدی (M88 genus prevention):** lookup PROJECT_MANIFEST.md در زمان setup (و در stage-end refresh per §۲.۴). hardcoded list در این document intentionally absent تا drift hazard ساخته نشود — اگر آینده T1 doc جدید اضافه شد، manifest خود authoritative است.

**Setup-time guidance (illustration, نه enumeration):** اولین setup شامل constitution main + rules + lessons + principles + REVIEW_PROTOCOL + PRE_ADD_CHECKLIST + HELPER_PROTOCOL + HANDOFF_TEMPLATE معمول است — ولی این رقم در آینده تغییر خواهد کرد و authoritative manifest باید مرجع باشد.

**Layer B — Custom Instructions (prompt-injected, behavior-shaping):**

محتوای Custom Instructions (template در §۲.۵):

- Helper role definition (§۱.۲ + §۱.۳)
- 8-Layer Review Framework reference (§۴)
- Authority Hierarchy reminder (§۱.۴)
- Output format requirements (severity-tagged findings، structured per layer)
- Iteration limits awareness (Bounded Bootstrap)

### ۲.۳ Setup procedure (one-time, UI action)

> ⚠️ این یک user-side UI action است. Filesystem MCP یا Constitution lock impact ندارد.

**Architecture decision:** Single Project `trading-system` برای main + helper chats هر دو. Project Knowledge مشترک، naming convention chat-level تفکیک می‌کند.

**Rationale:** existing infrastructure (Project `trading-system` already in use برای main chats از part04 onwards) reuse می‌شود. main chat هم HELPER_PROTOCOL را در Project Knowledge access دارد (cross-reference قابل-اعتماد). Project K refresh یک بار، not duplicate.

**Setup steps:**

1. **Use existing Project `trading-system`** (likely موجود). اگر موجود نیست (fresh setup): Create Project: name = `trading-system`
2. Upload Project Knowledge files (per §۲.۲ Layer A، lookup-based from PROJECT_MANIFEST)
3. Configure Custom Instructions (paste template از §۲.۵)
4. **Chat naming convention within Project:**
   - **Main chats:** `TRADING-phase{N}-part{NN}-{topic}` (per project standard, Discovery #5 D24)
   - **Helper chats:** `TRADING-helper-{topic}` (e.g., `TRADING-helper-d24-review`, `TRADING-helper-s31-rules`)
   - Helper chats are short-lived (single consultation) typically; main chats are long-running per part
5. Bookmark یا pin Project برای دسترسی سریع

**Helper chat lifecycle:**

- Create helper chat برای specific consultation (e.g., review batch)
- Helper Custom Instructions auto-apply (Project-level config)
- Helper invocation: paste main chat context + artifact + request
- Helper output: structured findings per §۴.۱۱
- Helper chat may be retained (history) یا archived per user preference

**Single-Project benefit:** اگر main chat نیاز به read HELPER_PROTOCOL در runtime داشت (e.g., trigger criteria check)، Project Knowledge موجود است. هیچ cross-Project bridge لازم نیست.

### ۲.۴ Refresh policy + Enforcement

#### ۲.۴.۱ Triggers (when stale)

Project Knowledge content stale می‌شود وقتی هر یک از T1 docs در §۲.۲ Layer A subset تغییر کند. authoritative source برای "T1 changed?" = git diff بین last-refresh-commit و current HEAD، filtered به T1 paths per PROJECT_MANIFEST.

#### ۲.۴.۲ Enforcement mechanism (anti-silent-failure)

⚠️ **silent failure mode acknowledged:** اگر user فراموش refresh کند، helper با stale context cross-check می‌کند → invisible quality degradation. این critical failure mode است که زیر sensor radar می‌رود.

**Stage-end protocol integration (mandatory step):**

در هر stage-end commit boundary، Claude main chat باید explicit این check را در chat surface صورت دهد (visible per M100 hidden-checklist-completion principle):

  Project Knowledge refresh check (M100 visible):
  - Last refresh commit: HASH اگر user tracks، یا "unknown — please refresh as safety"
  - T1 files changed since last refresh: list from git diff filter
  - Refresh action needed: Yes / No / Unknown - recommend refresh

اگر "Yes" یا "Unknown" → user manual re-upload به Project Knowledge قبل از next helper consultation. این می‌تواند یک Pre-Add Check 11 (آینده) شود.

**این enforcement در stage-end، نه chat-end:**

- chat-end در یک stage = stage continues = چت بعدی همان stage subject، refresh مهم نیست تا stage-end
- stage-end = transition به stage بعدی = اگر helper used next stage، باید fresh context باشد

#### ۲.۴.۳ Failure recovery

اگر helper consultation با stale context صورت گرفت و فهمیده شد:

1. Log در main chat: "helper round X conducted با stale Project Knowledge"
2. اگر critical artifact (T1 doc creation, constitution edit) — re-run helper پس از refresh
3. اگر minor — accept finding، note risk در commit message

این acknowledges هیچ enforcement perfect نیست؛ recovery procedure explicit.

#### ۲.۴.۴ Future work (per §۱۰)

Automation candidates:
- pre-stage-end hook که git diff T1 paths را calculate کند و reminder چاپ کند
- semi-automated upload script (Claude Desktop UI API نیست در فعلی، ولی future)

### ۲.۵ Custom Instructions Template

  You are a helper Claude for the trading-system project. Your role is
  consultative cross-check, not approval. Read HELPER_PROTOCOL.md in
  Project Knowledge for full role definition.

  Authority hierarchy:
  1. User explicit approval (absolute)
  2. Constitution (Project Knowledge)
  3. State-of-record (in user's pasted prompt)
  4. Main chat Claude reasoning
  5. Your findings (advisory only)

  For every review request:
  - Apply 8-Layer Framework per HELPER_PROTOCOL section 4
  - Tag each finding with severity (critical/high/medium/low/cosmetic)
  - Structure output by layer (L1-L8), not by chronology
  - Be specific: quote exact line/section being reviewed
  - If you find > 5 catches OR critical, signal "escalate to bootstrap mode"
  - Do not approve. Surface findings; user decides.

  Iteration limit awareness: maximum 2 rounds per review subject. If round 2
  produces > 2 catches, recommend escalation per section 3.4.

  Output language: defer به project default per constitution main.md frontmatter
  (در زمان setup currently Persian، ولی preference reference در constitution
  احترام داده می‌شود اگر تغییر کرد).

### ۲.۶ Alternatives considered (documented per REVIEW_PROTOCOL §۴ spirit)

سه گزینه دیگر بررسی شدند:

- **Custom GPT-style:** نیاز به paid OpenAI account، vendor lock-in، tier mismatch (Claude-based main chat). Rejected.
- **API-driven helper:** programmatic helper invocation از main chat. مزایا: automation. معایب: complexity، debug-hard، lock-in به API quotas. Deferred (v2.x future).
- **MCP-based helper server:** local MCP server با helper logic. مزایا: native integration. معایب: dev overhead، maintenance burden. Deferred (future R&D).

Project K/I selected چون: zero-setup-cost beyond UI، vendor-aligned (هر دو Claude)، transparent (همه context visible).

---

## ۳. Scope 2 — Operating Protocol

### ۳.۱ Invocation patterns

helper invocation در main chat در یکی از این patterns:

- **User explicit:** «بپرس از helper» / «helper این را review کند»
- **Claude proactive suggestion:** بر اساس trigger criteria §۶
- **Bounded Bootstrap pattern:** explicit در drafting major artifacts (§۳.۳)

### ۳.۲ Information bridge (what helper sees / doesn't see)

**Helper sees:**

- Project Knowledge content (per §۲.۲ Layer A)
- Current user prompt (manual paste-based)
- Main chat artifact under review (manual paste-based)
- Previous helper-chat history (اگر same chat reused)

**Helper does NOT see:**

- Other concurrent main chat artifacts (مگر explicit pasted)
- Filesystem state directly (helper has no Filesystem MCP)
- Git state directly (helper has no shell access)
- Real-time main chat ongoing (snapshot-based view only)
- User's mental model یا غیر-textual context

این bridge **manual + paste-based + snapshot-based** است. limitation acknowledged، automation در §۱۰ future-work.

### ۳.۳ Bounded Bootstrap Pattern (D24-introduced)

برای drafting major artifacts (new T1, new rule batch, new T2 substantive):

  Step 1: Upfront constraint checklist (main chat Claude)
  Step 2: User review checklist + approval
  Step 3: Batch comprehensive draft (main chat Claude — همه scopes با هم)
  Step 4: یک round helper review (structured prompt, multi-section)
  Step 5: Apply escalation criteria (section 3.4)
  Step 6: Apply user-approved changes
  Step 7: Commit + push

این pattern **explicit prevention** از Late-Catch Cascade. evidence base: part05 turn 9-10 (scope-by-scope iteration) vs D24 itself (batch upfront) — comparison metric: catches per artifact.

### ۳.۴ Escalation criteria

پس از helper round 1:

- **≤ 2 minor catches** → proceed به implementation directly
- **3-5 catches** → یک iteration (round 2)، توقف بعد از round 2 regardless
- **> 5 catches OR critical-severity catch** → **escape به bootstrap mode**: no further helper round، user direct review، apply user-approved changes

این criteria evidence-based: part05 turn 9-10 showed > 5 catches = process upstream signal، نه drafting refinement need.

**Bootstrap mode:** main chat Claude + user (only). helper not involved. این کاهش از 5 → 2 layer review است (helper layer removed). برای exceptional cases (new artifact types که helper Project K/I cover نمی‌کند) یا late-cascade signal.

### ۳.۵ Round 2 entry/exit criteria

اگر escalation = "3-5 catches":

- **Round 2 entry:** main chat Claude apply user-approved changes از round 1 → new draft → helper round 2
- **Round 2 exit:** regardless of catches count، توقف. اگر round 2 catches > 2 → escape to bootstrap.

این hard limit از diminishing returns evidence (part05 review % افزایش 85→92→95→97→98% با fundamental concerns ongoing).

---

## ۴. Scope 3 — 8-Layer Review Framework

### ۴.۱ Layer order rationale

| Layer | Topic | Order reason |
|---|---|---|
| L1 | Anti-pattern self-violation | upstream — catches cascade سایر layer |
| L2 | Cross-reference validity | structural integrity |
| L3 | Tier classification accuracy | governance scope correctness |
| L4 | Scope closure (M98) | atomic boundary integrity |
| L5 | Audit-readiness (mechanical) | counts, version sync |
| L6 | Drift-detection (current state) | snapshot consistency |
| L7 | M75 within-file consistency | internal coherence |
| L8 | Forward-looking risk | future-stage drift hazard |

L1 first چون upstream: violation در L1 (e.g., M88 genus) معمولاً cascade در L2-L7 می‌سازد. catching L1 upstream، work downstream را save می‌کند.

L8 last چون forward-looking: requires L1-L7 stability assessment first.

### ۴.۲ L1 — Anti-pattern self-violation

**Criterion:** آیا artifact under review، خود نقض یک constitution rule یا M-lesson می‌کند؟

**Common genera:**
- **M88 genus** (Hidden Regeneration Hazard): explicit-list anti-pattern — hardcoded list که می‌تواند drift بسازد. Solution: principle-based با illustration examples.
- **M77 genus** (HEAD self-reference): hardcoded commit hash که نمی‌تواند pre-commit verify شود.
- **M82 genus** (verification claim unverified): «X انجام شد» بدون read-back.

**Severity assignment:** critical اگر violated rule خود subject artifact است (eat-your-own-dogfood failure — part05 Concern C1 pattern، D24 L1.1 pattern).

### ۴.۳ L2 — Cross-reference validity

**Criterion:** آیا cross-refs (Rule #N، M-N، Section §N، file paths) به entities موجود اشاره می‌کنند؟

**Check method:** sample 3-5 cross-refs، verify Project Knowledge.

**Severity:** high اگر broken cross-ref در navigation-critical path (e.g., main.md → 01_rules.md). medium otherwise.

### ۴.۴ L3 — Tier classification accuracy

**Criterion:** آیا artifact به Tier درست classified شده طبق Pre-Add Check 1 + MDRS Tier rules؟

**Check:** path matches Tier convention (T1 = `docs/constitution/` یا root-level governance، T2 = `docs/` reference، T3 = code، T4 = config/assets، T5 = excluded).

**Severity:** high اگر T1/T2 misclassified (governance impact). medium otherwise.

### ۴.۵ L4 — Scope closure (M98)

**Criterion:** آیا artifact scope-closed است؟ بدون forward-reference به upcoming sub-stage یا scope creep؟

**Check:** scan برای phrases مثل «در stage بعدی» یا «در commit آینده» — اگر این phrase to upcoming work در همان atomic boundary اشاره دارد، scope violation. **استثنا:** T1 governance docs می‌توانند planning intent references داشته باشند (per M98 caveat — distinct از scope creep within atomic commit).

**Severity:** high اگر atomic commit boundary affected. medium otherwise.

### ۴.۶ L5 — Audit-readiness

**Criterion:** آیا artifact mechanically verifiable است؟

**Sub-checks:**
- Count consistency (e.g., «N rules» در text با actual count match)
- Version sync (Constitution version در header با main.md match)
- Naming convention conformance (Pre-Add Check 3)
- Pre-commit hook prediction (will it pass؟)

**Severity:** medium typically. critical اگر pre-commit fail predicted.

### ۴.۷ L6 — Drift-detection (current state)

**Criterion:** آیا artifact با current state-of-record (SESSION_STATUS, PROJECT_MANIFEST, REVIEW_LOG) consistent است؟

**Check:** sample 3 facts، cross-ref با state files.

**Severity:** medium typically. high اگر drift در stats یا counts.

### ۴.۸ L7 — M75 within-file consistency

**Criterion:** آیا artifact خود internally consistent است؟ (e.g., aggregate count با sub-counts match؟ Reserved IDs explicit؟ namespace separation honored؟)

**Check:** scan tables، summaries، اعداد در text.

**Severity:** medium typically.

### ۴.۹ L8 — Forward-looking risk

**Criterion:** آیا این تصمیم در stage{next} یا v{X+1} drift می‌سازد؟

**Check questions:**
- آیا artifact references چیزی که در آینده outdated خواهد بود (e.g., explicit file list)؟
- آیا تصمیم با planned future stage conflict دارد؟
- آیا migration path explicit است (اگر convention تغییر کرد)؟

**Distinct از L6:** L6 = snapshot consistency (current). L8 = trajectory consistency (future).

**Severity:** high اگر hazard severe (e.g., HANDOFF_TEMPLATE-genus drift). medium otherwise.

**Precedent:** part05 Rule #68 explicit list — این L8 hazard بود (file list outdated می‌شد در hand-off ها). D24 L1.1 (Project K explicit list) — همین genus، caught در helper round 1.

### ۴.۱۰ Application modes

| Mode | Layers | Use case |
|---|---|---|
| **Deep review** | L1-L8 | new T1 docs, constitution edits, major refactor |
| **Targeted check** | subset (typical: L1+L2+L8) | specific risk known |
| **Fast pass** | L1 only | post-draft verification before final write |

Mode selection per §۶.

### ۴.۱۱ Output format (per layer)

helper output structured per layer:

  L1 — Anti-pattern self-violation: severity-tag
    Finding 1: specific quote + line ref
    ...

  L2 — Cross-reference validity: severity-tag
    Finding 1: ...
    ...

  ...

  L8 — Forward-looking risk: severity-tag
    Finding 1: ...

  Summary:
    Total catches: N
    Critical: X
    High: Y
    Medium: Z
    Low/cosmetic: W
    Escalation recommendation: proceed / round 2 / bootstrap

این format machine-parseable برای future audit script (R&D).

---

## ۵. Scope 4 — Cross-Chat Learning Continuity (HM-namespace)

### ۵.۱ Problem

helper-side discoveries differ از main-chat-side M-lessons:

- main chat M-lessons: Claude main-chat-side mistakes/insights
- helper findings: helper-side patterns (e.g., "helper consultative misinterpretation" Discovery #10 part05)

Mixing both در 02_lessons.md M-namespace = ambiguity. e.g., اگر "M50" = main chat lesson یا helper lesson؟

### ۵.۲ Solution: HM-prefix namespace

**HM** = Helper-Memory (یا Helper-Meta — semantic alternative).

نمونه: HM-1, HM-2, HM-3, ...

**Rationale (deliberate distinction):**

- Semantic separation: helper-side ≠ main-side
- Z3.24 spirit: namespace categorization explicit
- Reserved IDs in M-series نقض نمی‌شود
- Future audit می‌تواند هر دو را independently track
- Cross-refs distinct (`HM-3` vs `M-3` no collision)

**HM ≠ M deliberate:** این namespace جدا یک design choice است (per N2 answer D24)، نه continuation از M-series. اگر آینده evidence نشان داد که helper-side و main-side lessons converge می‌کنند (rare scenario)، migration به M-series قابل-بحث است — ولی default = جدا.

### ۵.۳ Storage location

`docs/constitution/02_lessons.md` — new sub-section **"§۲.۹ Helper Consultation Lessons (HM-series)"** پس از current §۲.۸ "توضیحات کامل critical lessons M82-M86" (verified در D24 پیش از write — section §۲.۸ یک standalone explanation section است، §۲.۹ next available).

Sub-section structure (per part07 implementation):

  ## ۲.۹ Helper Consultation Lessons (HM-series)

  ### HM-namespace rationale
  per §۵.۲ summary

  ### HM-1 — title
  criterion + evidence + lesson + cross-refs

  ### HM-2 — ...

### ۵.۴ Numbering convention

- Sequential از HM-1 (no zero-pad initially)
- Reserved IDs allowed (HM-{N} reserved if pattern observed but not formalized)
- No collision check با M-series (distinct namespace)

### ۵.۵ Z3.24 Migration note

اگر Z3.24 Option C selected در v2.14 design (full namespace split):

- Z-namespace stays Z (state drift)
- P-namespace جدید (policy questions)
- W-namespace جدید (work-EOC items)
- M-namespace stays M (main chat lessons)
- **HM-namespace stays HM (helper-specific lessons, distinct from M general)**

این explicit position prevention از future migration ambiguity.

### ۵.۶ Implementation timing

- **Design:** D24 (این document، §۵)
- **Implementation:** part07 S3.1 redo همراه با constitution v2.14 atomic update
- **First HM entries candidate:** Discovery #10 part05 ("helper consultative misinterpretation") + helper-discovered patterns در D24 (Discoveries #1, #3, #5, #6, #7 — all HM-candidates per logs)

PENDING entry در `docs/PENDING_FOR_NEXT_VERSION.md` صریح این timing.

**Forward-reference disclaimer (M98 caveat):** این forward-reference به part07 یک **planning intent** است، نه scope creep. T1 governance docs به‌طور inherently trajectories future را reference می‌کنند (forward-looking design). M98 scope closure در atomic commit boundaries اعمال می‌شود — این فایل از D24 commit boundary نمی‌گذرد (HELPER_PROTOCOL design در D24 atomic، implementation reference در part07 commit atomic). دو scope جداگانه، هر کدام closed.

---

## ۶. Scope 5 — Triggers and Operating Modes

### ۶.۱ Severity-based triggers (per Rule #77 **(candidate)** Hybrid C — pending locking در part07 S3.1)

| Severity | helper consultation |
|---|---|
| critical | **required** |
| high | **required** |
| medium | optional (Claude or user discretion) |
| low | skipped (default) |
| cosmetic | skipped |

### ۶.۲ Severity assessment (principle-based — M88 genus prevention)

severity assignment **principle-based**، نه hardcoded list:

- **critical:** affects constitution lock, MDRS v2 core, atomic boundary integrity, OR eat-your-own-dogfood (subject نقض می‌کند rule خودش)
- **high:** affects T1 یا T2 doc creation/substantive change, multi-stage impact, drift hazard, governance change
- **medium:** affects T2 یا T3 substantive change, single-stage impact
- **low:** affects T3 routine, single-file scope
- **cosmetic:** typo, format, whitespace

Examples illustrative only — actual assignment per principle-judgment per case.

### ۶.۳ Mode definitions

- **Deep review (L1-L8):** new T1 docs, constitution edits, major refactor. Time: ~15-30 min helper.
- **Targeted check (subset):** specific risk known در advance. Time: ~5-10 min.
- **Fast pass (L1 only):** post-draft verification. Time: ~3-5 min.

### ۶.۴ Mode selection criteria

| Scenario | Recommended mode |
|---|---|
| New T1 doc creation | Deep review |
| Constitution rule batch (S3.1-genus) | Deep review |
| T2 substantive change | Deep review or Targeted |
| Pre-Add Check 1 verification | Targeted (L3 focus) |
| Final pre-commit verification | Fast pass |
| Bug fix architectural review | Targeted (L1+L8 focus) |

selection principle: severity higher → deeper mode. Time-constrained scenarios → fast pass acceptable but log explicit.

---

## ۷. Upfront Constraint Checklist Pattern (META — Self-Applied)

### ۷.۱ Why upfront

evidence base: Late-Catch Cascade در part05 = scope-by-scope drafting → N catches per iteration → process upstream broken.

Solution: ALL constraints upfront → batch comprehensive draft based on approved constraints → single helper round → escalation criteria.

### ۷.۲ Template structure

  A. Constitution Lock Constraints (Hard)
  B. MDRS v2 & Tier Constraints
  C. Review Constraints (REVIEW_PROTOCOL trigger)
  D. Pre-Add Checklist (10 Checks visible execution per M100)
  E. M88 Genus Prevention
  F. Late-Catch Cascade Prevention (Bounded Bootstrap)
  G. Scope-by-Scope Boundaries
  H. Files Touched Plan (atomic boundaries)
  I. Commit Plan
  J. M-Lessons Applied
  K. PENDING Updates Plan
  L. Boot Boundary Verification
  M. Anti-Pattern Awareness (e.g., Z3.24)
  N. Open Questions

### ۷.۳ Application example

D24 خود = canonical example. See chat transcript «گام ۴ — Upfront Constraint Checklist» (turn before helper round) برای complete reference.

این self-application = eat-your-own-dogfood positive (vs negative pattern از part05 Concern C1).

---

## ۸. Anti-patterns (helper-side)

این patterns helper باید **اجتناب** کند:

- ❌ **Approving** — helper finding هرگز نباید "approved" یا "ready to commit" بگوید. user approves.
- ❌ **Unbounded iteration** — helper نباید "round 3, 4, 5" بپذیرد. escalation criteria binding.
- ❌ **Subjective feedback** — "looks good" یا "feels off" بدون layer-criterion citation. هر finding باید per-layer per-criterion structured باشد.
- ❌ **Late catch cascade** — اگر round 1 یک concern داشت، round 2 نباید **اضافی** concerns بسازد. اگر cascade observed، helper باید explicit escalation signal بدهد.
- ❌ **Endorsing deprecated artifacts** — helper اگر مثال‌های specific می‌آورد، باید verify current state (M88 second-order prevention).
- ❌ **Memory-based claims** — helper نباید "I remember from..." بگوید. هر claim باید source از Project Knowledge یا pasted prompt.

---

## ۹. Cross-references

| Topic | Reference |
|---|---|
| Explicit approval rule | Rule #51 (MCP-mediated scope) — broader application به helper per project decision |
| Helper consultative role (initial) | Rule #51 + Discovery #10 part05 |
| Review trigger procedure | REVIEW_PROTOCOL.md §۲ + §۶ |
| Pre-Add Checklist (gate) | PRE_ADD_CHECKLIST.md (10 checks) |
| CLAUDE_CHECKLIST per-chat workflow | docs/CLAUDE_CHECKLIST.md (referenced by PRE_ADD_CHECKLIST §۱.۱) |
| M88 genus prevention | 02_lessons.md M88 |
| M98 scope closure | 02_lessons.md M98 |
| Triple-Rule atomic | M93 |
| M101 Post-Handoff State Drift | 02_lessons.md (M-candidate در part07) |
| M-candidate Late-Catch Cascade | PENDING_FOR_NEXT_VERSION.md strategic section |
| HM-namespace sub-section | 02_lessons.md §۲.۹ (در part07) |
| Rule #77 (candidate) — Continuous Discovery Logging | PENDING_FOR_NEXT_VERSION.md R-NEW (pending Lock در part07 S3.1) |
| Chat naming convention (Discovery #5 D24) | TRADING-phase{N}-part{NN}-{topic} — pending HM-formalization در part07 |

---

## ۱۰. Version و Maintenance

| Field | Value |
|---|---|
| Version | v1.0 |
| Created | 2026-05-23 |
| Source chat | TRADING-phase1-part06-mdrs-v2-D24-helper-infrastructure |
| Source commit | (filled at D24.1 commit time) |
| Review Record | Review #003 (docs/REVIEW_LOG.md row #003) |
| Tier | T1 |
| Subject of future Reviews | yes — هر substantive change نیاز به Review |

**Maintenance triggers:**

- Constitution version bump → §۹ cross-refs review، update if needed
- Z3.24 resolution در v2.14 → §۵.۵ migration note implementation
- New helper-side anti-pattern discovered → §۸ extension (Review #N+)
- Layer framework evolution → §۴ revision (Review #N+)

**Future work (out of D24 scope):**

- API-driven helper (§۲.۶ alternative) R&D
- MCP-based helper (§۲.۶ alternative) R&D
- Machine-parseable output format (§۴.۱۱) → audit script integration

---

**📌 پایان HELPER_PROTOCOL.md**
