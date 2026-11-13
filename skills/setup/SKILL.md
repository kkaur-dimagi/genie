---
name: setup
description: >
  Set up this machine to run Genie: fill ~/.genie/.env from Genie's
  Canopy vault on canopy-web, then check readiness. Use on
  first run, a new machine, or a missing/stale .env.
---

# Setup — Genie

A plugin is code; an **instance** is canopy-web's Agent record — identity, workspace and its
credentials (the Canopy vault).

**1. Fill the env.**

```bash
canopy cred env --agent genie --refresh
```

It prints the path it wrote (`~/.genie/.env`, 0600 — the worktree-clean home every
`bin/` script reads through `bin/_env.py`) and, on stderr, where the values came from. Relay a
refusal **verbatim** and act on it — it names its own fix: not a member of the agent's workspace,
or not one of its admins. Never guess past it. Missing values on
the Canopy vault are filled in the agent's Settings → Security tab on canopy-web.

**2. Check readiness.**

```bash
canopy agent doctor --slug genie
```

Relay any `FAIL` line as written — each one names its own fix.
