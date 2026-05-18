# Agent: xc — Admin (Human)

**Role:** Administrator / CEO
**Tier:** 1 — Human
**Primary systems:** All

---

## This is the human operator role

xc is not an AI agent. It is the human who owns the organisation and controls
all credentials, approvals, and irreversible actions. This file documents xc's
role so AI agents know who they report to and what requires human approval.

---

## What xc controls

- All credentials, API keys, and access tokens
- User account creation and deletion on all systems
- Publishing and making content publicly visible
- Financial commitments and payments
- Structural changes to any system (folders, schemas, permissions)
- Deployment to production
- Overriding any agent decision

## What xc delegates to agents

- Drafting content, proposals, reports
- Reading and summarising data from any system
- Uploading to shared folders in Nextcloud
- Creating draft records in Dolibarr (proposals, orders, invoices — not confirmed)
- Generating analytics and cross-system summaries

---

## Escalation: when agents must stop and ask xc

Any agent must stop and ask xc before:
- Deleting any record, file, or account
- Publishing or sending anything externally
- Changing permissions or access on any system
- Making any financial transaction
- Taking an action they are uncertain about

---

## How to invoke xc coordination

```
"Acting as xc: [coordinate task across agents]"

"Acting as xc — delegate to pam: draft blog post about [topic]"

"Acting as xc — review pam's draft at /Shared/Marketing/drafts/ and approve for publishing"
```
