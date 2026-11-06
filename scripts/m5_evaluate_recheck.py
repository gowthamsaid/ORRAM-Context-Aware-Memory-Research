#!/usr/bin/env python3
"""Close M5 only if all 24 reopened OpenSTA logs have check_setup output.

Check marker boundaries and report negative findings as failures instead
of ignoring unknown unconstraint notices.
"""
import json,re,sys
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
records=[];errors=[]
redflags=[
 r"Warning:.*(unconstrained|no clock|missing.*delay|no.*(input|output).*delay)",
 r"Error:",
 r"unconstrained (?:endpoints|startpoints|paths)\s*:\s*[1-9]",
]
for width in (8,16):
 for ctx in ("ring24","serpentine_tile","dma_stride"):
  for seed in (11,23):
   for arch in ("row","word"):
    case=root/str(width)/arch/ctx/f"s{seed}"
    logfile=case/"audit.log"
    if not logfile.exists():
     errors.append(f"Missing {logfile}");continue
    text=logfile.read_text(errors="replace")
    a=text.find("M5_CHECK_SETUP_BEGIN")
    b=text.find("M5_CHECK_SETUP_END",a+1)
    if a<0 or b<0:
     errors.append(f"Missing check_setup markers: {logfile}");continue
    check=text[a+len("M5_CHECK_SETUP_BEGIN"):b].strip()
    findings=[line for line in check.splitlines() if any(re.search(p,line,re.I) for p in redflags)]
    if findings:errors.append(f"{case}: "+repr(findings))
    expected=f"M5_POSTROUTE_RECHECK_PASS dir=/study/physical/integration/{arch}/{ctx}/s{seed}"
    if expected not in text:errors.append(f"Missing completed marker {logfile}")
    counts=re.search(r"M5_COUNTS launch=(\d+) capture=(\d+) input=(\d+) output=(\d+)",text)
    if not counts or tuple(map(int,counts.groups()))!=(5,width,6+width,width):
     errors.append(f"Bad registered count {logfile}")
    for p in ("target_read.rpt","all_setup.rpt","wns.rpt","hold_wns.rpt","tns.rpt","provenance.txt"):
     if not (case/p).exists() or (case/p).stat().st_size == 0:
      errors.append(f"Missing or empty report {case/p}")
    records.append({"width":width,"mode":ctx,"seed":seed,"architecture":arch,
      "check_setup_excerpt":check[:2500],"warning_matches":findings,"checked":True})
status={"cases":len(records),"errors":errors,"check_setup_excerpt_first":records[0]["check_setup_excerpt"] if records else "",
"interpretation":"Only detects setup errors/warnings in explicit check_setup output; an ideal clock and incomplete signoff remain. Tcl check_setup does not certify electrical/tapeout compliance."}
(out/"recheck_summary.json").write_text(json.dumps(status,indent=2)+"\n")
print(json.dumps(status,indent=2))
if len(records)!=24 or errors:raise SystemExit("M5 recheck evidence failed")
print("M5_COVERAGE_GATE_PASS")
