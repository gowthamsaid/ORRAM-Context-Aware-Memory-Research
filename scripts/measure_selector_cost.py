#!/usr/bin/env python3
"""Measured candidate implementation-work cost of row/word selection.

Times include one Docker invocation per placement or route (therefore are
wall-clock implementation-stage costs, not pure EDA CPU and not whole CI time).
Includes no reference library characterization time unless separately known.
Compares blind-word, preplacement selector, dual-placement selector, two-route
oracle using same recorded per-stage timings; do not claim prospective
wall-clock speedup from adding these sequentially to a parallel CI matrix.
"""
import csv,json,statistics,sys
from pathlib import Path
physical=Path(sys.argv[1]);predictions=Path(sys.argv[2]);out=Path(sys.argv[3])
out.mkdir(parents=True,exist_ok=True)
choices={(x["size"],x["context"]):x["predicted"] for x in csv.DictReader(predictions.open())}
records=[]
for width in (8,16):
 for ctx in ("ring24","serpentine_tile","dma_stride"):
  for seed in (11,23):
   runs={}
   for arch in ("row","word"):
    p=physical/f"32x{width}"/"integration"/arch/ctx/f"s{seed}"
    q={}
    for kind,file in (("placement","place_seconds.txt"),("route","route_seconds.txt")):
     val=float((p/file).read_text().strip().splitlines()[-1])
     if val<=0:raise RuntimeError(f"Missing positive runtime for {p/file}")
     q[kind]=val
    runs[arch]=q
   guess=choices[f"32x{width}",ctx]
   row,word=runs["row"],runs["word"]
   blind=word["placement"]+word["route"]
   selected=runs[guess]["placement"]+runs[guess]["route"]
   exhaustive_placed=row["placement"]+word["placement"]+runs[guess]["route"]
   routed_oracle=row["placement"]+row["route"]+word["placement"]+word["route"]
   records.append(dict(width=width,context=ctx,seed=seed,decision=guess,
     blind_word_seconds=round(blind,3),select_one_seconds=round(selected,3),
     dual_placement_seconds=round(exhaustive_placed,3),
     both_routed_seconds=round(routed_oracle,3),
     decision_extra_over_blind_seconds=round(selected-blind,3),
     dual_placement_extra_over_predictor_seconds=round(exhaustive_placed-selected,3)))
with (out/"implementation_cost.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
summary={
 "pairs":len(records),
 "means_seconds":{k:round(statistics.mean(x[k] for x in records),3) for k in
 ("blind_word_seconds","select_one_seconds","dual_placement_seconds","both_routed_seconds",
  "decision_extra_over_blind_seconds","dual_placement_extra_over_predictor_seconds")},
 "notes":[
  "Selection itself does not require a target RAM placement, but calibration and independent Liberty analysis are extra work and are NOT included in these means.",
  "The model is instantiated in the original frozen predictor workflow using a mapped address cone, and it still needs a chosen RAM placement+route.",
  "These per-stage Docker wall seconds vary with runner load and cannot establish full end-to-end speedup or energy benefit.",
  "Both row/word variants were generated in the experimental workflow for oracle measurement; that testing work is not counted as online prediction."
 ],
 "samples":records}
(out/"cost_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="samples"},indent=2))
