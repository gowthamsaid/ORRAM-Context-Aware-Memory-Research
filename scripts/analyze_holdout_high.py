#!/usr/bin/env python3
"""Held-out delayed-high-address physical context, preregistered negative control."""
from pathlib import Path
import re,hashlib,json,statistics,csv,sys
root=Path(sys.argv[1]);rows=[]
for arch in ("row","word"):
 seen=set()
 for seed in (11,23,37):
  p=root/arch/"late_high"/f"s{seed}"
  assert (p/"seed_status.txt").read_text().strip()==f"SEED_SUPPORTED:{seed}",p
  def slack(file):
   m=re.search(r'(?m)^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)',(p/file).read_text())
   if not m:raise SystemExit(f"BLOCKED: no valid slack in {p/file}")
   return float(m.group(1))
  def_text=(p/"placed.def").read_text()
  comp=re.search(r"(?ms)^\s*COMPONENTS\s+\d+\s*;(.*?)^\s*END COMPONENTS",def_text).group(1)
  matches=[]
  for name,master,rest in re.findall(r"(?ms)^\s*-\s+(\S+)\s+(\S+)(.*?);",comp):
   m=re.search(r"\+\s+(?:PLACED|FIXED)\s+\(\s*(\d+)\s+(\d+)\s*\)",rest)
   if m:matches.append((name,int(m.group(1)),int(m.group(2))))
  if len(matches)<700:raise SystemExit("missing placement records")
  h=hashlib.sha256(json.dumps(sorted(matches)).encode()).hexdigest()
  if h in seen:raise SystemExit("DUPLICATE_PLACEMENT")
  seen.add(h)
  if (p/"routed.spef").stat().st_size<10000:raise SystemExit("SPEF missing")
  if (p/"routed_flow_status.txt").read_text().strip()!="ROUTED_AND_SPEF_IMPORTED":raise SystemExit("Missing SPEF reimport")
  rows.append({"seed":seed,"arch":arch,"placement_slack_ns":slack("read_reg_to_reg.rpt"),
               "routed_slack_ns":slack("routed_read_path.rpt"),"placement_sha256":h})
by={(x["seed"],x["arch"]):x for x in rows}
deltas=[];correct=[]
for seed in (11,23,37):
 row,word=by[(seed,"row")],by[(seed,"word")]
 d=row["routed_slack_ns"]-word["routed_slack_ns"]
 deltas.append(d)
 early="row" if row["placement_slack_ns"]>word["placement_slack_ns"] else "word"
 oracle="row" if d>0 else "word"
 correct.append(early==oracle)
summary={"heldout_context":"late_high","seed_count":3,"separate_placement_signatures_per_arch":3,
         "row_minus_word_routed_slack_ns":deltas,
         "mean_row_minus_word_ns":statistics.mean(deltas),
         "physical_early_selector_matches_oracle":sum(correct),
         "expected_negative_control":"word selected when high-order address bits arrive late",
         "caveats":["three seeded small-memory designs only",
                    "delayed cone uses preserved buffer chain",
                    "not full-chip signoff or novelty proof"]}
out=root/"holdout_high_summary";out.mkdir(exist_ok=True)
(out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
with (out/"results.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(json.dumps(summary,indent=2))
