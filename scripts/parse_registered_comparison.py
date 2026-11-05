#!/usr/bin/env python3
"""Cross-architecture comparison of matched top-level routed paths, deterministic placement only."""
from pathlib import Path
import re,csv,json,sys
root=Path(sys.argv[1])
rows=[]
for mode in ("balanced","late_low"):
 for arch in ("row","word"):
  p=root/arch/mode
  if not (p/"routed_flow_status.txt").is_file():
   raise SystemExit(f"BLOCKED: routing/extraction status missing: {p}")
  if "ROUTED_AND_SPEF_IMPORTED" not in (p/"routed_flow_status.txt").read_text():
   raise SystemExit(f"BLOCKED: not routed: {p}")
  if "SEED_UNSUPPORTED" not in (p/"seed_status.txt").read_text():
   raise SystemExit("BLOCKED: independent seed definition changed; recheck before comparison")
  rpt=(p/"routed_read_path.rpt").read_text()
  if "Startpoint:" not in rpt or "Endpoint:" not in rpt:
   raise SystemExit(f"BLOCKED: no target path {p}")
  first="Startpoint:"+rpt.split("Startpoint:",1)[1].split("Startpoint:",1)[0]
  def pick(pattern,field):
   m=re.search(pattern,first,re.M)
   if not m:raise ValueError(f"Missing {field} in {p}")
   return m.group(1).strip()
  def metrics(txt):
   return float(pick(r'^\s*([+-]?\d+\.\d+)\s+data arrival time\s*$',"arrival")),float(pick(r'^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)',"slack"))
  arrival,slack=metrics(first)
  if "u_addrff_" not in first or "u_capture_" not in first:
   raise SystemExit(f"BLOCKED: wrong path class in {p}")
  placement=(p/"read_reg_to_reg.rpt").read_text()
  pa=float(re.search(r'^\s*([+-]?\d+\.\d+)\s+data arrival time\s*$',placement,re.M).group(1))
  ps=float(re.search(r'^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)',placement,re.M).group(1))
  rows.append(dict(mode=mode,arch=arch,postroute_slack_ns=slack,
      postroute_arrival_ns=arrival,postplacement_slack_ns=ps,
      postplacement_arrival_ns=pa,read_path_start=pick(r'^Startpoint:\s*(.+)$',"start").split(" (")[0],
      read_path_end=pick(r'^Endpoint:\s*(.+)$',"end").split(" (")[0],
      spef_size=(p/"routed.spef").stat().st_size))
out=root/"cross_comparison";out.mkdir(exist_ok=True)
with (out/"results.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
by={(r["mode"],r["arch"]):r for r in rows}
def preference(mode):
 delta=by[(mode,"row")]["postroute_slack_ns"]-by[(mode,"word")]["postroute_slack_ns"]
 return ("row" if delta >0.020 else "word" if delta < -0.020 else "tie",round(delta,6))
b=preference("balanced");l=preference("late_low")
reversal=b[0]!="tie" and l[0]!="tie" and b[0]!=l[0]
summary={"reversal":reversal,"balanced_preference":b,"late_low_preference":l,
 "experimental_status":"DETERMINISTIC_SINGLE_PLACEMENT_ONLY",
 "assumptions":["same flattened 32x8 memory size and nominal area/SDC within each wrapper context",
 "mapped gate netlist retained without synthesis",
 "registered wrapper with no clock tree insertion or power/signal signoff",
 "routed SPEF was extracted and reimported for timing",
 "no independent placement seeds; cannot assert robustness",
 "context itself includes additional address buffer cells and different placement"]}
(out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
for x in rows:print(x)
