#!/bin/zsh
# usage: eval/run.sh <variant>... [-- sample...]
#   variant: a file in eval/variants/ (v4) or "working" for ./tldr.md
# Generates 3 reps per sample, grades each, prints the score table. Skips work already on disk.
EVAL=${0:A:h}
DATA=$EVAL/data
CTX=${TLDR_EVAL_CWD:-$HOME/code/phillips-connect}   # cwd for runs: loads that project's CLAUDE.md + memory
MODEL=${TLDR_EVAL_MODEL:-claude-opus-5-5}
REPS=${TLDR_EVAL_REPS:-3}
CLAUDE=(claude -p --tools "" --no-session-persistence --strict-mcp-config --model $MODEL)

if [[ $1 == _gen ]]; then
  out=$DATA/out/$2.$3.r$4.md; [[ -s $out ]] && exit 0
  (cd $CTX && python3 $EVAL/build_prompt.py $2 $3 | $CLAUDE > $out.tmp 2>/dev/null) && mv $out.tmp $out
  exit
elif [[ $1 == _grade ]]; then
  out=$DATA/grade/$2.$3.r$4.json; [[ -s $out ]] && exit 0
  (cd $EVAL && python3 grade_prompt.py $2 $3 $4 | $CLAUDE > $out.tmp 2>/dev/null) && mv $out.tmp $out
  exit
fi

variants=(); while (( $# )) && [[ $1 != -- ]]; do variants+=$1; shift; done; shift
sample_list=(${@:-$(awk -F'\t' '!/^#/ && NF {print $1}' $EVAL/samples.tsv)})
mkdir -p $DATA/out $DATA/grade
jobs=(); for v in $variants; do for s in $sample_list; do for r in $(seq $REPS); do jobs+="$v $s $r"; done; done; done
printf '%s\n' $jobs | xargs -P 8 -L 1 $0 _gen
printf '%s\n' $jobs | xargs -P 8 -L 1 $0 _grade
python3 $EVAL/score.py $variants
