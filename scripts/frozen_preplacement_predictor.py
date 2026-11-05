#!/usr/bin/env python3
"""Frozen cross-context/width *pre-placement* predictor; not a fitted ML model.

Training inputs: per-boundary observations from 32x8/balanced/seed11 ONLY.
Training requires BOTH candidate reference placements once (amortized).
New cases: topology-derived XOR stage count, no candidate placement.
An extra XOR stage is *assumed* to add 55 ps from prior path inspection,
NOT optimized against holdout. The estimated maxima are approximate:
no PDK slew/placement model, setup-time or power correction.
"""
import argparse,csv,json
from pathlib import Path
PROFILES = {"late_high": [1,1,1,3,3], "late_mid": [1,1,3,1,1], "staggered": [2,1,3,1,2]}

p=argparse.ArgumentParser()
p.add_argument("training_csv",type=Path)
p.add_argument("output_dir",type=Path)
args=p.parse_args()
records=list(csv.DictReader(args.training_csv.open()))
training=[r for r in records if r["size"]=="32x8" and r["context"]=="balanced" and r["seed"]=="11" and r["selected_target"]=="worst"]
assert len(training)==10, f"Expected ten calibration rows, got {len(training)}"
cal={}
for arch in ("row","word"):
 by={int(r["address_bit"]):r for r in training if r["arch"]==arch}
 assert set(by)==set(range(5))
 cal[arch]={i:{"boundary_ps":float(by[i]["boundary_time_ns"])*1000,
              "suffix_ps":float(by[i]["suffix_ps"])} for i in range(5)}
# Reuse equal-architecture mean arrival at boundary, not either candidate's
# physical arrival alone. No heldout row or word timing is consulted.
base={i:sum(cal[a][i]["boundary_ps"] for a in ("row","word"))/2 for i in range(5)}
increment=55.0
predictions=[]
for size in (8,16):
 for context in ("late_high","late_mid","staggered"):
  depths=PROFILES[context]
  estimates={}
  critical={}
  for arch in ("row","word"):
   arrival_by_bit=[base[i]+increment*(depths[i]-1)+cal[arch][i]["suffix_ps"] for i in range(5)]
   estimates[arch]=round(max(arrival_by_bit),3)
   critical[arch]=arrival_by_bit.index(max(arrival_by_bit))
  prediction=min(estimates,key=estimates.get)
  predictions.append(dict(size=f"32x{size}",context=context,selection=prediction,
    row_estimated_ps=estimates["row"],word_estimated_ps=estimates["word"],
    confidence_margin_ps=round(abs(estimates["row"]-estimates["word"]),3),
    row_dominant_input=critical["row"],word_dominant_input=critical["word"],
    available_before_new_placement=True))
args.output_dir.mkdir(parents=True,exist_ok=True)
with (args.output_dir/"frozen_predictions.csv").open("w",newline="") as f:
 writer=csv.DictWriter(f,fieldnames=list(predictions[0]))
 writer.writeheader()
 writer.writerows(predictions)
payload={
 "status":"FROZEN_BEFORE_HOLDOUT_PHYSICAL_IMPLEMENTATION",
 "calibration":"32x8 balanced seed11, 10 row/word per-address worst-path reports only",
 "calibration_openroad_required_once":True,
 "prediction_requires_new_placement":False,
 "incremental_xor_delay_ps_per_extra_stage":increment,
 "method":"max across address bits of avg calibrated memory-boundary arrival + 55ps per extra XOR stage + separately calibrated row/word RAM-to-capture suffix",
 "training_base_address_boundary_ps":base,
 "calibration_by_arch":cal,
 "predictions":predictions,
 "warnings":[
  "The training data include previously physically placed and routed 32x8 architectures; only per-new-wrapper placement is avoided.",
  "The 55ps incremental model was not fitted to the held-out physical winners; predictor is preliminary and not a fully analytical PDK model.",
  "Predictions cannot establish energy/power/area benefit; no new architecture placement is used at prediction time.",
  "Two holdout memory widths share the same training arcs, so accuracy is not statistical independence."
 ]
}
(args.output_dir/"frozen_protocol.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(payload,indent=2))
