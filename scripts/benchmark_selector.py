#!/usr/bin/env python3
"""Evaluate a *baseline*, not a novel algorithm, for memory variant selection.

Context-blind baseline: word decoder (winner of isolated reference timing).
Context-aware baseline: choose whichever variant has better **early placement**
register-to-register slack, then score using independent routed SPEF timing.
Oracle: best postroute choice, only used for retrospective regret.

The same two candidate placements are required to make the context-aware
decision, so this baseline does not claim low overhead or novelty.
"""
from pathlib import Path
import csv,json,statistics,sys
root=Path(sys.argv[1]);seeds=(11,23,37);modes=("balanced","late_low")
def parse(file):
 import re
 text=file.read_text()
 m=re.search(r'(?m)^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)',text)
 if not m:raise RuntimeError(f"No setup slack {file}")
 return float(m.group(1))
rows=[]
for mode in modes:
 for seed in seeds:
  path={arch:root/arch/mode/f"s{seed}" for arch in ("row","word")}
  early={a:parse(p/"read_reg_to_reg.rpt") for a,p in path.items()}
  actual={a:parse(p/"routed_read_path.rpt") for a,p in path.items()}
  early_best=max(early,key=early.get)
  blind="word"
  oracle=max(actual,key=actual.get)
  rows.append({"mode":mode,"seed":seed,"blind_choice":blind,"early_physical_choice":early_best,
               "oracle_choice":oracle,"blind_slack_ns":actual[blind],
               "early_physical_slack_ns":actual[early_best],
               "oracle_slack_ns":actual[oracle],
               "early_minus_blind_ps":round(1000*(actual[early_best]-actual[blind]),3),
               "blind_oracle_regret_ps":round(1000*(actual[oracle]-actual[blind]),3),
               "early_oracle_regret_ps":round(1000*(actual[oracle]-actual[early_best]),3)})
out=root/"selector_benchmark";out.mkdir(exist_ok=True)
with (out/"comparison.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
summary={
 "status":"BASELINE_EVALUATION_NOT_ORIGINAL_METHOD",
 "n_pairs":len(rows),
 "context_blind_baseline":"word",
 "selector":"maximum placement-stage setup slack with both candidates placed",
 "early_choice_matches_oracle":sum(r["early_physical_choice"]==r["oracle_choice"] for r in rows),
 "mean_early_advantage_over_blind_ps":statistics.mean(r["early_minus_blind_ps"] for r in rows),
 "mean_early_oracle_regret_ps":statistics.mean(r["early_oracle_regret_ps"] for r in rows),
 "mean_early_advantage_by_context_ps":{m:statistics.mean(r["early_minus_blind_ps"] for r in rows if r["mode"]==m) for m in modes},
 "rows":rows,
 "limitations":["two hand-crafted address cones","single 32x8 memory size","placement performed for both candidates","three physical seeds, not a general statistical population","no energy/power or overhead benchmark","not a novel context-aware selection algorithm"]}
(out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="rows"},indent=2))
