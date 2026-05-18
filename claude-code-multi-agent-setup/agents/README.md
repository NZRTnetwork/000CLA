# Agent Role Definitions

Each file in this folder defines one agent role. Copy and adapt for your team.

## File Naming

`[role-code].md` — matches the code used in CLAUDE.md and vault frontmatter.

## How Claude Uses These

At session start, tell Claude which role it's in:

```
"Acting as [fin] for this session."
```

Claude reads the role definition and applies the scope and access rules throughout the session.

## Roles in This Example

| File | Role | Tier |
|------|------|------|
| `xc.md` | Admin / Human | 1 |
| `pam.md` | Marketing | 2 |
| `fin.md` | Finance | 2 |
| `dan.md` | DBA / Infra | 3 |

Add more by copying any Tier 2 template and adjusting the scope.
