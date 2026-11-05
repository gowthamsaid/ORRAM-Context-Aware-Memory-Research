#!/usr/bin/env python3
"""Assess original per-pin routed memory-boundary suffixes at identical endpoint Qs.

This deliberately does not treat endpoint-matched output timing as proof of
physical identity: paths can use different internal word lines/rise/fall senses.
"""
import csv,json,sys,statistics
from pathlib import Path
root=Path(sys.argv[1])
rows=list(csv.DictReader((root/"boundary_suffix_paths.csv").open()))
out=[]
for size in ("32x8","32x16"):
 for context in ("balanced","late_low"):
  for q in ([0,7] if size=="32x8" else [0,7,14]):
   diffs=[]
   for bit in range(5):
    k=lambda a:next(r for r in rows if r["size"]==size and r["context"]==context and r["arch"]==a and int(r["address_bit"])==bit and r["selected_target"]==f"q{q}")
    r,w=k("row"),k("word")
    if r["endpoint"]!=w["endpoint"]:
     raise RuntimeError("Endpoint mismatch under fixed-q constraint")
    diffs.append(round(float(r["suffix_ps"])-float(w["suffix_ps"]),4))
   out.append(dict(size=size,context=context,endpoint=f"Q{q}",row_minus_word_suffix_ps_by_address=diffs,mean_across_addresses_ps=round(statistics.mean(diffs),4),positive_count=sum(x>0 for x in diffs),negative_count=sum(x<0 for x in diffs)))
summary={"cases":out,"endpoint_matched_comparisons":len(out)*5,
"important_limitations":"Fixed output endpoints allow more comparable timing sensitivities, but input launch FF and sensitized internal word line, edge polarity, routing and load may differ. Averaging address-pin suffixes is NOT a legitimate overall timing metric or architecture predictor by itself."}
(root/"fixed_endpoint_comparison.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps(summary,indent=2))
