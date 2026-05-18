# Task Routing — Which Agent Handles What

Use this as a reference when delegating tasks. Route to the most specific agent
that has access to the required system. Escalate to xc for cross-agent
coordination or irreversible actions.

---

## Quick Reference

| Task type | Route to | Systems used |
|-----------|----------|-------------|
| Blog post, product copy, social content | `pam` | WordPress, Nextcloud /Marketing |
| CRM lookup, sales proposal, order status | `cas` | Dolibarr CRM, Nextcloud /Sales |
| Supplier lookup, purchase order, stock check | `sun` | Dolibarr suppliers, Nextcloud /Procurement |
| Invoice status, payment tracking, financial report | `fin` | Dolibarr accounting, Nextcloud /Finance |
| Leave requests, HR records, expense reports | `han` | Dolibarr HRM, Nextcloud /HR |
| Email campaign, newsletter draft, template update | `ema` | Dolibarr EDM, Nextcloud /Dolibarr_EDM |
| Cross-system analytics, pipeline report, data export | `dai` | All Dolibarr (read), Nextcloud /Analytics |
| Database schema, backup log, DB ops | `dan` | Nextcloud /Database only (Tier 3) |
| Anything irreversible, cross-agent, strategic | `xc` | All systems |

---

## Routing Examples

### Single-agent tasks

```
# Marketing — content creation
"Acting as pam: draft a blog post about [topic] and save as draft in WordPress."

# Sales — pipeline check
"Acting as cas: list all open proposals in Dolibarr older than 30 days."

# Finance — overdue invoices
"Acting as fin: list unpaid invoices and total outstanding amount."

# HR — leave status
"Acting as han: list pending leave requests in Dolibarr."

# Procurement — stock alert
"Acting as sun: check stock for [product ref] and flag if below reorder level."

# EDM — campaign draft
"Acting as ema: draft a promotional email for [offer] and save to /Shared/Dolibarr_EDM/campaigns/."

# Analytics — cross-system summary
"Acting as dai: generate a monthly summary across all Dolibarr modules and save to /Shared/Analytics/."
```

### Multi-agent tasks (xc coordinates)

```
# Product launch workflow
"Acting as xc:
  1. Ask pam to write product copy for [product] and save to /Shared/Marketing/
  2. Ask cas to create the product record in Dolibarr CRM
  3. Ask ema to draft a launch email and save to /Shared/Dolibarr_EDM/campaigns/"

# Month-end close
"Acting as xc:
  1. Ask fin to generate the monthly invoice report and save to /Shared/Finance/reports/
  2. Ask dai to pull a cross-system summary for the same period
  3. Review both reports and confirm close"
```

---

## Escalation Rules

Always route to `xc` when:
- The task requires **deleting** any record or file
- The task involves **publishing** content publicly (not just drafting)
- The task requires **payment** or financial commitment
- The task spans **3 or more agents** in a single workflow
- The task touches **CREDS** or any credential file
- Any agent returns an **error or unexpected result** mid-task

---

## Anti-patterns

**Don't do this:**
```
# Wrong — pam has no access to finance data
"Acting as pam: check if the invoice for [client] has been paid."
→ Route to fin instead.

# Wrong — dan is Tier 3, cannot touch Dolibarr
"Acting as dan: export the product list from Dolibarr."
→ Route to dai instead.

# Wrong — irreversible action needs xc
"Acting as cas: delete the duplicate customer records in CRM."
→ Escalate to xc, who delegates with explicit approval.
```
