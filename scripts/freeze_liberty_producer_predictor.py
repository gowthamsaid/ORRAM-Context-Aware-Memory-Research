#!/usr/bin/env python3
"""Pre-placement Liberty-STA selector on structurally distinct address producers.

Calibration remains reference 32x8/balanced/seed11 routed RAM-side suffixes.
Per-application timing is from only a small address-producer netlist with a
fixed hypothetical capacitive load on its outputs. No candidate RAM placement,
routing, or actual heldout timing is consulted to produce the selections.
"""
import csv,json,re,sys
from pathlib import Path
calibration=Path(sys.argv[1]);presta=Path(sys.argv[2]);out=Path(sys.argv[3])
records=list(csv.DictReader(calibration.open()))
cal={(r["arch"],int(r["address_bit"])):float(r["suffix_ps"]) for r in records
     if r["size"]=="32x8" and r["context"]=="balanced" and r["seed"]=="11" and r["selected_target"]=="worst"}
assert len(cal)==10
results=[]
for width in (8,16):
 for kind in ("binary_increment","gray_encode","gray_decode"):
  starts=[]
  for bit in range(5):
   file=presta/kind/f"addr_{bit}.rpt"
   m=re.search(r'(?m)^\s*([+-]?\d+\.\d+)\s+data arrival time',file.read_text())
   if not m:raise RuntimeError(f"Missing producer arrival: {file}")
   starts.append(1000*float(m.group(1)))
  candidates={a:round(max(starts[i]+cal[a,i] for i in range(5)),4) for a in ("row","word")}
  guess=min(candidates,key=candidates.get)
  results.append(dict(size=f"32x{width}",context=kind,predicted=guess,
    row_estimate_ps=candidates["row"],word_estimate_ps=candidates["word"],
    estimated_margin_ps=round(abs(candidates["row"]-candidates["word"]),4),
    address_arrivals_ps=[round(x,4) for x in starts]))
out.mkdir(parents=True,exist_ok=True)
with (out/"predictions.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=["size","context","predicted","row_estimate_ps","word_estimate_ps","estimated_margin_ps"])
 w.writeheader()
 for r in results:w.writerow({k:r[k] for k in w.fieldnames})
payload=dict(status="FROZEN_BEFORE_NEW_PHYSICAL_RUN",training="32x8 balanced seed11 routed suffix reference",
 model="max over per-address isolated liberty producer arrival plus frozen downstream physical RAM-side suffix",
 output_load_assumption="0.03 pF, fixed for all address producer outputs",
 no_new_memory_placement=True,
 calibrated_routed_reference_requires_two_architectures=True,
 results=results,
 limitations=["Producer is not physically placed and port load is assumed","Reference arcs are old routed paths rather than generic characterized timing tables","Two word widths use the same 32x8 calibration","Hand-coded counter/Gray motifs are not a survey of industrial RTL"])
(out/"frozen_model.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(payload,indent=2))
