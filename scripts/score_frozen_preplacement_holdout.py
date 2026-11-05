#!/usr/bin/env python3
"""Score holdout physical runs with frozen, previously produced predictions.

The predictions artifact is created before holdout implementations and must
not be edited in this workflow. Output actuals are measured after routing.
"""
import csv,json,re,statistics,sys
from pathlib import Path
physical=Path(sys.argv[1]);prediction_file=Path(sys.argv[2]);output=Path(sys.argv[3])
output.mkdir(parents=True,exist_ok=True)
predictions={(r["size"],r["context"]):r for r in csv.DictReader(prediction_file.open())}
def slack(p):
 t=p.read_text()
 x=re.search(r'(?m)^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)',t)
 if not x:raise RuntimeError(f"Missing valid setup slack in {p}")
 return float(x.group(1))
rows=[]
for size in ("32x8","32x16"):
 for ctx in ("late_high","late_mid","staggered"):
  assert (size,ctx) in predictions
  for seed in (11,23):
   scores={}
   early={}
   for arch in ("row","word"):
    p=physical/size/"integration"/arch/ctx/f"s{seed}"
    scores[arch]=slack(p/"routed_read_path.rpt")
    early[arch]=slack(p/"read_reg_to_reg.rpt")
    assert (p/"routed.spef").stat().st_size>1000
    assert "ROUTED_AND_SPEF_IMPORTED" in (p/"routed_flow_status.txt").read_text()
   oracle=max(scores,key=scores.get)
   early_decision=max(early,key=early.get)
   guess=predictions[(size,ctx)]["selection"]
   rows.append(dict(size=size,context=ctx,seed=seed,predicted=guess,oracle=oracle,early_placement=early_decision,
     row_minus_word_slack_ps=round(1000*(scores["row"]-scores["word"]),3),
     predictor_regret_ps=round(1000*(scores[oracle]-scores[guess]),3),
     early_regret_ps=round(1000*(scores[oracle]-scores[early_decision]),3),
     predictor_gain_over_word_ps=round(1000*(scores[guess]-scores["word"]),3),
     oracle_gain_over_word_ps=round(1000*(scores[oracle]-scores["word"]),3)))
with (output/"holdout_comparisons.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary=dict(
 frozen_predictions_from="Actions run 42130789146 (created before physical holdout)",
 total=len(rows),
 predictor_correct=sum(x["predicted"]==x["oracle"] for x in rows),
 early_placement_correct=sum(x["early_placement"]==x["oracle"] for x in rows),
 predictor_mean_regret_ps=statistics.mean(x["predictor_regret_ps"] for x in rows),
 predictor_max_regret_ps=max(x["predictor_regret_ps"] for x in rows),
 predictor_mean_gain_over_word_ps=statistics.mean(x["predictor_gain_over_word_ps"] for x in rows),
 results_by_context={ctx:{"n":sum(x["context"]==ctx for x in rows),
    "correct":sum(x["predicted"]==x["oracle"] for x in rows if x["context"]==ctx),
    "mean_regret_ps":statistics.mean(x["predictor_regret_ps"] for x in rows if x["context"]==ctx)} for ctx in ("late_high","late_mid","staggered")},
 rows=rows,
 limitations="Hand-crafted XOR contexts; 32x16 and 32x8 tests are correlated; physical seed perturbations are not independent benchmark circuits; predictor uses calibrated routed 32x8 reference architecture models.")
(output/"holdout_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
assert len(rows)==12
