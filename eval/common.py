import os
EVAL = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(EVAL, "data")
# The project the samples came from; Claude Code keys its transcript dir on that path.
CWD = os.path.abspath(os.path.expanduser(os.environ.get("TLDR_EVAL_CWD", "~")))
TRANSCRIPTS = os.environ.get(
    "TLDR_TRANSCRIPTS",
    os.path.expanduser("~/.claude/projects/" + CWD.replace("/", "-") + "/"))

def samples():
    rows = {}
    for line in open(os.path.join(EVAL, "samples.tsv")):
        if line.startswith("#") or not line.strip():
            continue
        name, session, row, args, checklist, _ = line.rstrip("\n").split("\t")
        rows[name] = dict(session=session, row=int(row),
                          args="" if args == "-" else args, checklist=checklist)
    return rows

def variant_path(variant):
    if variant == "working":
        return os.path.join(EVAL, "..", "tldr.md")
    return os.path.join(EVAL, "variants", f"{variant}.md")

def words(path):
    return len(open(path).read().split())
