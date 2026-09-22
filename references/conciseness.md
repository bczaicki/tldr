# Conciseness references

Source material for `/tldr` line editing. Examples are quoted from each guide.

- **Purdue OWL — Conciseness**: <https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/index.html>
  (sub-pages: [Eliminating Words](https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/eliminating_words.html),
  [Changing Phrases](https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/changing_phrases.html),
  [Avoid Common Pitfalls](https://owl.purdue.edu/owl/general_writing/academic_writing/conciseness/avoid_common_pitfalls.html))
- **UNC Writing Center — Conciseness handout**: <https://writingcenter.unc.edu/tips-and-tools/conciseness-handout/>
- **URI Graduate Writing Center — Concise writing tips and tricks**: <https://web.uri.edu/graduate-writing-center/concise-writing-tips-and-tricks/>

## Techniques, merged across the three guides

| Technique | Before → after | Source |
|---|---|---|
| **Collapse excess detail into the outcome** | "After booking a ticket… checked in, went through security… a three-hour delay before takeoff" (47w) → "My flight to Dallas was delayed for three hours." (9w) | Purdue: Eliminating Words §1 |
| **Put the action in the verb** (no nominalizations) | "The function of this department is the collection of accounts." → "This department collects accounts." | Purdue: Pitfalls §2; URI §2 |
| **Start with the subject, not an expletive** | "There are four rules that should be observed" → "Four rules should be observed" | Purdue: Pitfalls §1; URI §4 |
| **Active voice** | "Your figures were checked by the research department." → "The research department checked your figures." | Purdue: Changing Phrases §3; UNC; URI §1 |
| **One word for a phrase** | "due to the fact that" → "because"; "is able to" → "can"; "in the event that" → "if"; "prior to" → "before" | UNC §5; URI §9; Purdue: Pitfalls §4 |
| **Cut "of" chains / prepositional phrases** | "The opinion of the group is…" → "The group's opinion is…" | UNC §3; URI §7 |
| **Clause → phrase** | "The report, which was released recently" → "The recently released report" | Purdue: Changing Phrases §2 |
| **Combine sentences that share a subject** | "Ludwig's castles are… By his death, he had commissioned three castles" → "Ludwig's three castles are…" | Purdue: main page §3 |
| **Specific words over vague ones** | "talked about several of the merits of" → "touted" | Purdue: main page §1; URI §6 |
| **Cut intensifiers and filler modifiers** | "really", "basically", "kind of", "for all intents and purposes", "particular" | Purdue: Eliminating Words §2; UNC §2 |
| **Cut redundant pairs and categories** | "each and every", "end result", "future plans", "round in shape" | UNC §1; Purdue: Eliminating Words §4-5 |
| **Affirmative over stacked negatives** | "If you do not have more than five years…" → "Applicants with fewer than five years…" | UNC §6 |
| **Simple tense over -ing** | "were researching" → "researched" | URI §8 |

## How this maps onto `/tldr`

The guides edit prose one sentence at a time. `/tldr` also has to decide *which* sentences survive, and that triage is the part the guides don't cover. The eval showed that model output already avoids the phrase-level patterns (about 0.1 hits per 100 words; see `eval/score.py` `WORDY`). The techniques that could still shorten a tldr are:

- **Collapse excess detail into the outcome.** This is the guides' version of the triage's *Explanation → clause or pointer* rule.
- **Combine sentences that share a subject.** v3/v4 outputs split one item across 3-4 short sentences ("Its id is X. It overlaps Y.").
- **Specific words over vague ones.** A specific word replaces a phrase.

**Caution:** UNC's affirmative-over-negative rule must not flip a meaningful negative. "#6530 doesn't fix 2882" is the finding itself. The rule applies only to stacked negatives.
