# Agent Handoff Patterns

How agents pass work to each other in a multi-agent Claude Code setup.
All handoffs go through Nextcloud shared folders — the shared filesystem is the
message bus. No agent speaks directly to another; they write outputs and xc (or
the next agent) picks them up.

---

## Core Pattern

```
Agent A completes task → saves output to /Shared/<folder>/ → xc confirms → Agent B reads from /Shared/<folder>/
```

Agents do not chain automatically. xc is always in the loop between agents for
anything non-trivial.

---

## Handoff Message Format

When an agent saves a handoff file, the filename and content should make the
next step obvious without further explanation.

**Filename convention:**
```
YYYY-MM-DD_[source-agent]_to_[target-agent]_[brief-description].md
```

**Example:**
```
2026-04-25_pam_to_ema_product-launch-copy.md
```

**File content structure:**
```markdown
# Handoff: pam → ema
Date: 2026-04-25
From: pam (Products & Marketing)
To: ema (EDM & Communications)
Status: ready for action

## What I did
Drafted product copy for the Iteasel launch. Saved final version to
/Shared/Marketing/copy/iteasel-launch-v1.md

## What ema needs to do
1. Read /Shared/Marketing/copy/iteasel-launch-v1.md
2. Draft a launch email using this copy
3. Save draft to /Shared/Dolibarr_EDM/campaigns/iteasel-launch-email.md
4. Flag to xc for review before sending

## Notes
- Keep subject line under 60 chars
- Target audience: small business owners, solo operators
```

---

## Common Handoff Sequences

### 1. Product → Marketing → EDM

```
pam: writes product copy → saves to /Shared/Marketing/copy/
     writes handoff to /Shared/Marketing/handoffs/2026-04-25_pam_to_ema_[desc].md

xc:  reviews copy, confirms OK to proceed

ema: reads copy from /Shared/Marketing/copy/
     drafts email campaign → saves to /Shared/Dolibarr_EDM/campaigns/
     flags to xc for send approval
```

### 2. Sales → Finance (invoice trigger)

```
cas: confirms order in Dolibarr → saves order summary to /Shared/Sales/
     writes handoff to /Shared/Sales/handoffs/2026-04-25_cas_to_fin_[desc].md

xc:  confirms order is complete

fin: reads order summary
     creates draft invoice in Dolibarr
     flags to xc for approval before sending to customer
```

### 3. Procurement → Finance (supplier payment)

```
sun: receives goods, marks reception in Dolibarr
     saves supplier invoice scan to /Shared/Procurement/invoices/
     writes handoff to /Shared/Procurement/handoffs/

xc:  approves payment

fin: records payment in Dolibarr bank module
     uploads payment confirmation to /Shared/Finance/payments/
```

### 4. Analytics → All (monthly report)

```
dai: pulls cross-system data from Dolibarr
     reads summary files from /Shared/Marketing, /Shared/Sales, /Shared/Finance (read-only)
     generates consolidated report → saves to /Shared/Analytics/reports/YYYY-MM/

xc:  reviews and distributes
```

---

## Handoff Checklist (for each agent)

Before saving a handoff:
- [ ] Output file is in the correct `/Shared/<folder>/` location
- [ ] Filename is dated and describes the content
- [ ] Handoff note names the target agent and lists exactly what they need to do
- [ ] No credentials, passwords, or API keys are in any handoff file
- [ ] Status is clear: `ready for action` / `needs xc review` / `blocked — see notes`

---

## What xc does between handoffs

xc is not a pass-through. Between each agent step, xc:
1. Reads the output file
2. Verifies it matches the intended outcome
3. Decides whether to proceed, revise, or abort
4. Gives the next agent an explicit instruction (not just "continue")

This prevents compounding errors — one agent's mistake won't silently propagate
through the whole workflow.
