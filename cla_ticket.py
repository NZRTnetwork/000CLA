"""
create_cla_ticket.py — create a Claude session traceability ticket assigned to xc.
Hardcoded: type=000LLM, category=CLA, assign=xc (user_id=2).

Usage:
  python create_cla_ticket.py --subject "Session 06.06 — updated NCS SOP, ticket scripts" \\
      [--message "..."] [--systems obs,agt,dol] [--project-id N] [--dry-run]

--systems: comma-separated shortcodes for systems touched in session.
  Shortcodes: api dol ics ncl ncs wor cpl mai inf scr tog obs fla git llm agt win bch llm
Auth: set DOLIBARR_API_KEY env var (xc Dolibarr API key)
"""
import argparse
import os
import sys
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv
load_dotenv(dotenv_path=r"C:\RPO-SAI\SYS\PLA\WIN\FRA\FAI\ORG\RPO-NZT\OPS\RPO-agt\SET\create_agents\.env")

DOL_HELPER_URL    = "https://nzrtnetwork.com/dol-sql-helper/"
DOL_HELPER_SECRET = "nzrt_f7a2c849e3d561b0"
DOL_BASE = "https://erp.nzrtnetwork.com/dolibarr/api/index.php"
DOL_WEB  = "https://erp.nzrtnetwork.com/dolibarr"

XC_USER_ID = 2

# Ticket tag IDs (llx_categorie rowid, type=ticket)
# Full tag set, verified against GET /categories?type=ticket (see CLAUDE.md).
# Re-derive from the live DB when tags change; keep this in sync.
SYSTEM_TAGS = {
    "aba": 408, "adm": 409, "aga": 400, "agt": 334, "api": 51,
    "app": 398, "aut": 401, "bch": 383, "bnz": 360, "bra": 410,
    "bun": 361, "bup": 411, "bus": 397, "cal": 402, "cas": 412,
    "cat": 413, "cfg": 414, "chr": 415, "cla": 384, "cod": 416,
    "com": 417, "con": 418, "cpl": 76,  "dai": 419, "dan": 420,
    "dem": 421, "doc": 422, "dol": 52,  "dve": 423, "ema": 424,
    "ety": 425, "eve": 403, "ext": 426, "fai": 427, "ffm": 375,
    "fil": 428, "fin": 429, "fla": 282, "flo": 430, "fox": 431,
    "fra": 432, "git": 283, "goo": 379, "gov": 433, "han": 434,
    "ics": 53,  "img": 435, "ins": 436, "int": 437, "ite": 54,
    "itg": 438, "k8s": 385, "kbs": 439, "llm": 333, "mai": 77,
    "med": 440, "mig": 441, "mnu": 442, "mp3": 443, "mp4": 444,
    "mth": 445, "ncl": 55,  "ncs": 56,  "not": 446, "obs": 281,
    "ops": 447, "orc": 404, "org": 448, "pal": 362, "pam": 449,
    "pat": 450, "pdf": 451, "pgc": 452, "pgt": 453, "pjs": 399,
    "pla": 454, "pln": 455, "pod": 394, "pol": 456, "por": 457,
    "pre": 458, "pro": 459, "psc": 460, "pst": 461, "ref": 462,
    "rev": 463, "rpo": 396, "rpt": 464, "sai": 465, "sch": 405,
    "scr": 204, "sdr": 466, "seq": 406, "ses": 467, "sli": 468,
    "str": 469, "sun": 470, "svc": 471, "sys": 472, "tag": 473,
    "tic": 474, "tog": 205, "tol": 475, "tri": 407, "tsk": 476,
    "typ": 477, "vlt": 478, "web": 479, "wik": 480, "win": 335,
    "wor": 57,  "wps": 481, "wts": 483, "x40": 482, "ytb": 395,
}


def dol_helper(op, **kwargs):
    payload = {"token": DOL_HELPER_SECRET, "op": op, **kwargs}
    body = json.dumps(payload).encode()
    req = urllib.request.Request(DOL_HELPER_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"dol-sql-helper {op} failed {e.code}: {e.read().decode()}")


def api(method, endpoint, data=None, api_key=None):
    url = f"{DOL_BASE}/{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("DOLAPIKEY", api_key)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)


