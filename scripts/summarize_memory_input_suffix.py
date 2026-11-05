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
            folder = root / size / arch / context / "s11"
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
                        size=size, context=context, arch=arch, address_bit=bit,
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

cases = []
for size in ("32x8", "32x16"):
    for context in ("balanced", "late_low"):
        per = {}
        for bit in range(5):
            r = next(x for x in rows if x["size"] == size and x["context"] == context and x["arch"] == "row" and x["address_bit"] == bit and x["selected_target"] == "worst")
            w = next(x for x in rows if x["size"] == size and x["context"] == context and x["arch"] == "word" and x["address_bit"] == bit and x["selected_target"] == "worst")
            per[f"A{bit}"] = dict(
                row_suffix_ps=r["suffix_ps"],
                word_suffix_ps=w["suffix_ps"],
                row_minus_word_ps=round(r["suffix_ps"]-w["suffix_ps"], 4),
                row_end=r["endpoint"], word_end=w["endpoint"],
                note="Worst path through each boundary may have distinct launch/endpoint and transition",
            )
        cases.append(dict(size=size, context=context, per_address=per))
summary = dict(path_count=len(rows), cases=cases,
    conditions="Nangate45 typical, ideal 4ns clock, original routed ODB/SDC/SPEF, seed 11",
    interpretation="Suffix is path-specific time from last XOR driver Z to capture D, not intrinsic memory arc.",
    limitations="Different output endpoints/transitions may be selected, and boundary driver slew/loading differ; cross-context implementations have distinct placement and routing. No universal causal attribution.",
    next_gate="Compare fixed output Q0/Q7/(Q14) and characterize input slew/load before freezing any predictive rule.")
(root / "boundary_suffix_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
