#!/usr/bin/env python3
"""Audit postroute RAM address-boundary timing suffixes, with raw evidence.

Given each FF-to-capture report constrained THROUGH the final XOR driver
feeding addr_mem[bit], subtract that driver's reported timing arrival
from the capture/D arrival on the *same path*. The result includes physical
input net and RAM decoder/storage/output delay, and does not claim to be
an intrinsic abstract Liberty arc.
"""
import csv
import json
import re
import statistics
import sys
from pathlib import Path

root = Path(sys.argv[1])
rows = []
point = re.compile(
    r'^\s*(?:\d+\s+[\d.]+\s+)?[\d.]+\s+([\d.]+)\s+([\d.]+)\s+[\^v]\s+'
    r'(\S+)\s+\(([^)]+)\)\s*$'
)
for size in ("32x8", "32x16"):
    for context in ("balanced", "late_low"):
        for arch in ("row", "word"):
            for seed in (11,23,37):
                folder = root / size / arch / context / f"s{seed}"
                stages = {"balanced": 0, "late_low": None}
                targets = [0, 7] + ([14] if size == "32x16" else [])
                for bit in range(5):
                    stage = 2 if context == "late_low" and bit < 2 else 0
                    boundary = f"u_mix_{bit}_{stage}/Z"
                    for target in ["worst"] + [f"q{q}" for q in targets]:
                        path = folder / f"address_{bit}_{target}.rpt"
                        contents = path.read_text()
                        if "Startpoint:" not in contents or "Endpoint:" not in contents:
                            raise RuntimeError(f"Missing valid report {path}")
                        # Each worst report may include 8 paths. Here the first
                        # is the worst of its -through-constrained paths.
                        first = "Startpoint:" + contents.split("Startpoint:", 1)[1].split("Startpoint:", 1)[0]
                        m_start = re.search(r"(?m)^Startpoint:\s*(\S+)", first)
                        m_end = re.search(r"(?m)^Endpoint:\s*(\S+)", first)
                        m_arrival = re.search(r"(?m)^\s*([+-]?\d+\.\d+)\s+data arrival time", first)
                        m_slack = re.search(r"(?m)^\s*([+-]?\d+\.\d+)\s+slack\s+\((?:MET|VIOLATED)\)", first)
                        if not all((m_start, m_end, m_arrival, m_slack)):
                            raise RuntimeError(f"Missing timing summary {path}")
                        points = []
                        for line in first.splitlines():
                            m = point.match(line)
                            if m:
                                points.append((m.group(3), float(m.group(2)), float(m.group(1))))
                        at_boundary = [p for p in points if p[0] == boundary]
                        at_capture = [p for p in points if p[0] == f"{m_end.group(1)}/D"]
                        if len(at_boundary) != 1 or len(at_capture) != 1:
                            raise RuntimeError(f"Timing boundary/capture point missing {path}: {boundary} {m_end.group(1)}; {points}")
                        btime = at_boundary[0][1]
                        ctime = at_capture[0][1]
                        arrival = float(m_arrival.group(1))
                        if abs(ctime - arrival) > 0.00001:
                            raise RuntimeError(f"Capture pin time differs from arrival in {path}")
                        suffix = (ctime - btime) * 1000
                        if suffix < -0.001:
                            raise RuntimeError(f"Negative downstream delay in {path}")
                        rows.append(dict(
                            size=size, context=context, arch=arch, seed=seed, address_bit=bit,
                            selected_target=target, startpoint=m_start.group(1),
                            endpoint=m_end.group(1),
                            boundary_driver=boundary, boundary_time_ns=btime,
                            capture_time_ns=ctime, suffix_ps=round(suffix, 4),
                            total_slack_ns=float(m_slack.group(1)),
                            source_report=str(path)
                        ))
csvpath = root / "boundary_suffix_paths.csv"
with csvpath.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)


result = []
for size in ("32x8", "32x16"):
 for context in ("balanced","late_low"):
  for seed in (11,23,37):
   for q in ([0,7] if size=="32x8" else [0,7,14]):
    differences = []
    for bit in range(5):
     def pick(arch):
      return next(x for x in rows if x["size"]==size and x["context"]==context and x["seed"]==seed and x["arch"]==arch and x["address_bit"]==bit and x["selected_target"]==f"q{q}")
     a,b=pick("row"),pick("word")
     if a["endpoint"]!=b["endpoint"]:raise RuntimeError("Endpoint not matched")
     differences.append(round(a["suffix_ps"]-b["suffix_ps"],4))
    result.append(dict(size=size,context=context,seed=seed,output=f"Q{q}",
      delta_ps_by_bit=differences,
      low_bits_row_better=all(x<0 for x in differences[:2]),
      high_bits_word_better=all(x>0 for x in differences[3:])))
summary={"path_count":len(rows),"fixed_output_comparisons":sum(len(x["delta_ps_by_bit"]) for x in result),
 "fixed_output_cases":len(result),
 "low_address_row_better_cases":sum(x["low_bits_row_better"] for x in result),
 "high_address_word_better_cases":sum(x["high_bits_word_better"] for x in result),
 "cases":result,
 "interpretation":"Each delta is row-minus-word physical suffix at the same capture register. Positive favors word, negative favors row.",
 "limitations":"Three intentionally perturbed placements per engineered context; not independent real workloads. Different internal sensitization and boundary slew may remain."}
(root/"multiseed_boundary_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(json.dumps({k:v for k,v in summary.items() if k!="cases"},indent=2))
