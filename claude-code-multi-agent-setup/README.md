# Claude Code Multi-Agent Setup

A pattern for running multiple scoped AI agents in a single Claude Code project. Each agent has a defined role, access boundary, and task scope — all configured through `CLAUDE.md` and `.claude/settings.json`.

Built from a real production system running 9 agents across Dolibarr ERP, Nextcloud, and WordPress.

## The Problem

Claude Code is powerful out of the box — but when you're using it to manage multiple business systems, a single undifferentiated "Claude" creates problems:

- No clear ownership of tasks ("who" does what)
- No access boundaries (Claude touches everything)
- No role-specific context (Claude doesn't know it's acting as finance vs marketing)
- Prompts grow unwieldy as scope expands

## The Solution

Define named agent roles in `CLAUDE.md`. Each role has:
- A **code** (short identifier used in frontmatter, file ownership, task routing)
- A **scope** (what systems and tasks this role touches)
- A **tier** (human admin vs AI agent vs restricted AI agent)
- **Access limits** (what it can and cannot do autonomously)

Claude doesn't become multiple models — it becomes context-aware of which role it's operating in for a given session.

## What's Included

```
claude-code-multi-agent-setup/
├── README.md
├── CLAUDE.md                     # Master agent config — copy and adapt
├── .claude/
│   ├── settings.json             # Permissions, hooks, env vars
│   └── hooks/
│       └── pre-tool-use.sh       # Example hook: log all tool calls
├── agents/
│   ├── README.md                 # How to define and use agents
│   ├── xc.md                     # Example: admin/human role
│   ├── pam.md                    # Example: marketing agent
│   ├── fin.md                    # Example: finance agent
│   └── dan.md                    # Example: DBA/infra agent
└── examples/
    ├── task-routing.md           # How to route tasks to specific agents
    └── agent-handoff.md          # How agents hand work to each other
```

## Quick Start

1. Copy `CLAUDE.md` to your project root
2. Edit the **Agent Roster** section — replace example agents with your roles
3. Edit **System Access** — list the systems each agent can touch
4. Copy `.claude/settings.json` — adjust permissions for your environment
5. Start a session: tell Claude which agent role it's operating as at the start

```
"Acting as [fin] — finance agent. Review the outstanding invoices in Dolibarr and flag any overdue."
```

## The Agent Pattern

### CLAUDE.md Structure

```markdown
## AI Agents

| Code | Role | Tier | Primary Systems |
|------|------|------|----------------|
| xc   | Admin / Human | 1 — Human | All |
| pam  | Marketing | 2 — AI | WordPress, CRM |
| fin  | Finance | 2 — AI | ERP, accounting |
| dan  | DBA | 3 — AI | GitHub, servers |
```

### Tier System

| Tier | Who | Autonomy |
|------|-----|---------|
| 1 — Human | The actual human operator | Full — approves all irreversible actions |
| 2 — AI | Department agents | High — can create/read within their system scope |
| 3 — AI (restricted) | Infrastructure agents | Low — read-mostly, writes need human confirmation |

### Scope Boundaries

Each agent definition specifies:
- **Can do autonomously**: read their systems, create drafts, generate reports
- **Must confirm with Tier 1**: deletes, publishes, permission changes, financial commits
- **Cannot do**: access other agents' credentials, touch systems outside their scope

## Agent Role Template

```markdown
## Agent: [code]

**Role:** [Human title]
**Tier:** [1/2/3]
**Primary systems:** [list]

### Can do autonomously
- [action 1]
- [action 2]

### Must confirm with xc (Tier 1)
- [irreversible action]
- [cross-system action]

### Cannot do
- [access boundary]
- [credential boundary]
```

## Works Best With

- **MCP tools** — wire up nc_*, dol_*, wp_* MCP tools so agents have real system access
- **Obsidian vault** — document agent tasks and decisions in a structured knowledge base
- **Hooks** — use `.claude/settings.json` hooks to log agent actions for audit trail

## Real-World Usage

This pattern runs [NZRT Network](https://nzrtnetwork.com)'s virtual organisation:
- 9 agents across marketing, sales, finance, HR, analytics, DBA, and admin
- Integrated with Dolibarr ERP, Nextcloud, and WordPress via MCP tools
- Fully documented in an Obsidian vault using the [obsidian-business-vault-template](https://github.com/nzrtnetwork/obsidian-business-vault-template)

## License

MIT

---

*Built by NZRT Network · [nzrtnetwork.com](https://nzrtnetwork.com)*
