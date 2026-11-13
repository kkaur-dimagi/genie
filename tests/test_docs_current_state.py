"""Docs and skills say what is true now, never what used to be.

Git keeps history, and a history line in a file an agent reads misleads it. This pins the shapes a
history line takes in CLAUDE.md, persona, README, docs, skills and the config `_doc` strings: an ISO
date, an issue or PR number, "used to / formerly / was previously / no longer / until now", an
"owner decision" or "owner's rule" citation, and pointers to docs/superpowers or docs/archive.
A rule keeps its REASON in the present tense ("do not relax X: Y depends on it"); that is not history.

Fleet-standard guard: canopy's agent factory stamps this file verbatim and `canopy fleet-align`
distributes updates to it, so change the rule in canopy, not here. State the rule as it holds now
and put when, why and who in the PR description.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    [ROOT / n for n in ("CLAUDE.md", "persona.md", "README.md") if (ROOT / n).is_file()]
    + sorted((ROOT / "docs").rglob("*.md"))
    + sorted((ROOT / "skills").rglob("*.md"))
)
HISTORY = re.compile(
    r"\b20\d\d-[01]\d-[0-3]\d\b"                       # an ISO date
    r"|(?<![\w/&])#\d{3,}\b|\bPR #?\d+"                # a PR or issue number
    r"|\bowner decision\b|\bowner's rule\b"            # a citation of who decided
    r"|\bused to\b|\bformerly\b|\bno longer\b|\bwas previously\b|\buntil now\b"
    r"|docs/superpowers|docs/archive",
    re.I,
)


def test_no_history_in_the_files_an_agent_reads():
    bad = []
    for f in FILES:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if '"used to"' in line or "`used to`" in line:     # a line that NAMES the pattern to avoid
                continue
            if HISTORY.search(line):
                bad.append(f"{f.relative_to(ROOT)}:{n}: {line.strip()[:90]}")
    assert not bad, "state the rule as it holds now; history belongs in git:\n" + "\n".join(bad)


def _doc_strings(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str) and key.startswith("_") and key.endswith("doc"):
                yield f"{path}{key}", value
            else:
                yield from _doc_strings(value, f"{path}{key}.")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _doc_strings(value, f"{path}{i}.")


def test_config_doc_strings_have_no_history():
    bad = []
    for f in sorted((ROOT / "config").glob("*.json")):
        for where, text in _doc_strings(json.loads(f.read_text(encoding="utf-8"))):
            if HISTORY.search(text):
                bad.append(f"{f.relative_to(ROOT)}:{where}: {text[:90]}")
    assert not bad, "state the rule as it holds now; history belongs in git:\n" + "\n".join(bad)
