"""Rebuild data/corpus/ from local transcripts: the user message and your full turn's text."""
import glob, json, os
from common import DATA, TRANSCRIPTS, samples

def user_text(r):
    if r.get("type") != "user":
        return None
    c = r.get("message", {}).get("content")
    if isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None
        c = "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    if not isinstance(c, str) or c.startswith("Base directory for this skill") or "<local-command-caveat>" in c:
        return None
    return c

def extract(session, row):
    path = glob.glob(os.path.join(TRANSCRIPTS, session + "*.jsonl"))[0]
    rows = [json.loads(l) for l in open(path)]
    start = row
    while start >= 0 and user_text(rows[start]) is None:
        start -= 1
    parts = []
    for r in rows[start + 1: row + 1]:
        if r.get("type") != "assistant":
            continue
        for b in r["message"]["content"]:
            if isinstance(b, dict) and b.get("type") == "text" and b["text"].strip():
                parts.append(b["text"])
            elif isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "ReportFindings":
                parts.append("[ReportFindings rendered to the user]\n" + json.dumps(b["input"], indent=1))
    return user_text(rows[start]), "\n\n".join(parts)

if __name__ == "__main__":
    out = os.path.join(DATA, "corpus")
    os.makedirs(out, exist_ok=True)
    for name, s in samples().items():
        u, a = extract(s["session"], s["row"])
        open(f"{out}/{name}.user.md", "w").write(u)
        open(f"{out}/{name}.assistant.md", "w").write(a)
        print(f"{name}: {len(a.split())} words")
