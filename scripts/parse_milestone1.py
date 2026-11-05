#!/usr/bin/env python3
"""Parse strict first-path audits; no imagined physical verification."""
import csv,json,re,pathlib,sys
root=pathlib.Path(sys.argv[1]);rows=[]
for arch in ("row","word"):
 p=root/arch
 def first(label,style="worst"):
  src=p/f"load_{label}_{style}.rpt"
  txt=src.read_text()
  if "Startpoint:" not in txt:raise ValueError(f"Missing timing path {src}")
  t="Startpoint:"+txt.split("Startpoint:",1)[1].split("Startpoint:",1)[0]
  def extract(pat):
   m=re.search(pat,t,re.M)
   if not m:raise ValueError(f"Malformed report {src} pattern {pat}")
   return m.group(1).strip()
  return {"arch":arch,"load_pf":float(label),"path_kind":style,
   "startpoint":extract(r"^Startpoint:\s*(.+)$").split(" (")[0],
   "endpoint":extract(r"^Endpoint:\s*(.+)$").split(" (")[0],
   "arrival_ns":float(extract(r"^\s*([+-]?\d+\.\d+)\s+data arrival time")),
   "slack_ns":float(extract(r"^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)"))}
 for l in ("0.005","0.050","0.500","5.000"):
  for style in ("worst","q0"):rows.append(first(l,style))
 if not (p/"ram_structural.v").stat().st_size:raise ValueError("structural Verilog export empty")
 if not (p/"extraction_status.txt").is_file():raise ValueError("extraction status missing")
out=root/"summary";out.mkdir(exist_ok=True)
with (out/"load-sensitivity.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
metrics={}
for arch in ("row","word"):
 d={x["load_pf"]:x for x in rows if x["arch"]==arch and x["path_kind"]=="q0"}
 delta=d[5.0]["arrival_ns"]-d[0.005]["arrival_ns"]
 status=(root/arch/"extraction_status.txt").read_text().strip()
 metrics[arch]={"q0_arrival_delta_0.005_to_5pf_ns":round(delta,8),
    "output_load_affects_fixed_endpoint":abs(delta)>1e-5,
    "extraction_status":status,"structural_netlist_nonempty":True}
decision={
 "timing_load_model_ready":all(x["output_load_affects_fixed_endpoint"] for x in metrics.values()),
 "physical_extraction_ready":all(x["extraction_status"]=="EXTRACTION_SUCCEEDED" for x in metrics.values()),
 "architectures":metrics,
 "note":"Place-estimated RC cannot substitute for extracted routed RC; a null load response is a model/debug blocker, not a negative research result."
}
(out/"audit.json").write_text(json.dumps(decision,indent=2)+"\n")
print(json.dumps(decision,indent=2))
