# ClawBoys Crew Memory

**Group**: ClawBoys
**Goal**: Execute tasks for Master (Daniel Riggs) with zero friction
**Conductor**: Kimi (orchestrates crew)

## Active Agents

| Agent | Platform | Location | Status |
|-------|----------|----------|--------|
| Kimi Claw Desktop | Windows (main PC) | Desktop | ✅ Active |
| CloudyClaw | Cloud Linux | Remote | ✅ Active |
| PhoneClaw | Android | Mobile | ✅ Active |
| ClawX Desktop | Windows | 100.65.191.124:18789 | ✅ Active |
| ClawX Mini | Windows | 100.85.177.19:18789 | ✅ Active |
| Hermes | CLI | Desktop PC | ✅ Active |

## Current Projects

1. **Electrician Curriculum** — 15-week safety-first course, in development
2. **Bridge Architecture** — Dispatcher v2 deployed with memory injection
3. **Shared Memory** — GitHub sync + auto-commit in progress

## Key Facts

- Master timezone: America/New_York
- Bridge folder: `C:\Users\thegr\Documents\ClawBoys-Bridge\`
- GitHub repo: `thegreatrigsby/clawboys-memory`
- Tailscale network: 100.x.x.x range
- Main PC Tailscale IP: 100.65.191.124
- Mini PC Tailscale IP: 100.85.177.19

## How to Use Dispatcher

Drop a `.txt` file in `incoming/`:
- `desktop: do something` → Desktop PC ClawX
- `mini: do something` → Mini PC ClawX
- `hermes: do something` → Hermes CLI
- No prefix → defaults to Desktop PC

Reply appears in `outgoing/` within 10-15 seconds.
