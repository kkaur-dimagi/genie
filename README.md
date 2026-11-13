# Genie

Genie — Find ways to improve the next CHC implementation

A Claude Code agent built on the **canopy agent operating model** (see canopy
`docs/agent-operating-model.md`). Primary channel: `genie@example.com`.

## How it works
- **Persona** in `persona.md`; the operating contract in `CLAUDE.md`.
- **A turn** is the unit of work: `skills/turn/SKILL.md` is the re-read-every-time checklist.
- **Reads free, writes gated — rails, not gates:** canopy's session gating hook reads
  `config/gating.json` and hard-blocks wrong paths (`deny` rails that name the right path) at
  the tool-call boundary. Approval is procedural — the turn checklist's explicit
  draft-then-ask step — never a blocking hook modal (`approve` stays empty by default).
- **Email channel:** `bin/genie-email` — a thin shim over the shared `canopy email`
  engine; identity from `config/agent.json`. Raw `gog gmail send` is deny-railed.

## Run a turn
In Claude Code, from this repo: "do a turn". Genie re-reads `skills/turn/SKILL.md` and
follows it: preflight → process inbound (one counterpart at a time) → skill self-check → close.

## Make it yours
1. Fill in `persona.md` (voice, mandate detail, memory scope).
2. Add domain skills under `skills/<name>/SKILL.md`.
3. Add each outbound action as a `deny` rail in `config/gating.json` pointing at its one
   sanctioned path — not as prose, and not as an `approve` rule (approval is the turn
   checklist's job; hook modals stall autonomous work).
4. Store each secret the agent needs in its Canopy vault (canopy-web → the agent's Settings →
   Credentials), named as the env var it becomes (`CANOPY_WEB_PAT`, `GDRIVE_ROOT_FOLDER`). That
   is the only declaration: a runner writes `~/.genie/.env` from it, `/genie:setup`
   (`canopy cred env`) does the same on a laptop, and `bin/_env.py` reads it.
5. The agent's own thing is its MAILBOX (genie@example.com).
   - **Canopy-hosted** (an address on the workspace's own mail domain): nothing to sign in.
     canopy-web routes mail to the agent when it is created and sends as it; `canopy email`
     finds the route itself, and turns get a canopy-web thread UUID. canopy-web keeps every
     message, even ones that start no turn: an unscoped turn sweeps them with
     `canopy email inbox --repo .` (unread hosted threads). A Google sign-in is optional
     — only for Drive/Docs — and is for the agent's Google ACCOUNT, which is usually a different
     address (e.g. `genie@dimagi-ai.com`): name it in `config/agent.json`
     `google_account` (`canopy create-agent --google-account`), or gog runs as the mail address.
   - **Google** (Gmail / Google Workspace mail): sign it in once — the agent's Settings →
     External accounts → **Connect Google**, or `gog login genie@example.com --client canopy --services
     gmail,drive,docs,sheets,forms,appscript`. The gog OAuth client is the SHARED fleet app (`canopy`
     on a laptop, `canopy-web` from the button); never type a client in a gog command — use
     `"$(canopy email client --repo .)"`.
   Verify with `canopy email preflight --repo .`; send via `bin/genie-email`.
