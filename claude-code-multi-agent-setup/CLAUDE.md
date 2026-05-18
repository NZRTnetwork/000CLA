# [Your Org Name] — Claude Code Agent Configuration

Replace everything in [brackets] with your own details.

---

## Organisation Overview

[Describe your organisation. What it does, what systems it runs.]

**Core systems:**
| System | Service Code | URL / Location |
|--------|-------------|---------------|
| [ERP] | `000DOL` | [url] |
| [Files] | `000NCL` | [url] |
| [Website] | `000WEB` | [url] |
| [Git] | `000GIT` | [url] |

---

## AI Agents

[Your human operator] is Tier 1 — the only human, approves all irreversible actions.
All other agents are Claude-powered with scoped access.

| Code | Role | Tier | Primary Systems |
|------|------|------|----------------|
| **xc** | Admin / Human | 1 — Human | All |
| pam | Marketing | 2 — AI | WordPress, CRM |
| cas | Sales | 2 — AI | ERP, CRM |
| fin | Finance | 2 — AI | ERP, accounting |
| han | HR | 2 — AI | ERP, HR modules |
| dan | DBA / Infra | 3 — AI | GitHub, servers |

**Customise this table** — remove roles you don't need, add roles you do.

---

## Agent Access Rules

### Tier 2 agents can autonomously:
- Read all data within their primary systems
- Create drafts, records, and documents within their scope
- Generate reports and summaries
- Update existing records within their scope

### Tier 2 agents must confirm with xc (Tier 1) before:
- Deleting any record or file
- Publishing content publicly
- Changing permissions or access
- Any financial commitment or payment
- Cross-system actions that affect multiple agents

### All agents cannot:
- Access credentials files (`CREDS/`, `.env`, API keys)
- Act on behalf of another agent without explicit instruction
- Take irreversible actions without Tier 1 confirmation

---

## Vault Conventions

### Frontmatter (required on all notes)
```yaml
---
tags: [<domain-tag>, <org-tag>, <service-code>, <note-type>]
aliases: [<human readable names>]
role: <role-code>
created: YYYY-MM-DD
status: draft|review|complete|active|archived
type: MOC|guide|reference|config|adr|schema
related:
  - "[[path/to/related-note|Display Name]]"
---
```

### Wikilinks
Always full path from vault root + display text:
`[[Domain/Subfolder/Note|Display Title]]`

### File Naming
- Folders: `Title Case` or `NN - Title Case`
- Notes: `Title Case.md`
- HOME.md = folder index (always)

---

## Key Files

| File | Purpose |
|------|---------|
| `HOME.md` | Master vault index |
| `schema.md` | Frontmatter schema, codes, conventions |
| `agents/` | Per-agent role definitions |

---

## How to Use Agent Roles in Sessions

At the start of a session, state which agent role Claude is operating as:

```
"Acting as [pam] — marketing agent. Draft a blog post about [topic] for nzrtnetwork.com."
```

Claude will apply the scope and access rules for that agent for the session.

For cross-agent coordination:
```
"Acting as [xc] — coordinate: ask pam to draft the post, then cas to prepare a follow-up email sequence."
```
