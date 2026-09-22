# tldr

`/tldr` is a Claude Code slash command. It condenses Claude's previous response into its shortest form while losing as little information as possible.

```
/tldr              condense the last response
/tldr slack        paste-ready Slack mrkdwn, in a code block
/tldr pm           outcomes and links, no file paths or code
/tldr <audience>   write for any audience you name
```

## Install

```sh
./install.sh   # symlinks ~/.claude/commands/tldr.md -> ./tldr.md (backs up a real file first)
```

## How it works

| Strategy | What it does |
|---|---|
| **Triage** | Sorts every source sentence into one of three groups. *Load-bearing* is kept. *Explanation* becomes a ≤10-word clause or a pointer (`path:line`, a PR link, "commands above"). *Scaffolding* is dropped. |
| **Shape by content** | Findings become ranked bullets, multi-attribute items a table, causal chains `A → B → C`, a question list one line per question. |
| **Fidelity** | Every statement traces to the source. A fix, next step, count or caveat appears only if the source states it. |
| **Length budget** | 20–35% of the source. When over budget, it shortens explanations first. A source under ~100 words gets one line. |
| **Language** | Active voice, digits with units, identifiers verbatim, and qualifiers that change the action kept as tags. |

## Evaluation

`eval/` runs A/B tests of command variants against real responses taken from past sessions:

- Each run is a fresh `claude -p` call with tools off.
- Each output is graded against a fact checklist written before anything ran.

```sh
eval/run.sh v4 working            # compare a stored variant with ./tldr.md, all samples x 3 reps
eval/run.sh working -- s1 s3      # only some samples
python3 eval/score.py v1 v4       # re-print the table from saved grades
```

**Metrics:**
- **retain:** checklist facts kept.
- **ratio:** output words ÷ source words.
- **fab:** claims the source never made.
- **wordy:** conciseness-guide patterns per 100 words.

| version | retain | ratio | fab (per 24 runs) | notes |
|---|---|---|---|---|
| v1 | 71% | 0.29 | 10 | 3-6 bullet cap; drops caveats; bullets only |
| v2 | 94% | 0.59 | 38 | keeps everything; invented "Fix:"/"Next:" lines |
| v3 | 91% | 0.42 | 9 | budget + explanation clause; shapes work |
| **v4** (live) | 90% | 0.43 | 6 | fidelity re-scan stops invented fixes and memory-sourced caveats |
| v5 (rejected) | 91% | 0.44 | 10 | v4 + a line-edit pass from the conciseness guides; no shorter, and dropped qualifiers turned hedged claims into certain ones |

**Open problem:** long, dense sources still land at 0.42–0.51 (s1, s3, s4). Wording isn't the cause: outputs already score about 0.1 wordy hits per 100 words. The length comes from how many details survive triage, so the next lever is triage itself, not line editing.

`eval/data/` (corpus, checklists, outputs, grades) is **gitignored**, because it holds excerpts of client-work transcripts. The corpus can be rebuilt with `python3 eval/extract.py`, which needs the local transcripts. `data/checklists.md` is hand-written and exists only on this machine.

## References

- [Purdue OWL — Conciseness](https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/index.html)
- [UNC Writing Center — Conciseness handout](https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/)
- [URI Graduate Writing Center — Concise writing tips and tricks](https://web.uri.edu/graduate-writing-center/concise-writing-tips-and-tricks/)

These are distilled, with examples and a mapping onto `/tldr`, in [references/conciseness.md](references/conciseness.md).