def main():
    # CLA session tickets are xc's audit trail for xc's own Claude Code sessions.
    # Agent runs (`claude -p` from run-agents.ps1) inherit the global CLAUDE.md and
    # will otherwise follow its "MANDATORY session start" block and file one against
    # xc's name — cas did exactly that on 2026-07-19 (TS2607-0222). The runner marks
    # its children with NZRT_AGENT_RUN; refuse outright rather than rely on the prompt.
    if os.environ.get("NZRT_AGENT_RUN"):
        sys.stderr.write(
            "REFUSED: create_cla_ticket.py cannot be run from an agent run "
            f"(NZRT_AGENT_RUN={os.environ['NZRT_AGENT_RUN']}).\n"
            "CLA session tickets are xc's audit trail only. Agents consume tickets, "
            "they do not create them. Continue with your assigned tickets.\n")
        sys.exit(2)

    parser = argparse.ArgumentParser(description="Create a Claude session traceability ticket for xc")
    parser.add_argument("--subject", required=True, help="Session summary subject")
    parser.add_argument("--message", default="", help="Session detail body (optional)")
    parser.add_argument("--systems", default="llm", help="Comma-separated system shortcodes touched (default: llm)")
    parser.add_argument("--task-id", type=int, default=122, help="Session task ID (default: 122 = LLM-TSK-003)")
    parser.add_argument("--project-id", type=int, default=39, help="Link to Dolibarr project (default: 39 = PJ-LLM)")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without creating")
    args = parser.parse_args()

    api_key = os.environ.get("DOLIBARR_API_KEY") or os.environ.get("DOL_API_KEY")
    if not api_key:
        print("Error: set DOLIBARR_API_KEY env var", file=sys.stderr)
        sys.exit(1)

    systems = [s.strip().lower() for s in args.systems.split(",") if s.strip()]
    unknown = [s for s in systems if s not in SYSTEM_TAGS]
    if unknown:
        print(f"Warning: unknown system shortcodes (will skip): {unknown}", file=sys.stderr)
    tag_ids = [SYSTEM_TAGS[s] for s in systems if s in SYSTEM_TAGS]

    message = args.message or args.subject

    ticket = {
        "subject":              args.subject,
        "type_code":            "000LLM",
        "category_code":        "CLA",
        "fk_user_assign":       XC_USER_ID,
        "severity_code":        "NORMAL",
        "message":              message,
        "notify_tiers_at_create": 0,
        "fk_soc":               31,  # Anthropic — always the provider for CLA sessions
    }

    if args.dry_run:
        print("DRY RUN — payload:")
        print(json.dumps(ticket, indent=2))
        print(f"  Systems: {systems}")
        print(f"  Tag IDs to apply: {tag_ids}")
        if args.task_id:
            print(f"  Would link to task {args.task_id}")
        if args.project_id:
            print(f"  Would link to project {args.project_id}")
        return

    result    = api("POST", "tickets", ticket, api_key)
    ticket_id = result if isinstance(result, (int, str)) else result.get("id", result)

    details = api("GET", f"tickets/{ticket_id}", api_key=api_key)
    ts_ref  = details.get("ref", f"ID={ticket_id}") if isinstance(details, dict) else f"ID={ticket_id}"

    print(f"Ticket created: {ts_ref} (ID={ticket_id})")
    print(f"  Subject:     {args.subject}")
    print(f"  Assigned to: xc (user ID {XC_USER_ID}) — Claude session")
    print(f"  Ref:         {ts_ref}  (use this ref in all mentions)")
    print(f"  View: {DOL_WEB}/ticket/card.php?id={ticket_id}")

    if args.task_id:
        res = dol_helper("link_ticket_task", ticket_id=int(ticket_id), task_id=args.task_id)
        print(f"  task {args.task_id} {'linked OK' if res.get('ok') else 'link ERROR: ' + str(res)}")

    if args.project_id:
        res = dol_helper("link_ticket_project", ticket_id=int(ticket_id), project_id=args.project_id)
        print(f"  project {args.project_id} {'linked OK' if res.get('ok') else 'link ERROR: ' + str(res)}")

    for tag_id in tag_ids:
        res = dol_helper("tag_ticket_categorie", ticket_id=int(ticket_id), categorie_id=tag_id)
        code = next((k for k, v in SYSTEM_TAGS.items() if v == tag_id), str(tag_id))
        print(f"  tag {code}({tag_id}) {'applied OK' if res.get('ok') else 'ERROR: ' + str(res)}")


if __name__ == "__main__":
    main()
