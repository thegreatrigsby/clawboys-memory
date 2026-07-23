# Kimi Claw Desktop — Persistent Memory

**Location:** `C:\Users\thegr\Documents\ClawBoys-Bridge\shared-memory\kimi-desktop-memory.md`
**Fallback:** `~/.kimi_openclaw/workspace/MEMORY.md`

---

## User Preferences

- The user explicitly wants ClawX to keep improving itself with useful skills, better research habits, durable memory, and Claude-like agentic behavior: explore first, reason carefully, use tools, verify with evidence, and learn from mistakes.
- The user is comfortable with proactive internal self-improvement within safe bounds: adding reputable skills, creating local workflow skills, updating memory/guidance, and scheduling quiet self-review. External actions, credentials, destructive changes, or privacy-sensitive sharing still require explicit approval.
- **Tradesman and curriculum writer** — intuitive document formatting is critical.
- **NEVER hallucinate or approximate** — look up the correct answer, cross-check sources, cite references.
- **Rule:** "Better than 'I'm not sure' — just look up the correct answer."

## Assistant Operating Preferences

- Be concise, capable, warm, and practical.
- Prefer concrete action over promises.
- Use durable notes/skills/guidance for lessons that should survive restarts.
- When resuming after compaction, aborts, or partial state, verify actual files/tool state instead of relying on summaries alone.

## Curriculum Rules (Immutable)

When creating or editing curriculum — these rules are HARD GATES, not suggestions:

1. **Safety & PPE → ALWAYS FIRST**
2. **Tools & math → before electrical theory**
3. **DC circuits → before AC circuits**
4. **Theory → before hands-on practice**
5. **Low voltage → before high voltage**
6. **Dead circuits → before live work**
7. **NEVER put students in danger** in training exercises

### Progressive Learning Order Example (Electrician)
- Week 1: Safety, PPE, tool identification, basic math
- Week 2: Electrical theory (Ohm's Law, series/parallel)
- Week 3: DC circuits, breadboard work (dead)
- Week 4: AC theory, transformers
- Week 5: Residential wiring (low voltage, dead)
- Week 6: Panel work (supervised, low voltage)
- Week 7+: Advanced topics with proper prerequisites met

## Document Formatting Rules

- **Preserve visual formatting** — match existing document styles
- **Tables for structured data** — schedules, rubrics, checklists
- **Headings for hierarchy** — H1 module, H2 week, H3 lesson
- **Consistent fonts** — match the source document
- **No raw dumping** — format for human readability
- **Screenshot-verify** — for mobile agents, confirm output looks right

## Verified Sources (Curriculum)

- OSHA 29 CFR 1926 Subpart K (Electrical)
- NFPA 70E (Standard for Electrical Safety in the Workplace)
- NCCER Electrical Level 1-4 Curriculum
- IBEW/NECA training standards
- NEC (National Electrical Code) 2023

## Skills Installed

| Skill | Purpose | Location |
|-------|---------|----------|
| error-recovery | Retry/backoff/circuit breaker | `~/.openclaw/skills/error-recovery` |
| web-scraping-advanced | CSS selector extraction | `~/.openclaw/skills/web-scraping-advanced` |
| observability-logging | JSONL activity logging | `~/.openclaw/skills/observability-logging` |
| debugging-and-error-recovery | Systematic debugging triage | `~/.openclaw/skills/debugging-and-error-recovery` |
| process-management | Linux process mgmt (limited use on Windows) | `~/.openclaw/skills/process-management` |

## System Status (Last Updated)

- ClawX auto-driver: PID 11536, running
- Hermes auto-daemon: PID 14116, running
- Ollama: Port 11434 listening
- ClawX Desktop API: Port 18789 responding
- OpenClaw gateway: Running via Kimi Desktop (port 18679)
- Startup shortcuts: Fixed for next reboot
- Bridge: Operational (tested 2026-07-23, autonomous file processing confirmed)
