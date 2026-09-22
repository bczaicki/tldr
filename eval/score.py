"""Score table: checklist retention, length ratio, fabrications, wordy-pattern density."""
import json, os, re, sys
from common import DATA, samples, words

# Line-edit patterns from references/conciseness.md (expletives, stock phrases, qualifiers, nominalizations).
WORDY = re.compile(r"""\b(there\s+(is|are|was|were)|it\s+is\s+\w+\s+that|due\s+to\s+the\s+fact|in\s+order\s+to|
    is\s+able\s+to|in\s+the\s+event\s+that|prior\s+to|with\s+regard\s+to|at\s+this\s+point\s+in\s+time|
    really|basically|very|actually|definitely|generally|quite|somewhat|
    (the|an?)\s+\w+(tion|ment|ance|ence)s?\s+of)\b""", re.I | re.X)

def grade(variant, name, rep):
    t = open(f"{DATA}/grade/{variant}.{name}.r{rep}.json").read()
    return json.loads(t[t.find("{"): t.rfind("}") + 1])

def cell(variant, name, reps):
    ret, ratio, fab, wordy = [], [], 0, []
    src = words(f"{DATA}/corpus/{name}.assistant.md")
    for r in reps:
        out = f"{DATA}/out/{variant}.{name}.r{r}.md"
        if not os.path.exists(out):
            return None
        text = open(out).read()
        g = grade(variant, name, r)
        marks = g["items"].values()
        ret.append(sum(1 if m == "Y" else .5 if m == "P" else 0 for m in marks) / len(marks))
        ratio.append(len(text.split()) / src)
        fab += len(g["fabrications"])
        wordy.append(100 * len(WORDY.findall(text)) / max(1, len(text.split())))
    n = len(reps)
    return sum(ret) / n, sum(ratio) / n, fab, sum(wordy) / n

if __name__ == "__main__":
    variants = sys.argv[1:]
    reps = range(1, int(os.environ.get("TLDR_EVAL_REPS", 3)) + 1)
    names = list(samples())
    print("sample | " + " | ".join(f"{v}: retain ratio fab wordy/100w" for v in variants))
    totals = {v: [] for v in variants}
    for name in names:
        row = []
        for v in variants:
            c = cell(v, name, reps)
            if c: totals[v].append(c)
            row.append(f"{c[0]:4.0%} {c[1]:.2f} {c[2]:2d} {c[3]:4.1f}" if c else "   —")
        print(f"{name:6} | " + " | ".join(f"{x:28}" for x in row))
    mean = []
    for v in variants:
        t = totals[v]
        mean.append(f"{sum(c[0] for c in t)/len(t):4.0%} {sum(c[1] for c in t)/len(t):.2f} "
                    f"{sum(c[2] for c in t):2d} {sum(c[3] for c in t)/len(t):4.1f}" if t else "—")
    print(f"{'mean':6} | " + " | ".join(f"{x:28}" for x in mean))
