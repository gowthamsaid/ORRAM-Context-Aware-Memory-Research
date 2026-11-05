#!/usr/bin/env python3
"""Validate physical placement diversity and architecture timing under three paired seeds."""
from pathlib import Path
import csv,hashlib,json,re,statistics,sys
root=Path(sys.argv[1]);seeds=(11,23,37);rows=[]
for mode in ("balanced","late_low"):
 for arch in ("row","word"):
  signatures=set()
  for seed in seeds:
   p=root/arch/mode/("s"+str(seed))
   mark=(p/"seed_status.txt").read_text().strip()
   if mark != f"SEED_SUPPORTED:{seed}":raise SystemExit(f"BAD SEED: {p}: {mark}")
   d=(p/"placed.def").read_text()
   components=re.search(r"(?ms)^\s*COMPONENTS\s+\d+\s*;(.*?)^\s*END COMPONENTS",d)
   if not components:raise SystemExit(f"BLOCKED: no placement components {p}")
   records=re.findall(r"(?ms)^\s*-\s+(\S+)\s+(\S+)(.*?);",components.group(1))
   coords=[]
   for name,master,rest in records:
    m=re.search(r"\+\s+(?:PLACED|FIXED)\s+\(\s*(\d+)\s+(\d+)\s*\)",rest)
    if m:coords.append((name,int(m.group(1)),int(m.group(2))))
   if len(coords)<700:raise SystemExit(f"BLOCKED: too few placed cells {p}: {len(coords)}")
   sig=hashlib.sha256(json.dumps(sorted(coords)).encode()).hexdigest()
   if sig in signatures:raise SystemExit(f"BLOCKED: duplicate physical placement {arch}/{mode} seed {seed}")
   signatures.add(sig)
   rpt=(p/"routed_read_path.rpt").read_text()
   if "Startpoint: u_addrff_" not in rpt or "Endpoint: u_capture_" not in rpt:raise SystemExit("Wrong read path")
   first="Startpoint:"+rpt.split("Startpoint:",1)[1].split("Startpoint:",1)[0]
   def find(pattern):
    m=re.search(pattern,first,re.M)
    if not m:raise SystemExit(f"malformed report {p}: {pattern}")
    return m.group(1)
   slack=float(find(r'^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)'))
   arrival=float(find(r'^\s*([+-]?\d+\.\d+)\s+data arrival time'))
   if (p/"routed.spef").stat().st_size<1000:raise SystemExit("missing SPEF")
   if "ROUTED_AND_SPEF_IMPORTED" not in (p/"routed_flow_status.txt").read_text():raise SystemExit("SPEF no-read")
   rows.append(dict(seed=seed,mode=mode,arch=arch,slack_ns=slack,arrival_ns=arrival,
                    placement_sha256=sig,cell_count=len(coords)))
out=root/"multi_seed_summary";out.mkdir(exist_ok=True)
with (out/"timing.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
by={(r["seed"],r["mode"],r["arch"]):r for r in rows}
effects=[]
for mode in ("balanced","late_low"):
 diffs=[]
 for seed in seeds:
  delta=by[(seed,mode,"row")]["slack_ns"]-by[(seed,mode,"word")]["slack_ns"]
  diffs.append(delta)
  effects.append(dict(seed=seed,mode=mode,row_minus_word_slack_ns=round(delta,6),
                      winner=("row" if delta>0.020 else "word" if delta<-.020 else "tie")))
summary={"per_seed_effects":effects,"distinct_placements_per_arch_per_mode":len(seeds),
   "mean_row_minus_word_ns":{m:statistics.mean(e["row_minus_word_slack_ns"] for e in effects if e["mode"]==m) for m in ("balanced","late_low")},
   "seed_count":len(seeds),
   "limitations":["clock is ideal; no CTS/IR/EM/DRC/LVS signoff","physically modified balanced vs late_low wrappers contain different numbers of buffers","small 32x8 standard-cell memory test","postroute extracted SPEF readback performed","no novel architecture-selection algorithm yet"]}
if summary["mean_row_minus_word_ns"]["balanced"] < -0.020 and summary["mean_row_minus_word_ns"]["late_low"] >0.020:
 summary["screening_result"]="MEAN_RANKING_REVERSAL_ACROSS_SEEDS"
else:
 summary["screening_result"]="NO_ROBUST_MEAN_REVERSAL_AT_20PS"
(out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
