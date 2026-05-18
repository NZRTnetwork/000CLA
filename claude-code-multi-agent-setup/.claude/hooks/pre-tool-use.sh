#!/usr/bin/env bash
# .claude/hooks/pre-tool-use.sh
#
# PreToolUse hook — logs all tool calls and blocks access to credential paths.
# Exit 0 = allow. Exit 2 = block (message on stderr shown to Claude).
#
# Wired in .claude/settings.json under hooks.PreToolUse.
# Set AGENT_CODE in settings.json env block to identify the active agent.

INPUT="$(cat)"
AGENT="${AGENT_CODE:-xc}"
TOOL="$(echo "$INPUT" | python -c "import sys,json; print(json.load(sys.stdin).get('tool_name',''))" 2>/dev/null || echo "")"
PATHS="$(echo "$INPUT" | python -c "
import sys, json
inp = json.load(sys.stdin).get('tool_input', {})
print('\n'.join(str(v) for v in inp.values() if isinstance(v, str)))
" 2>/dev/null || echo "")"

# xc (human Tier 1) is never blocked
[[ "$AGENT" == "xc" ]] && exit 0

# Block access to credential paths for all AI agents
for pattern in "CREDS" ".env" "agent_credentials" "settings.local.json"; do
    if echo "$PATHS" | grep -qi "$pattern"; then
        echo "BLOCKED [$AGENT]: '$TOOL' tried to access restricted path ('$pattern')" >&2
        exit 2
    fi
done

# Log allowed tool call (set AGENT_LOG_FILE env var to enable)
[[ -n "${AGENT_LOG_FILE:-}" ]] && echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) [$AGENT] $TOOL" >> "$AGENT_LOG_FILE"

exit 0
