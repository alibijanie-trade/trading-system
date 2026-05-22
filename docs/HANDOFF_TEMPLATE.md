# HANDOFF TEMPLATE — Standard Format for Chat-End Handoff Files

> Purpose: Standard structure for all chat-end handoff files in this project.
> Location convention: `claude_workspace/incoming_permanent/PHASE{N}_PART{NN}_{TOPIC}_HANDOFF.txt`
> First defined: 2026-05-22 at end of chat TRADING-phase1-part03-mdrs-v2-implementation
> Rationale: User-requested permanent fix to prevent context-amnesia anti-pattern (M56 + M77 + M100 enforcement at chat boundaries)

---

## WHEN TO USE THIS TEMPLATE

Every chat ending with hand-off to a next chat MUST create a handoff file using this template structure. Triggers:

- Context budget low + work incomplete = handoff
- Stage boundary reached + intentional split between chats
- User explicitly requests hand-off
- Any situation where state transfer between chats is needed

---

## TEMPLATE STRUCTURE

```
# PHASE{N} PART{NN} — {Stage/Topic} HANDOFF

> Chat Source: {previous-chat-name}
> Date: YYYY-MM-DD ({stage marker})
> Branch: {branch-name}
> Final commit: {hash}
> Next Chat Title: {next-chat-name}

---

## CRITICAL CONTEXT AWARENESS (READ FIRST)

You (the Claude reading this in the next chat) have NO MEMORY of the previous chat. Each chat is an independent AI instance. What you have available:

1. THIS handoff file (boot guidance)
2. Filesystem MCP for reading all project files
3. GitHub remote (git log, git show for full history)
4. State-of-record files: docs/SESSION_STATUS.md, docs/CHAT_LOG.md, docs/PENDING_FOR_NEXT_VERSION.md

What you DO NOT have:

1. Conversational context from the previous chat (negotiations, user catches, iteration loops)
2. Tone and partnership style established in the previous chat
3. Any memory of past decisions — all must be reconstructed from files

CRITICAL Anti-patterns (M56 + M77 + M100):
- DO NOT claim from memory anything you have not read in a file
- DO NOT write "I remember from the previous chat..." — this is a false claim
- If something is unclear, ASK — do not assume

The user expects partnership-style work with:
- Preview-then-approve for substantive document creation
- Visible pre-add checklist execution (M100): explicit Yes/No + reasoning per check in chat surface
- Triple-Rule honored (M93): SESSION_STATUS + CHAT_LOG + PROJECT_MANIFEST atomic at stage boundaries
- -F flag for long commits (M99): git commit -F claude_workspace/commit_msg_{stage}.txt
- ASCII-only commit messages (M95 + M97): no metacharacters
- Read-back verify after every write (Rule #37)
- Helper chat consultation at major decision points
- User catches drive lesson discovery — visibility in preview enables this

Before proceeding to any task in this chat, you MUST:
1. Read all files listed in "FILES TO READ ON BOOT" section below
2. Run git state verification commands (git status, git log --oneline -12)
3. Ask the user the sign-off questions in the "BOOT QUESTIONS" section
4. Wait for user approval before starting work

If at any point you are tempted to act from memory rather than from files, STOP. Read the file. Quote the file. Then act.

---

## FILES TO READ ON BOOT (in order)

1. docs/SESSION_STATUS.md (current state)
2. docs/PENDING_FOR_NEXT_VERSION.md (find latest version section)
3. THIS file (the handoff file you are reading)
4. docs/PROJECT_MANIFEST.md (manifest state)
5. {stage-specific files relevant to next chat work}
6. docs/CHAT_LOG.md (latest chat section)
7. The 10 mandatory constitution files per Rule #68.2 Boot Protocol

---

## BOOT QUESTIONS

Ask the user explicitly before starting work:

1. Confirm branch {branch-name} is current HEAD ({hash})?
2. Confirm Constitution version still {version} (no manual edits between chats)?
3. Confirm execution plan for next stage (as outlined in this handoff)?
4. Any new context or constraint discovered between chats?
5. {Stage-specific verification question}

---

## EXECUTIVE SUMMARY

{1-2 paragraphs: What was accomplished in previous chat, what state the project is in, what comes next}

---

## CURRENT STATE (as of end of previous chat)

{Branch state, version state, progress markers, key counts, manifest state}

---

## NEW ITEMS (Already in PENDING_FOR_NEXT_VERSION.md)

{Brief reference to where the details are, e.g., "See docs/PENDING_FOR_NEXT_VERSION.md tail section for full structured tables"}

---

## NEXT STAGE — DETAILED EXECUTION PLAN

{Sub-commit structure, deliverables, dependencies, atomic boundaries}

---

## SUBSEQUENT STAGES — OVERVIEW

{Brief outline of stages beyond the immediate next, for awareness}

---

## CRITICAL LESSONS APPLIED IN PREVIOUS CHAT (DO NOT FORGET)

{M-lessons with brief explanation, especially user-catch-derived lessons}

---

## CRITICAL OPERATIONAL PATTERNS

{Commit pattern, checklist pattern, review pattern, atomic stage-end pattern — refer to constitution where defined}

---

## FILES TO PRESERVE / TO DELETE

{What stays, what goes in next chat's chat-end commit}

---

## KEY COMMITS AND REFERENCE

{Commit list with brief description, transcript pointers if any}

---

## USER META-PRINCIPLES (PRESERVED)

{Direct quotes from user about working style preferences — these transcend individual chats}

---

## FINAL STATE-OF-RECORD CONFIRMATION

{What the chat-end commit accomplished, state of branch, ready signal for next chat}

End of HANDOFF.
```

---

## CHECKLIST FOR HANDOFF CREATION (at chat-end)

Before creating handoff file, verify:

1. State-of-record files (SESSION_STATUS, CHAT_LOG, PENDING_FOR_NEXT_VERSION) are atomically committed in chat-end commit (M93 enforcement)
2. Tracker (if any used in current chat, e.g., MDRS_V2_PENDING_DRAFT.md) is transferred to PENDING_FOR_NEXT_VERSION.md
3. Tracker file is then deleted in same atomic commit
4. Handoff file is placed in `claude_workspace/incoming_permanent/` with naming convention
5. Handoff file is included in atomic chat-end commit
6. Commit message uses -F flag (M99) and ASCII-only content (M95 + M97)
7. Push immediately after commit (#66)
8. Provide user with paste-ready handoff text for next chat

---

## ENFORCEMENT

This template is a permanent project asset. Any chat-end handoff that omits the CRITICAL CONTEXT AWARENESS section or BOOT QUESTIONS section is non-conformant.

Future audit check (proposed for v2.14+): scan claude_workspace/incoming_permanent/*HANDOFF*.txt for required sections.

---

## VERSION HISTORY

- v1.0 (2026-05-22): Initial template defined at end of TRADING-phase1-part03-mdrs-v2-implementation. Triggered by user request after recognizing M100 pattern in handoff design (context-amnesia anti-pattern needs explicit prevention in template, not just chat-specific text).

---

## RELATED LESSONS AND RULES

- M56: Memory-based claims need source verification
- M77: HEAD self-reference must use placeholder
- M93: Triple-Rule Atomic Boundary (atomic state-of-record at stage/chat boundaries)
- M100: Hidden-Checklist Completion (visibility requirement)
- Rule #68.2: Boot Protocol mandatory file reads
- Rule #51: Explicit approval for actions
- Rule #66: Push at end-of-chat
